import json
import os

from eth_abi.abi import encode
from eth_abi.exceptions import EncodingTypeError
from web3 import Web3

from normalisation.constants import SOLANA_CHAIN_ID
from normalisation.utils import normalise_address_if_needed, safe_checksum_address
from protocol_data.nitro import NITRO_CHAIN_ID_TO_CONTRACT_ADDRESS

# MAYBE: alternatively we could send requests like:
# but that would need to be moved to ingestion step
# - normalisation should use as little external calls as possible
# https://api.poap-nft.routerprotocol.com/feeManager/dest?network=mainnet&srcChainId=1&destChainId=137&srcTokenAddr=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

# downloaded from
# https://raw.githubusercontent.com/router-protocol/nitro-tokens/refs/heads/main/src/mainnet/allTokens.json
NITRO_TOKENS = {}
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NITRO_TOKENS_PATH = os.path.join(SCRIPT_DIR, "nitro_tokens.json")


def normalise_nitro_tokens(nitro_tokens: list[dict]) -> list[dict]:
    for nitro_token in nitro_tokens:
        nitro_token["address"] = safe_checksum_address(nitro_token["address"])
        if nitro_token["chainId"] == "solana":
            nitro_token["chainId"] = SOLANA_CHAIN_ID
    return nitro_tokens


with open(NITRO_TOKENS_PATH, encoding="utf-8") as f:
    NITRO_TOKENS = json.load(f)
    NITRO_TOKENS = normalise_nitro_tokens(NITRO_TOKENS)


def get_nitro_token(
    chain_id: str, token_address: str | None = None, token_id: str | None = None
) -> dict | None:
    if token_address is not None:
        token_address = safe_checksum_address(token_address)

    if token_address is None and token_id is None:
        raise ValueError("Either token_address or token_id must be provided")

    for nitro_token in NITRO_TOKENS:
        if nitro_token["chainId"] != chain_id:
            continue

        if token_address is not None and nitro_token["address"] == token_address:
            return nitro_token

        if token_id is not None and nitro_token["id"] == token_id:
            return nitro_token

    print(
        f"Could not find nitro token for chain_id: [{chain_id}] "
        f"token_address: [{token_address}] token_id: [{token_id}]"
    )
    return None


def chain_id_to_bytes(chain_id):
    return ("0x" + memoryview(str.encode(str(chain_id))).hex() + "0" * 66)[:66]


def strip_chain_id(string):
    return "".join(filter(str.isdigit, string))


def bytes_to_chain_id(byte_string):
    chain_id = strip_chain_id(bytearray.fromhex(byte_string[2:]).decode("utf-8"))
    if chain_id == "":
        raise ValueError(f"Invalid chain id bytes (might be expected): [{byte_string}]")
    if chain_id == "solana":
        return SOLANA_CHAIN_ID
    return chain_id


def print_lacking_token_info(
    *, tx_hash: str, chain_id: str, token_id: str, token_address: str
):
    tx_hash_to_print = tx_hash
    if tx_hash.startswith("0x"):
        tx_hash_to_print = tx_hash
    else:
        tx_hash_to_print = "0x" + tx_hash
    print(
        f"Please add token matching for chain: [{chain_id}]\n"
        f"token_id: [{token_id}]\n"
        f"token_address: [{token_address}]\n"
        f"tx: [https://explorer.routernitro.com/tx/{tx_hash_to_print}]"
    )


