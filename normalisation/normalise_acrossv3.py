from normalisation.utils import normalise_address_if_needed


def normalise_across_v3(original_doc, type, normalised_doc):
    if type == "tx":
        if original_doc["scraper_function"] != "fillV3Relay":
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None
        normalised_doc["name"] = "order_fill_tx"

        normalised_doc["source_address"] = original_doc["tx"]["relayData"]["depositor"]
        normalised_doc["destination_address"] = original_doc["tx"]["relayData"][
            "recipient"
        ]

        normalised_doc["source_chain"] = original_doc["tx"]["relayData"][
            "originChainId"
        ]
        normalised_doc["destination_chain"] = int(normalised_doc["scraper_originChain"])

        normalised_doc["source_token_address"] = normalise_address_if_needed(
            original_doc["tx"]["relayData"]["inputToken"]
        )
        normalised_doc["destination_token_address"] = normalise_address_if_needed(
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
        if original_doc["scraper_event"] == "V3FundsDeposited":
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_address"] = original_doc["event"]["depositor"]
            normalised_doc["destination_address"] = original_doc["event"]["recipient"]

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = original_doc["event"][
                "destinationChainId"
            ]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["inputToken"]
            )
            normalised_doc["destination_token_address"] = normalise_address_if_needed(
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

        elif original_doc["scraper_event"] == "FilledV3Relay":
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["source_address"] = original_doc["event"]["depositor"]
            # Note there is a relayExecutionInfo.updatedRecipient,
            #  we should check how this is used..
            normalised_doc["destination_address"] = original_doc["event"]["recipient"]

            normalised_doc["source_chain"] = original_doc["event"]["originChainId"]
            normalised_doc["destination_chain"] = int(
                normalised_doc["scraper_originChain"]
            )

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["inputToken"]
            )
            normalised_doc["destination_token_address"] = normalise_address_if_needed(
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


if __name__ == "__main__":
    tx = {
        "scraper_function": "fillV3Relay",
    }
    print(normalise_across_v3(tx, "tx", {}))
