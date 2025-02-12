from chains.chain_info import is_supported
from normalisation.normalise_acrossv2 import normalise_across_v2
from normalisation.normalise_acrossv3 import normalise_across_v3
from normalisation.normalise_cowswap import normalise_cowswap
from normalisation.normalise_dln import normalise_dln
from normalisation.normalise_nitro import normalise_nitro
from normalisation.normalise_rhinofi import normalise_rhinofi
from normalisation.normalise_synapse import normalise_synapse
from normalisation.utils import (
    bytes_as_hex_str,
    initialise_normalised_entry_with_common_values,
    safe_checksum_address,
)
from signal_handler import SignalHandler


def is_field_value_present(doc: dict, field: str) -> bool:
    if field not in doc or doc[field] is None:
        print(f"Test failed: mandatory field [{field}] missing")
        return False
    return True


def is_valid_normalised_doc(doc: dict) -> bool:
    is_valid = True

    # docs that fail normalisation but that is expected
    # we don't need to log errors about them
    if ("order_id" not in doc or doc["order_id"] is None) and (
        "scraper_tx_status" in doc and doc["scraper_tx_status"] != "ok"
    ):
        return False
    if "source_chain" in doc and not is_supported(str(doc["source_chain"])):
        return False
    if "destination_chain" in doc and not is_supported(str(doc["destination_chain"])):
        return False

    mandatory_fields = ["type", "name"]

    mandatory_fields_fill = [
        "destination_token_address",
        "destination_token_amount",
        "filler_address",
    ]
    mandatory_fields_deposit = ["source_token_address", "source_token_amount"]
    mandatory_fields_scraper = [
        "scraper_originChain",
        "scraper_blockNumber",
        "scraper_tx_hash",
        "scraper_blockTimestamp",
        "scraper_protocol",
        "scraper_from",
    ]

    # modify mandatory fields for protocols if needed
    if doc["scraper_protocol"] == "nitro":
        mandatory_fields_fill = ["filler_address"]
        mandatory_fields_deposit = []
        mandatory_fields_scraper.append("scraper_contractAddress")
    elif doc["scraper_protocol"] == "rhinofi":
        mandatory_fields_fill = [
            "destination_address",
            "destination_chain",
            "destination_token_address",
            "destination_token_amount",
            "filler_address",
        ]
        mandatory_fields_deposit = [
            "source_address",
            "source_chain",
            "source_token_address",
            "source_token_amount",
        ]

    for field in mandatory_fields:
        if not is_field_value_present(doc, field):
            is_valid = False

    if doc["name"] in {"order_fill_tx", "order_fill_event", "order_swap_event"}:
        for field in mandatory_fields_fill:
            if not is_field_value_present(doc, field):
                is_valid = False
    elif doc["name"] in {"order_deposit_tx", "order_deposit_event", "order_swap_event"}:
        for field in mandatory_fields_deposit:
            if not is_field_value_present(doc, field):
                is_valid = False
    else:
        print(f"Test failed: mandatory field name has invalid value: [{doc['name']}]")
        is_valid = False

    if doc["type"] not in {"tx", "event"}:
        print(f"Test failed: mandatory field type has invalid value: [{doc['type']}]")
        is_valid = False

    for field in mandatory_fields_scraper:
        if not is_field_value_present(doc, field):
            is_valid = False

    if not is_valid:
        print(f"Normalised doc failed validation (see errors above), doc: [{doc}]")

    return is_valid


def normalise(doc: dict, _signal_handler: SignalHandler) -> dict | None:
    type = None
    if "scraper_event" in doc:
        type = "event"
    elif "scraper_function" in doc:
        type = "tx"
    else:
        print(f"Unknown type record {doc}, unable to parse!")
        return None

    normalised_doc = initialise_normalised_entry_with_common_values(doc, type)

    protocol = doc["scraper_protocol"]
    if protocol == "acrossv2":
        normalised_doc = normalise_across_v2(doc, type, normalised_doc)
    elif protocol == "acrossv3":
        normalised_doc = normalise_across_v3(doc, type, normalised_doc)
    elif protocol == "nitro":
        normalised_doc = normalise_nitro(doc, type, normalised_doc)
    elif protocol == "dln":
        normalised_doc = normalise_dln(doc, type, normalised_doc)
    elif protocol == "synapse":
        normalised_doc = normalise_synapse(doc, type, normalised_doc)
    elif protocol == "rhinofi":
        normalised_doc = normalise_rhinofi(doc, type, normalised_doc)
    elif protocol == "cowswap":
        normalised_doc = normalise_cowswap(doc, type, normalised_doc)
    else:
        print(f"Unabled to process protocol [{protocol}]")
        return None

    if normalised_doc is not None:

        def checksum_address(address_key):
            if address_key in normalised_doc:
                normalised_doc[address_key] = safe_checksum_address(
                    normalised_doc[address_key]
                )

        checksum_address("scraper_contractAddress")
        checksum_address("source_token_address")
        checksum_address("destination_token_address")
        checksum_address("source_address")
        checksum_address("destination_address")
        checksum_address("filler_address")

        bytes_as_hex_str(normalised_doc)

        if not is_valid_normalised_doc(normalised_doc):
            return None

    return normalised_doc


if __name__ == "__main__":
    import json

    def read_json_file(file_path):
        with open(file_path, encoding="utf-8") as file:
            return json.load(file)

    signal_handler = SignalHandler()
    for doc in read_json_file("normalisation/example_source_docs/events.json"):
        normalised_doc = normalise(doc, signal_handler)
        print(json.dumps(normalised_doc, indent=4))