def get_nitro_corresponding_dest_token(original_doc):
    """
    Should only be used for deposit events, because of source chain id
    """
    source_chain = original_doc["scraper_originChain"]
    source_token_address = safe_checksum_address(
        normalise_address_if_needed(original_doc["event"]["srcToken"])
    )
    destination_chain = bytes_to_chain_id(original_doc["event"]["destChainIdBytes"])

    source_token = get_nitro_token(source_chain, source_token_address)
    if source_token is None:
        print_lacking_token_info(
            tx_hash=original_doc["scraper_tx_hash"],
            chain_id=source_chain,
            token_id="???",
            token_address=source_token_address,
        )
        return None
    token_id = source_token["id"]

    destination_token = get_nitro_token(destination_chain, token_id=token_id)

    if destination_token is None:
        print_lacking_token_info(
            tx_hash=original_doc["scraper_tx_hash"],
            chain_id=destination_chain,
            token_id=source_token["id"],
            token_address="???",
        )
        return None

    return destination_token["address"]


def is_valid_nitro(original_doc):
    """
    Fillers might send invalid data, example
    https://explorer.routernitro.com/tx/0x98e2103cdb02a73322e41578b4a24765716fd08c7204df4a3a25bd0a44e0ddea
    """
    try:
        if (
            "tx" in original_doc
            and "relayData" in original_doc["tx"]
            and "srcChainId" in original_doc["tx"]["relayData"]
        ):
            bytes_to_chain_id(original_doc["tx"]["relayData"]["srcChainId"])
        if "event" in original_doc and "destChainIdBytes" in original_doc["event"]:
            bytes_to_chain_id(original_doc["event"]["destChainIdBytes"])
    except Exception:
        return False
    return True


def normalise_nitro_dest_token(destination_token_address: str, original_doc: dict):
    if destination_token_address in {
        "0x0000000000000000000000000000000000000000",
        "0x",
    }:
        # TODO: find out how we can get the true destination token of an intent
        # in some cases the event for deposit specifies default route (USDT -> USDT),
        # but the user requested a swap to ETH and that occured via a separate contract call during fill
        # and we do not see it in the deposit event
        # https://explorer.routernitro.com/tx/0x63cdca787bc2398323362d57f11b1cb74235386eaf76c8a509e212f1798694a5
        return get_nitro_corresponding_dest_token(original_doc)
    return destination_token_address


