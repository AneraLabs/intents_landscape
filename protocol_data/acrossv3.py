import json
import os

PROTOCOL_NAME = "acrossv3"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

with open(os.path.join(PARENT_DIR, "abis", "across_v3.json"), encoding="utf-8") as f:
    PROTOCOL_ABI = json.load(f)


CHAINS_TO_CONTRACTS = {
    "42161": {
        "deposit": {0: "0xe35e9842fceaCA96570B734083f4a58e8F7C5f2A"},
        "fill": {0: "0xe35e9842fceaCA96570B734083f4a58e8F7C5f2A"},
    },
    "8453": {
        "deposit": {0: "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"},
        "fill": {0: "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"},
    },
    "81457": {
        "deposit": {0: "0x2D509190Ed0172ba588407D4c2df918F955Cc6E1"},
        "fill": {0: "0x2D509190Ed0172ba588407D4c2df918F955Cc6E1"},
    },
    "1": {
        "deposit": {0: "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5"},
        "fill": {0: "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5"},
    },
    "59144": {
        "deposit": {0: "0x7E63A5f1a8F0B4d0934B2f2327DAED3F6bb2ee75"},
        "fill": {0: "0x7E63A5f1a8F0B4d0934B2f2327DAED3F6bb2ee75"},
    },
    "1135": {
        "deposit": {0: "0x9552a0a6624A23B848060AE5901659CDDa1f83f8"},
        "fill": {0: "0x9552a0a6624A23B848060AE5901659CDDa1f83f8"},
    },
    "34443": {
        "deposit": {0: "0x3baD7AD0728f9917d1Bf08af5782dCbD516cDd96"},
        "fill": {0: "0x3baD7AD0728f9917d1Bf08af5782dCbD516cDd96"},
    },
    "10": {
        "deposit": {0: "0x6f26Bf09B1C792e3228e5467807a900A503c0281"},
        "fill": {0: "0x6f26Bf09B1C792e3228e5467807a900A503c0281"},
    },
    "137": {
        "deposit": {0: "0x9295ee1d8C5b022Be115A2AD3c30C72E34e7F096"},
        "fill": {0: "0x9295ee1d8C5b022Be115A2AD3c30C72E34e7F096"},
    },
    "690": {
        "deposit": {0: "0x13fDac9F9b4777705db45291bbFF3c972c6d1d97"},
        "fill": {0: "0x13fDac9F9b4777705db45291bbFF3c972c6d1d97"},
    },
    "534352": {
        "deposit": {0: "0x3baD7AD0728f9917d1Bf08af5782dCbD516cDd96"},
        "fill": {0: "0x3baD7AD0728f9917d1Bf08af5782dCbD516cDd96"},
    },
    "324": {
        "deposit": {0: "0xE0B015E54d54fc84a6cB9B666099c46adE9335FF"},
        "fill": {0: "0xE0B015E54d54fc84a6cB9B666099c46adE9335FF"},
    },
    "7777777": {
        "deposit": {0: "0x13fDac9F9b4777705db45291bbFF3c972c6d1d97"},
        "fill": {0: "0x13fDac9F9b4777705db45291bbFF3c972c6d1d97"},
    },
    "41455": {
        "deposit": {0: "0x13fDac9F9b4777705db45291bbFF3c972c6d1d97"},
        "fill": {0: "0x13fDac9F9b4777705db45291bbFF3c972c6d1d97"},
    },
    "57073": {
        "deposit": {0: "0xeF684C38F94F48775959ECf2012D7E864ffb9dd4"},
        "fill": {0: "0xeF684C38F94F48775959ECf2012D7E864ffb9dd4"},
    },
    "480": {
        "deposit": {0: "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"},
        "fill": {0: "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"},
    },
}


def get_contract_address(chain_id, type):
    contracts = CHAINS_TO_CONTRACTS

    if chain_id in contracts:
        return contracts[chain_id][type]

    return None


def get_contract_abi(_chain_id, type):
    if type in {"deposit", "fill"}:
        return {0: PROTOCOL_ABI}

    return None


def get_supported_chains():
    return list(CHAINS_TO_CONTRACTS.keys())


def get_deposit_function_filter():
    return None


def get_deposit_event_filter():
    return {0: ["V3FundsDeposited"]}


def get_fill_function_filter():
    return {0: ["fillV3Relay"]}


def get_fill_event_filter():
    return {0: ["FilledV3Relay"]}
