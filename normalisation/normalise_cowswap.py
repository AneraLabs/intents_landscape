from normalisation.utils import normalise_address_if_needed


def normalise_cowswap(original_doc, type, normalised_doc):
    if type == "event":
        normalised_doc["name"] = "order_swap_event"
        normalised_doc["source_address"] = original_doc["event"]["owner"]
        normalised_doc["destination_address"] = original_doc["event"]["owner"]
        normalised_doc["source_chain"] = original_doc["scraper_originChain"]
        normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

        normalised_doc["source_token_address"] = normalise_address_if_needed(
            original_doc["event"]["sellToken"]
        )
        normalised_doc["destination_token_address"] = normalise_address_if_needed(
            original_doc["event"]["buyToken"]
        )
        normalised_doc["order_id"] = original_doc["event"]["orderUid"]

        normalised_doc["source_token_amount"] = original_doc["event"]["sellAmount"]
        normalised_doc["destination_token_amount"] = original_doc["event"]["buyAmount"]
        normalised_doc["filler_address"] = original_doc["scraper_from"]

        # Protocol fee is in source token
        normalised_doc["protocol_fee"] = int(original_doc["event"]["feeAmount"])

        if (
            "destination_token_address" in normalised_doc
            and normalised_doc["destination_token_address"]
            == "0x0000000000000000000000000000000000000000"
        ):
            # default route will be filled later - during matching
            normalised_doc.pop("destination_token_address")

    return normalised_doc
