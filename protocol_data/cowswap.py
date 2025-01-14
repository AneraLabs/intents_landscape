import json
import os

PROTOCOL_NAME = "cowswap"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

with open(os.path.join(PARENT_DIR, "abis", "cowswap.json"), encoding="utf-8") as f:
    PROTOCOL_ABI = json.load(f)


def get_contract_address(chain_id, type):
    contracts = {
        "1": {
            "deposit": {0: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"},
            "fill": {0: "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"},
        }
    }
    return contracts[chain_id][type]


def get_contract_abi(_chain_id, type):
    if type in {"deposit", "fill"}:
        return {0: PROTOCOL_ABI}

    return None


def get_supported_chains():
    # Todo : Support other chains
    return ["1"]


def get_deposit_function_filter():
    return None


def get_deposit_event_filter():
    return {0: ["Trade"]}


def get_fill_function_filter():
    return None


def get_fill_event_filter():
    return {0: ["Trade"]}
