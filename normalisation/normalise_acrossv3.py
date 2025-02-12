from normalisation.utils import normalise_address_if_needed
from protocol_data.acrossv3 import (
    get_deposit_event_filter,
    get_fill_event_filter,
    get_fill_function_filter,
)


def normalise_address(address):
    # after update the addresses are now longer
    # https://docs.across.to/introduction/migration-guides/migration-guide-for-non-evm-and-prefills/breaking-changes-for-indexers
    # we assume that all chains are evm chains
    # (we do not track non-evm chains for across atm)

    address = normalise_address_if_needed(address)

    if len(address) == 42:  # noqa: PLR2004
        return address

    return "0x" + address[-40:]


def normalise_across_v3(original_doc, type, normalised_doc):
    if type == "tx":
        if original_doc["scraper_function"] not in get_fill_function_filter()[0]:
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None
        normalised_doc["name"] = "order_fill_tx"

        normalised_doc["source_address"] = normalise_address(
            original_doc["tx"]["relayData"]["depositor"]
        )
        normalised_doc["destination_address"] = normalise_address(
            original_doc["tx"]["relayData"]["recipient"]
        )

        normalised_doc["source_chain"] = original_doc["tx"]["relayData"][
            "originChainId"
        ]
        normalised_doc["destination_chain"] = int(normalised_doc["scraper_originChain"])

        normalised_doc["source_token_address"] = normalise_address(
            original_doc["tx"]["relayData"]["inputToken"]
        )
        normalised_doc["destination_token_address"] = normalise_address(
            original_doc["tx"]["relayData"]["outputToken"]
        )

        normalised_doc["source_token_amount"] = original_doc["tx"]["relayData"][
            "inputAmount"
        ]
        normalised_doc["destination_token_amount"] = original_doc["tx"]["relayData"][
            "outputAmount"
        ]

        normalised_doc["order_id"] = (
            str(normalised_doc["source_chain"])
            + "_"
            + str(original_doc["tx"]["relayData"]["depositId"])
        )
        normalised_doc["protocol_fee"] = int(
            normalised_doc["source_token_amount"]
        ) - int(normalised_doc["destination_token_amount"])

        normalised_doc["filler_address"] = original_doc["scraper_from"]

    elif type == "event":
        if original_doc["scraper_event"] in get_deposit_event_filter()[0]:
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_address"] = normalise_address(
                original_doc["event"]["depositor"]
            )
            normalised_doc["destination_address"] = normalise_address(
                original_doc["event"]["recipient"]
            )

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = original_doc["event"][
                "destinationChainId"
            ]

            normalised_doc["source_token_address"] = normalise_address(
                original_doc["event"]["inputToken"]
            )
            normalised_doc["destination_token_address"] = normalise_address(
                original_doc["event"]["outputToken"]
            )

            normalised_doc["source_token_amount"] = original_doc["event"]["inputAmount"]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "outputAmount"
            ]

            # TODO double check that this is safe, is there a token swap happening?
            normalised_doc["protocol_fee"] = int(
                original_doc["event"]["inputAmount"]
            ) - int(original_doc["event"]["outputAmount"])

        elif original_doc["scraper_event"] in get_fill_event_filter()[0]:
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["source_address"] = normalise_address(
                original_doc["event"]["depositor"]
            )
            # Note there is a relayExecutionInfo.updatedRecipient,
            #  we should check how this is used..
            normalised_doc["destination_address"] = normalise_address(
                original_doc["event"]["recipient"]
            )

            normalised_doc["source_chain"] = original_doc["event"]["originChainId"]
            normalised_doc["destination_chain"] = int(
                normalised_doc["scraper_originChain"]
            )

            normalised_doc["source_token_address"] = normalise_address(
                original_doc["event"]["inputToken"]
            )
            normalised_doc["destination_token_address"] = normalise_address(
                original_doc["event"]["outputToken"]
            )

            normalised_doc["source_token_amount"] = original_doc["event"]["inputAmount"]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "outputAmount"
            ]

            # TODO double check that this is safe, is there a token swap happening?
            normalised_doc["protocol_fee"] = int(
                original_doc["event"]["inputAmount"]
            ) - int(original_doc["event"]["outputAmount"])

            # Ideally we'd use the value in original_doc['event']['relayer'],
            # however this would be inconsistent with txs
            # which do not expose this. Without looking at the inner txs
            # the originating EOA is the best we can do for now
            normalised_doc["filler_address"] = original_doc["scraper_from"]
        else:
            print(f"Unknown event type {original_doc['scraper_event']}")
            return None

        normalised_doc["order_id"] = (
            str(normalised_doc["source_chain"])
            + "_"
            + str(original_doc["event"]["depositId"])
        )

    if (
        "destination_token_address" in normalised_doc
        and normalised_doc["destination_token_address"]
        == "0x0000000000000000000000000000000000000000"
    ):
        # default route will be filled later - during matching
        normalised_doc.pop("destination_token_address")

    return normalised_doc


# ruff: noqa: E501
if __name__ == "__main__":
    from normalisation.utils import initialise_normalised_entry_with_common_values

    tx = {
        "_id": {
            "protocol": "acrossv3",
            "origin_chain_id": "81457",
            "tx_hash": "bdd353286ed9c714d4e811520e525899d6458235b4e6f357b613a7fac6848600",
            "order_id": "3058809",
        },
        "scraper_originChain": "81457",
        "scraper_blockNumber": 15266538,
        "scraper_blockTimestamp": 1739342891,
        "scraper_from": "0x41ee28EE05341E7fdDdc8d433BA66054Cd302cA1",
        "scraper_to": "0x2D509190Ed0172ba588407D4c2df918F955Cc6E1",
        "scraper_protocol": "acrossv3",
        "scraper_contractAddress": "0x2D509190Ed0172ba588407D4c2df918F955Cc6E1",
        "scraper_function": "fillRelay",
        "scraper_effectiveGasPrice": "27649679",
        "scraper_gasUsed": "146771",
        "scraper_tx_status": "ok",
        "scraper_tx_hash": "bdd353286ed9c714d4e811520e525899d6458235b4e6f357b613a7fac6848600",
        "tx": {
            "relayData": {
                "depositor": "0x00000000000000000000000025c77c01a5d96a6d9538022f3d8cffb211f6b899",
                "recipient": "0x00000000000000000000000025c77c01a5d96a6d9538022f3d8cffb211f6b899",
                "exclusiveRelayer": "0x0000000000000000000000000000000000000000000000000000000000000000",
                "inputToken": "0x00000000000000000000000082af49447d8a07e3bd95bd0d56f35241523fbab1",
                "outputToken": "0x0000000000000000000000004300000000000000000000000000000000000004",
                "inputAmount": "200000000000000000",
                "outputAmount": "199961290449457525",
                "originChainId": "42161",
                "depositId": "3058809",
                "fillDeadline": "4294967295",
                "exclusivityDeadline": "0",
                "message": "0x",
            },
            "repaymentChainId": "42161",
            "repaymentAddress": "0x00000000000000000000000041ee28ee05341e7fdddc8d433ba66054cd302ca1",
        },
    }
    pre_filled = initialise_normalised_entry_with_common_values(tx, "tx")
    print(normalise_across_v3(tx, "tx", pre_filled))
