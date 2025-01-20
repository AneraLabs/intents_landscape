from eth_abi.abi import decode
from web3 import Web3

from normalisation.utils import normalise_address_if_needed


def decode_request(request_bytes: str) -> dict:
    request_bytes = request_bytes.removeprefix("0x")

    # The types are defined in the synapse contract
    # if the contract changes, this will need to be updated
    # IFastBridge -> BridgeTransaction
    fields = [
        ("originChainId", "uint32"),
        ("destChainId", "uint32"),
        ("originSender", "address"),
        ("destRecipient", "address"),
        ("originToken", "address"),
        ("destToken", "address"),
        ("originAmount", "uint256"),
        ("destAmount", "uint256"),
        ("originFeeAmount", "uint256"),
        ("sendChainGas", "bool"),
        ("deadline", "uint256"),
        ("nonce", "uint256"),
    ]

    decoded = list(decode([f[1] for f in fields], bytes.fromhex(request_bytes)))
    result = {}
    for i, (field_name, _) in enumerate(fields):
        result[field_name] = decoded[i]
    return result


def normalise_synapse(original_doc, type, normalised_doc):
    if type == "tx":
        if original_doc["scraper_function"] != "relay":
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None
        normalised_doc["name"] = "order_fill_tx"

        request = original_doc["tx"]["request"]

        decoded_request = decode_request(request)

        normalised_doc["source_address"] = decoded_request["originSender"]
        normalised_doc["destination_address"] = decoded_request["destRecipient"]

        normalised_doc["source_chain"] = decoded_request["originChainId"]
        normalised_doc["destination_chain"] = decoded_request["destChainId"]

        normalised_doc["source_token_address"] = decoded_request["originToken"]
        normalised_doc["destination_token_address"] = decoded_request["destToken"]

        normalised_doc["source_token_amount"] = decoded_request["originAmount"]
        normalised_doc["destination_token_amount"] = decoded_request["destAmount"]

        values_to_hash = [request]
        # pylint: disable=no-value-for-parameter
        order_id_part = str(
            Web3.solidity_keccak(abi_types=["bytes"], values=values_to_hash).hex()
        )
        normalised_doc["order_id"] = (
            str(normalised_doc["source_chain"]) + "_" + order_id_part
        )
        normalised_doc["protocol_fee"] = decoded_request["originFeeAmount"]

        normalised_doc["filler_address"] = original_doc["scraper_from"]

    elif type == "event":
        if original_doc["scraper_event"] == "BridgeRequested":
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_address"] = original_doc["event"]["sender"]
            normalised_doc["destination_address"] = original_doc["event"]["sender"]

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = original_doc["event"]["destChainId"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["originToken"]
            )
            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["event"]["destToken"]
            )

            normalised_doc["source_token_amount"] = original_doc["event"][
                "originAmount"
            ]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "destAmount"
            ]

            normalised_doc["protocol_fee"] = 0

        elif original_doc["scraper_event"] == "BridgeRelayed":
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["source_address"] = original_doc["event"]["to"]
            # Note there is a relayExecutionInfo.updatedRecipient,
            # we should check how this is used..
            normalised_doc["destination_address"] = original_doc["event"]["to"]

            normalised_doc["source_chain"] = original_doc["event"]["originChainId"]
            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["originToken"]
            )
            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["event"]["destToken"]
            )

            normalised_doc["source_token_amount"] = original_doc["event"][
                "originAmount"
            ]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "destAmount"
            ]

            # TODO double check that this is safe, is there a token swap happening?
            normalised_doc["protocol_fee"] = 0

            # Ideally we'd use the value in original_doc['event']['relayer'],
            # however this would be inconsistent with txs
            # which do not expose this. Without looking at the inner txs the originating
            # EOA is the best we can do for now
            normalised_doc["filler_address"] = original_doc["scraper_from"]
        else:
            print(f"Unknown event type {original_doc['scraper_event']}")
            return None

        normalised_doc["order_id"] = (
            str(normalised_doc["source_chain"])
            + "_"
            + str(original_doc["event"]["transactionId"])
        )

    # approximate prove and claim gas paid
    if (
        normalised_doc["name"] in {"order_fill_tx", "order_fill_event"}
        and "source_chain" in normalised_doc
    ):
        if normalised_doc["source_chain"] == "1":
            normalised_doc["scraper_prove_gas_paid_usd"] = 2.0
            normalised_doc["scraper_claim_gas_paid_usd"] = 1.8
        else:
            normalised_doc["scraper_prove_gas_paid_usd"] = 0.01
            normalised_doc["scraper_claim_gas_paid_usd"] = 0.01

    return normalised_doc
