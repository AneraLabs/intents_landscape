from normalisation.constants import NATIVE_TOKEN_ADDRESS
from normalisation.utils import normalise_address_if_needed
from protocol_data.solana_parser import UNPARSED_INSTRUCTION_FIELD_NAME

# This module will only work within the context of the parent closed source repository
# TODO: decouple from price_helper
try:
    from services.common.price_helper import PartnerFee, ProtocolFee, add_fee_usd
except ImportError:
    pass


# https://docs.debridge.finance/dln-the-debridge-liquidity-network-protocol/fees-and-supported-chains
DLN_INTERNAL_CHAIN_ID_MAP = {
    "100000001": "245022934",
    "100000002": "100",
    "100000003": "1890",
    "100000004": "1088",
    "100000005": "7171",
    "100000014": "146",
}


def normalise_chain_id(chain_id: str | int) -> str:
    chain_id = str(chain_id)
    if chain_id in DLN_INTERNAL_CHAIN_ID_MAP:
        return DLN_INTERNAL_CHAIN_ID_MAP[chain_id]
    return chain_id


def normalise_native_token_address(normalised_doc):
    native_token_addresses = [
        "0x0000000000000000000000000000000000000000000000000000000000000000",
        "0x0000000000000000000000000000000000000000",
        "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        "11111111111111111111111111111111",
        "0x0",
    ]
    if normalised_doc["source_token_address"] in native_token_addresses:
        normalised_doc["source_token_address"] = NATIVE_TOKEN_ADDRESS
    if normalised_doc["destination_token_address"] in native_token_addresses:
        normalised_doc["destination_token_address"] = NATIVE_TOKEN_ADDRESS


