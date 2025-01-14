import json
import os

PROTOCOL_NAME = "synapse"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

with open(os.path.join(PARENT_DIR, "abis", "synapse.json"), encoding="utf-8") as f:
    PROTOCOL_ABI = json.load(f)


def get_contract_address(chain_id, type):
    # Call by scraping logic to determine where to monitor for events
    # Synapse FASTBRIDGE_CONTRACTS, source:
    # https://github.com/synapsecns/sanguine/blob/2f452875d88c95505cb491cff2f64a46b7d7e497/packages/synapse-constants/constants/chains/index.ts#L121
    contracts = {
        "42161": {
            "deposit": {
                0: "0x6C0771aD91442D670159a8171C35F4828E19aFd2",
                189700328: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
            "fill": {
                0: "0x6C0771aD91442D670159a8171C35F4828E19aFd2",
                189700328: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
        },
        "1": {
            "deposit": {
                0: "0x4983DB49336fD4f95e864aB6DA9135e057EF0be1",
                19421323: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
            "fill": {
                0: "0x4983DB49336fD4f95e864aB6DA9135e057EF0be1",
                19421323: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
        },
        "10": {
            "deposit": {
                0: "0x6C0771aD91442D670159a8171C35F4828E19aFd2",
                117334308: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
            "fill": {
                0: "0x6C0771aD91442D670159a8171C35F4828E19aFd2",
                117334308: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
        },
        "534352": {
            "deposit": {5124895: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E"},
            "fill": {5124895: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E"},
        },
        "8453": {
            "deposit": {
                12478103: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
            "fill": {
                12478103: "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
            },
        },
    }

    return contracts[chain_id][type]


def get_contract_abi(_chain_id, type):
    # deposit and fill contracts may be the same for some protocols
    if type in {"deposit", "fill"}:
        return {0: PROTOCOL_ABI}
    return None


def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return ["42161", "534352", "1", "10", "8453"]


def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None


def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return {0: ["BridgeRequested"]}


def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a
    # fill event filter will not result in reverted txs being picked up
    return {0: ["relay"]}


def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return {0: ["BridgeRelayed"]}