def _normalise_nitro(original_doc, type, normalised_doc):
    if not is_valid_nitro(original_doc):
        return None

    # url = 'https://api-beta.pathfinder.routerprotocol.com/api/v2/status?srcTxHash=' +
    # original_doc['scraper_tx_hash']

    # max_retries = 10
    # retry_count = 0

    # while True:
    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         response_json = response.json()
    #         break
    #     except Exception as e:
    #         retry_timeout = min(2 ** retry_count, 32)
    #         retry_count += 1
    #         if retry_count > max_retries:
    #             print(f"Failed to fetch nitro dest token: {url}\nRetried {max_retries}
    #                    times, giving up.")
    #             return None
    #         print(f"Failed to fetch nitro dest token: {url}\nError: {e}\nRetrying
    #               {retry_count} / {max_retries} in {retry_timeout} seconds...")
    #         time.sleep(retry_timeout)

    def encode_bytes(
        input_amount,
        src_chain_id,
        deposit_id,
        dest_token,
        recipient,
        contract_address,
        message_bytes,
    ):
        return encode(
            ["uint256", "bytes32", "uint256", "address", "address", "address", "bytes"],
            [
                int(input_amount),
                bytearray.fromhex(src_chain_id[2:]),
                deposit_id,
                normalise_address_if_needed(dest_token),
                normalise_address_if_needed(recipient),
                normalise_address_if_needed(contract_address),
                bytearray.fromhex(message_bytes[2:]),
            ],
        )

    def get_message_hash(
        input_amount, src_chain_id, deposit_id, dest_token, recipient, contract_address
    ):
        def pad_addr(addr):
            return "0x" + addr[2:].rjust(64, "0")

        # pylint: disable=no-value-for-parameter
        return Web3.solidity_keccak(
            abi_types=["uint256", "bytes32", "uint256", "bytes", "bytes", "bytes"],
            values=[
                int(input_amount),
                src_chain_id,
                int(deposit_id),
                pad_addr(dest_token),
                pad_addr(recipient),
                pad_addr(contract_address),
            ],
        ).hex()

    # TODO: fix ruff warnings
    # ruff: noqa: PLR0913, PLR0917
    def get_message_hash_with_calldata(
        input_amount,
        src_chain_id,
        deposit_id,
        dest_token,
        recipient,
        contract_address,
        message_bytes,
    ):
        return Web3.keccak(
            encode_bytes(
                int(input_amount),
                src_chain_id,
                int(deposit_id),
                dest_token,
                recipient,
                contract_address,
                message_bytes,
            )
        ).hex()

    if type == "tx":
        if original_doc["scraper_function"] == "iRelay":
            normalised_doc["name"] = "order_fill_tx"

            normalised_doc["source_chain"] = bytes_to_chain_id(
                original_doc["tx"]["relayData"]["srcChainId"]
            )
            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["destination_address"] = normalise_address_if_needed(
                original_doc["tx"]["relayData"]["recipient"]
            )

            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["tx"]["relayData"]["destToken"]
            )

            normalised_doc["destination_token_amount"] = original_doc["tx"][
                "relayData"
            ]["amount"]

            normalised_doc["filler_address"] = original_doc["scraper_from"]
            normalised_doc["order_id"] = get_message_hash(
                original_doc["tx"]["relayData"]["amount"],
                original_doc["tx"]["relayData"]["srcChainId"],
                original_doc["tx"]["relayData"]["depositId"],
                original_doc["tx"]["relayData"]["destToken"],
                original_doc["tx"]["relayData"]["recipient"],
                original_doc["scraper_contractAddress"],
            )
        elif original_doc["scraper_function"] == "iRelayMessage":
            normalised_doc["name"] = "order_fill_tx"

            normalised_doc["source_chain"] = bytes_to_chain_id(
                original_doc["tx"]["relayData"]["srcChainId"]
            )
            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["destination_address"] = original_doc["tx"]["relayData"][
                "recipient"
            ]

            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["tx"]["relayData"]["destToken"]
            )

            normalised_doc["destination_token_amount"] = original_doc["tx"][
                "relayData"
            ]["amount"]

            normalised_doc["filler_address"] = original_doc["scraper_from"]
            normalised_doc["order_id"] = get_message_hash_with_calldata(
                original_doc["tx"]["relayData"]["amount"],
                original_doc["tx"]["relayData"]["srcChainId"],
                original_doc["tx"]["relayData"]["depositId"],
                original_doc["tx"]["relayData"]["destToken"],
                original_doc["tx"]["relayData"]["recipient"],
                original_doc["scraper_contractAddress"],
                original_doc["tx"]["relayData"]["message"],
            )
        else:
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None

    elif type == "event":
        if original_doc["scraper_event"] == "FundsDeposited":
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )

            normalised_doc["source_address"] = original_doc["event"]["depositor"]
            normalised_doc["destination_address"] = original_doc["event"]["recipient"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["srcToken"]
            )
            normalised_doc["destination_token_address"] = normalise_nitro_dest_token(
                original_doc["event"]["destToken"], original_doc
            )

            normalised_doc["source_token_amount"] = original_doc["event"]["amount"]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "destAmount"
            ]

            destination_chain = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )
            if destination_chain not in NITRO_CHAIN_ID_TO_CONTRACT_ADDRESS:
                print(
                    f"Nitro contract address for chain id {destination_chain} "
                    "not found, skipping"
                )
                return None

            destination_chain_contract_address = NITRO_CHAIN_ID_TO_CONTRACT_ADDRESS[
                destination_chain
            ]

            if normalised_doc["destination_token_address"] is None:
                print(
                    "Could not normalise destination token address for nitro doc: "
                    f'[{original_doc.get("_id", "N/A")}], skipping document...'
                )
                return None

            normalised_doc["order_id"] = get_message_hash(
                normalised_doc["destination_token_amount"],
                chain_id_to_bytes(original_doc["scraper_originChain"]),
                original_doc["event"]["depositId"],
                normalised_doc["destination_token_address"],
                original_doc["event"]["recipient"],
                destination_chain_contract_address,
            )

        elif original_doc["scraper_event"] == "FundsPaid":
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["order_id"] = original_doc["event"]["messageHash"]
            normalised_doc["filler_address"] = original_doc["event"]["forwarder"]

        elif original_doc["scraper_event"] == "FundsDepositedWithMessage":
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )

            normalised_doc["source_address"] = original_doc["event"]["depositor"]
            normalised_doc["destination_address"] = original_doc["event"]["recipient"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["srcToken"]
            )
            normalised_doc["destination_token_address"] = normalise_nitro_dest_token(
                original_doc["event"]["destToken"], original_doc
            )

            normalised_doc["source_token_amount"] = original_doc["event"]["amount"]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "destAmount"
            ]

            destination_chain = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )
            destination_chain_contract_address = NITRO_CHAIN_ID_TO_CONTRACT_ADDRESS[
                destination_chain
            ]

            if not destination_chain_contract_address:
                print(
                    f"Nitro contract address for chain id "
                    f"[{destination_chain}] not found"
                )
                return None

            if normalised_doc["destination_token_address"] is None:
                print(
                    f'Could not normalise destination token address for nitro doc: '
                    f'[{original_doc.get("_id", "N/A")}], skipping document...'
                )
                return None

            normalised_doc["order_id"] = get_message_hash_with_calldata(
                normalised_doc["destination_token_amount"],
                chain_id_to_bytes(original_doc["scraper_originChain"]),
                original_doc["event"]["depositId"],
                normalised_doc["destination_token_address"],
                original_doc["event"]["recipient"],
                destination_chain_contract_address,
                original_doc["event"]["message"],
            )

        elif original_doc["scraper_event"] == "FundsPaidWithMessage":
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["order_id"] = original_doc["event"]["messageHash"]
            normalised_doc["filler_address"] = original_doc["event"]["forwarder"]

        else:
            print(f"Unknown event type {original_doc['scraper_event']}")
            return None

    # approximate gas paid for claim events
    if normalised_doc["name"] in {"order_fill_tx", "order_fill_event"}:
        # nitro claim happens on their own chain
        normalised_doc["scraper_claim_gas_paid_usd"] = 0.01

    return normalised_doc