def normalise_dln(original_doc: dict, type: str, normalised_doc: dict) -> dict | None:
    if UNPARSED_INSTRUCTION_FIELD_NAME in original_doc:
        return None

    # give - deposit
    # take - fill

    # dln specifies protocol and partner fees only in the deposits
    protocol_fees = []
    partner_fees = []
    if type == "tx":
        if original_doc["scraper_function"] == "deposit":
            normalised_doc["name"] = "order_deposit_tx"

            normalised_doc["source_address"] = original_doc["scraper_from"]
            normalised_doc["destination_address"] = original_doc["tx"]["orderArgs"][
                "receiverDst"
            ]

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["tx"]["orderArgs"]["giveTokenAddress"]
            )
            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["tx"]["orderArgs"]["take"]["tokenAddress"]
            )

            normalised_doc["source_token_amount"] = original_doc["tx"]["orderArgs"][
                "giveOriginalAmount"
            ]
            normalised_doc["destination_token_amount"] = original_doc["tx"][
                "orderArgs"
            ]["take"]["amount"]

            normalised_doc["order_id"] = original_doc["tx"]["orderId"]

            normalise_native_token_address(normalised_doc)

            if original_doc["scraper_originChain"] == "7565164":
                # in Solana txs there are no data about protocol fees
                # calculating them according to the docs
                # https://docs.debridge.finance/dln-the-debridge-liquidity-network-protocol/fees-and-supported-chains

                # A flat fee is paid in the native gas token of the chain where the order is created
                # for solana it's 0.015 SOL
                native_fix_fee = ProtocolFee(
                    chain_id=normalised_doc["source_chain"],
                    token_address=NATIVE_TOKEN_ADDRESS,
                    amount=int(0.015 * 10**9),
                )
                protocol_fees.append(native_fix_fee)

                # A variable fee of 4bps is paid in the input token
                variable_fee = ProtocolFee(
                    chain_id=normalised_doc["source_chain"],
                    token_address=normalised_doc["source_token_address"],
                    amount=round(float(normalised_doc["source_token_amount"]) * 0.0004),
                )
                protocol_fees.append(variable_fee)

                # partner fees measured in the deposit token
                if (
                    "affiliateFee" in original_doc["tx"]
                    and original_doc["tx"]["affiliateFee"] is not None
                ):
                    fee_doc = original_doc["tx"]["affiliateFee"]
                    partner_fee = PartnerFee(
                        chain_id=normalised_doc["source_chain"],
                        token_address=normalised_doc["source_token_address"],
                        amount=int(fee_doc["amount"]),
                        partner_fee_address=fee_doc["beneficiary"],
                    )
                    partner_fees.append(partner_fee)
            else:
                # no deposit txs for other chains yet
                pass

        elif original_doc["scraper_function"] == "fulfillOrder":
            normalised_doc["name"] = "order_fill_tx"
            if original_doc["scraper_originChain"] == "7565164":
                # Note: this is just for solana
                normalised_doc["source_address"] = original_doc["tx"]["_order"][
                    "makerSrc"
                ]
                normalised_doc["destination_address"] = original_doc["tx"]["_order"][
                    "receiverDst"
                ]

                normalised_doc["source_chain"] = original_doc["tx"]["_order"]["give"][
                    "chainId"
                ]
                normalised_doc["destination_chain"] = original_doc["tx"]["_order"][
                    "take"
                ]["chainId"]

                normalised_doc["source_token_address"] = normalise_address_if_needed(
                    original_doc["tx"]["_order"]["give"]["tokenAddress"]
                )
                normalised_doc["destination_token_address"] = (
                    normalise_address_if_needed(
                        original_doc["tx"]["_order"]["take"]["tokenAddress"]
                    )
                )

                normalised_doc["source_token_amount"] = original_doc["tx"]["_order"][
                    "give"
                ]["amount"]
                normalised_doc["destination_token_amount"] = original_doc["tx"][
                    "_order"
                ]["take"]["amount"]

                normalised_doc["order_id"] = original_doc["tx"]["orderId"]
                normalised_doc["protocol_fee"] = 0

                normalised_doc["filler_address"] = original_doc["scraper_from"]
            else:
                # EVM chains
                normalised_doc["source_address"] = original_doc["tx"]["_order"][
                    "makerSrc"
                ]
                normalised_doc["destination_address"] = original_doc["tx"]["_order"][
                    "receiverDst"
                ]

                normalised_doc["source_chain"] = original_doc["tx"]["_order"][
                    "giveChainId"
                ]
                normalised_doc["destination_chain"] = original_doc["tx"]["_order"][
                    "takeChainId"
                ]

                normalised_doc["source_token_address"] = normalise_address_if_needed(
                    original_doc["tx"]["_order"]["giveTokenAddress"]
                )
                normalised_doc["destination_token_address"] = (
                    normalise_address_if_needed(
                        original_doc["tx"]["_order"]["takeTokenAddress"]
                    )
                )

                normalised_doc["source_token_amount"] = original_doc["tx"]["_order"][
                    "giveAmount"
                ]
                normalised_doc["destination_token_amount"] = original_doc["tx"][
                    "_order"
                ]["takeAmount"]
                normalised_doc["order_id"] = original_doc["tx"]["_orderId"]

                normalised_doc["filler_address"] = original_doc["scraper_from"]

            normalise_native_token_address(normalised_doc)
        else:
            print(f"Unknown funciton type {original_doc['scraper_function']}")
            return None

    elif type == "event":
        # shared fields between deposit and fill event
        normalised_doc["source_address"] = original_doc["event"]["order"]["makerSrc"]
        normalised_doc["destination_address"] = original_doc["event"]["order"][
            "receiverDst"
        ]

        normalised_doc["source_chain"] = original_doc["event"]["order"]["giveChainId"]
        normalised_doc["destination_chain"] = original_doc["event"]["order"][
            "takeChainId"
        ]

        normalised_doc["source_token_address"] = normalise_address_if_needed(
            original_doc["event"]["order"]["giveTokenAddress"]
        )
        normalised_doc["destination_token_address"] = normalise_address_if_needed(
            original_doc["event"]["order"]["takeTokenAddress"]
        )

        normalised_doc["source_token_amount"] = original_doc["event"]["order"][
            "giveAmount"
        ]
        normalised_doc["destination_token_amount"] = original_doc["event"]["order"][
            "takeAmount"
        ]

        normalised_doc["order_id"] = original_doc["event"]["orderId"]

        normalise_native_token_address(normalised_doc)

        if original_doc["scraper_event"] == "CreatedOrder":
            # deposit event

            normalised_doc["name"] = "order_deposit_event"

            # protocol has 2 types of fees:
            # 1. flat fee is paid in the native gas token
            if "nativeFixFee" in original_doc["event"]:
                native_fix_fee = ProtocolFee(
                    chain_id=normalised_doc["source_chain"],
                    token_address=NATIVE_TOKEN_ADDRESS,
                    amount=int(original_doc["event"]["nativeFixFee"]),
                )
                protocol_fees.append(native_fix_fee)
            # 2. variable fee is paid in the input token
            if "percentFee" in original_doc["event"]:
                variable_fee = ProtocolFee(
                    chain_id=normalised_doc["source_chain"],
                    token_address=normalised_doc["source_token_address"],
                    amount=int(original_doc["event"]["percentFee"]),
                )
                protocol_fees.append(variable_fee)

            # partner fee
            # measured in the deposit token, both beneficiary address and amount are stored in one hex string
            if (
                "affiliateFee" in original_doc["event"]
                and original_doc["event"]["affiliateFee"] != "0x"
            ):
                # example affiliate_fee_hex 0xb4f34d09124b8c9712957b76707b42510041ecbb00000000000000000000000000000000000000000000000025008e16879daa76
                affiliate_fee_hex = original_doc["event"]["affiliateFee"]
                affiliate_address = "0x" + affiliate_fee_hex[2:42]
                fee_amount_hex = "0x" + affiliate_fee_hex[42:]
                fee_amount = int(fee_amount_hex, 16)
                partner_fee = PartnerFee(
                    chain_id=normalised_doc["source_chain"],
                    token_address=normalise_address_if_needed(
                        normalised_doc["source_token_address"]
                    ),
                    amount=fee_amount,
                    partner_fee_address=affiliate_address,
                )
                partner_fees.append(partner_fee)
        elif original_doc["scraper_event"] == "FulfilledOrder":
            # fill event
            normalised_doc["name"] = "order_fill_event"
            normalised_doc["filler_address"] = original_doc["scraper_from"]
        else:
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None

    if "source_chain" in normalised_doc:
        normalised_doc["source_chain"] = normalise_chain_id(
            normalised_doc["source_chain"]
        )
    if "destination_chain" in normalised_doc:
        normalised_doc["destination_chain"] = normalise_chain_id(
            normalised_doc["destination_chain"]
        )

    add_fee_usd(normalised_doc, protocol_fees, partner_fees)

    if not isinstance(normalised_doc["order_id"], str):
        if (
            "scraper_tx_status" in original_doc
            and original_doc["scraper_tx_status"] == "ok"
        ):
            print(f"Unexcpected order_id type in normalised_doc [{normalised_doc}]")
            return None

    return normalised_doc