def normalise_nitro(original_doc, type, normalised_doc):
    try:
        return _normalise_nitro(original_doc, type, normalised_doc)
    # FIXME: improve encoding handling for chains like Osmosis
    except EncodingTypeError as e:
        print(f"Expected error during nitro normalisation: [{e}]")
        return None


# ruff: noqa: E501
if __name__ == "__main__":
    # deposit
    deposit_event = {
        "_id": {
            "protocol": "nitro",
            "origin_chain_id": "169",
            "tx_hash": "fbce2afda5510afb6bc9345233d57ea02880859dede5041b15d7a9e229ed2d85",
            "protocol_order_id": "29021",
        },
        "scraper_originChain": "169",
        "scraper_blockNumber": 3665203,
        "scraper_tx_hash": "fbce2afda5510afb6bc9345233d57ea02880859dede5041b15d7a9e229ed2d85",
        "scraper_blockTimestamp": 1730875989,
        "scraper_protocol": "nitro",
        "scraper_contractAddress": "0x21c1E74CAaDf990E237920d5515955a024031109",
        "scraper_event": "FundsDepositedWithMessage",
        "scraper_from": "0x8ca1Cd24Bd7A2386f523C36832D25E468072101a",
        "scraper_to": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_effectiveGasPrice": "20000000",
        "scraper_gasUsed": "599393",
        "event": {
            "partnerId": "1",
            "amount": "9819794",
            "destChainIdBytes": "0x3834353300000000000000000000000000000000000000000000000000000000",
            "destAmount": "9738348",
            "depositId": "29021",
            "srcToken": "0xb73603C5d87fA094B7314C74ACE2e64D165016fb",
            "recipient": "0x02d728b9c1513478a6b6de77a92648e1d8f801e7",
            "depositor": "0x8ca1Cd24Bd7A2386f523C36832D25E468072101a",
            "destToken": "0x",
            "message": "0x00000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000d476c6c61242b000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000000000000000000000000000000009400000000000000000000000008ca1cd24bd7a2386f523c36832d25e468072101a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009800000000000000000000000000000000000000000000000000000000000000002000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda02913000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000078490411a32000000000000000000000000dec876911cbe9428265af0d12132c52ee8642a99000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000833589fcd6edb6e08f4c7c32d4f71b54bda029130000000000000000000000004200000000000000000000000000000000000006000000000000000000000000dec876911cbe9428265af0d12132c52ee8642a9900000000000000000000000002d728b9c1513478a6b6de77a92648e1d8f801e7000000000000000000000000000000000000000000000000000000000094986c000000000000000000000000000000000000000000000000000d476c6c61242b000000000000000000000000000000000000000000000000000d58818d15badd0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000d2137a6d0ef438a7c2bb38eeef364500271658be00000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000034000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000104e5b07cdb0000000000000000000000001db0d0cb84914d09a92ba11d122bab732ac35fe00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000094986c000000000000000000000000dec876911cbe9428265af0d12132c52ee8642a9900000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000002e833589fcd6edb6e08f4c7c32d4f71b54bda02913000000420000000000000000000000000000000000000600001200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000648a6a1e850000000000000000000000004200000000000000000000000000000000000006000000000000000000000000353c1f0bc78fbbc245b3c93ef77b1dcc5b77d2a0000000000000000000000000000000000000000000000000000d58818d15badd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000001a49f865422000000000000000000000000420000000000000000000000000000000000000600000000000000000000000000000001000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000004400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000064d1660f99000000000000000000000000420000000000000000000000000000000000000600000000000000000000000002d728b9c1513478a6b6de77a92648e1d8f801e7000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000fa200000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000",
        },
    }

    # default route
    destination_token_address = get_nitro_corresponding_dest_token(deposit_event)
    assert (
        "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        == get_nitro_corresponding_dest_token(deposit_event)
    )

    normalised_deposit = normalise_nitro(deposit_event, "event", {})
    print(json.dumps(normalised_deposit, indent=4))

    # fill
    event = {
        "_id": {
            "protocol": "nitro",
            "origin_chain_id": "10",
            "tx_hash": "10e5aa6666eab0154410c220f496ec35542f3b6c73bfa69d69c3c0407cb53549",
            "protocol_order_id": "0xc8fc4831e6dd256954120f01c4a1783ed04f89bc54526981fd65f1f601ac6f19",
        },
        "scraper_originChain": "10",
        "scraper_blockNumber": 126094746,
        "scraper_tx_hash": "10e5aa6666eab0154410c220f496ec35542f3b6c73bfa69d69c3c0407cb53549",
        "scraper_blockTimestamp": 1727788269,
        "scraper_protocol": "nitro",
        "scraper_contractAddress": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_event": "FundsPaid",
        "scraper_from": "0x00051d55999c7cd91B17Af7276cbecD647dBC000",
        "scraper_to": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_effectiveGasPrice": "1359600",
        "scraper_gasUsed": "89643",
        "event": {
            "messageHash": "0xc8fc4831e6dd256954120f01c4a1783ed04f89bc54526981fd65f1f601ac6f19",
            "forwarder": "0x00051d55999c7cd91B17Af7276cbecD647dBC000",
            "nonce": "171974",
        },
    }

    normalised_doc = normalise_nitro(event, "event", {})
    print(json.dumps(normalised_doc, indent=4))