# ruff: noqa: E501
if __name__ == "__main__":
    tx_doc = {
        "_id": {
            "protocol": "dln",
            "origin_chain_id": "7565164",
            "tx_hash": "3yTjWsfrWB6Xh48yh5Rqwi5REYysVNAGJpST1Z681YoJhtUxoYgRgwWrJtHoKw33xHXgPeF1pZEH6MS2T9c3JFG9",
            "order_id": "0x966ee4b660b6fc81e337136e12c8c973b168f0aad33417a0b6cc3aaef7a633a0",
        },
        "scraper_protocol": "dln",
        "scraper_originChain": "7565164",
        "scraper_blockNumber": 297150699,
        "scraper_blockTimestamp": 1729647729,
        "scraper_from": "C1m3LAwKiosA4qFhCTMwhFjXaajLuHJMypT75CAkiHuH",
        "scraper_contractAddress": "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4",
        "scraper_tx_status": "ok",
        "scraper_tx_hash": "3yTjWsfrWB6Xh48yh5Rqwi5REYysVNAGJpST1Z681YoJhtUxoYgRgwWrJtHoKw33xHXgPeF1pZEH6MS2T9c3JFG9",
        "scraper_chain_fee": 5003,
        "scraper_chain_prioritization_fee": 2,
        "instruction_type": "outer_instruction",
        "tx": {
            "identifier": "createOrderWithNonce",
            "orderArgs": {
                "allowedCancelBeneficiarySrc": None,
                "allowedTakerDst": None,
                "giveOriginalAmount": 1234222231,
                "givePatchAuthoritySrc": "C1m3LAwKiosA4qFhCTMwhFjXaajLuHJMypT75CAkiHuH",
                "orderAuthorityAddressDst": "0x8958f6f0528595830c47e9835d1c6048f083a90d",
                "receiverDst": "0x8958f6f0528595830c47e9835d1c6048f083a90d",
                "take": {
                    "amount": "1227217936",
                    "chainId": "42161",
                    "tokenAddress": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                },
                "giveTokenAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            },
            "affiliateFee": {
                "amount": "4936889",
                "beneficiary": "4CPQqg2GeUiyykB5Vz5VHMSDbGa6ztjk5RcpdMdm3Hu1",
            },
            "referralCode": 30195,
            "nonce": {"$numberLong": "1729647695461"},
            "metadata": "0x1010000000de362000000000000000000000000000000000010dc254900000000000000000000000000000000000000000000000000000000000000000000000000",
            "orderId": "0x966ee4b660b6fc81e337136e12c8c973b168f0aad33417a0b6cc3aaef7a633a0",
        },
        "scraper_function": "deposit",
    }

    normalised_doc = {
        "scraper_protocol": "dln",
        "scraper_originChain": "7565164",
        "scraper_blockNumber": 297150699,
        "scraper_blockTimestamp": 1729647729,
        "scraper_from": "C1m3LAwKiosA4qFhCTMwhFjXaajLuHJMypT75CAkiHuH",
        "scraper_contractAddress": "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4",
        "scraper_tx_status": "ok",
        "scraper_tx_hash": "3yTjWsfrWB6Xh48yh5Rqwi5REYysVNAGJpST1Z681YoJhtUxoYgRgwWrJtHoKw33xHXgPeF1pZEH6MS2T9c3JFG9",
        "scraper_chain_fee": 5003,
        "scraper_chain_prioritization_fee": 2,
        "scraper_function": "deposit",
    }

    normalised_doc = normalise_dln(tx_doc, "tx", normalised_doc)
    print(normalised_doc)
