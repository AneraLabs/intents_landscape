import json
import os

from solders.rpc.responses import GetTransactionResp
from solders.transaction_status import UiPartiallyDecodedInstruction

from anchor_clients.rhinofi.instructions.deposit import layout as deposit_layout
from anchor_clients.rhinofi.instructions.withdraw import layout as withdraw_layout
from protocol_data.solana_parser import BaseSolanaParser, Parseable

PROTOCOL_NAME = "rhinofi"
DEPOSIT_SOLANA_PROGRAM_ID = "FCW1uBM3pZ7fQWvEL9sxTe4fNiH41bu9DWX4ErTZ6aMq"
FILL_SOLANA_PROGRAM_ID = "FCW1uBM3pZ7fQWvEL9sxTe4fNiH41bu9DWX4ErTZ6aMq"

CHAINS_TO_CONTRACTS = {
    # ethereum is not clear, there is no bridge contract
    # there is a deposit contract but no fill contract
    # "1": {
    #     "deposit": {0: "0xc3CA38091061e3E5358A52d74730F16C60cA9c26"},
    #     "fill": {0: "0xc3CA38091061e3E5358A52d74730F16C60cA9c26"},
    # },
    "7565164": {
        "deposit": DEPOSIT_SOLANA_PROGRAM_ID,
        "fill": FILL_SOLANA_PROGRAM_ID,
    },
    "42161": {
        "deposit": {12062072: "0x10417734001162Ea139e8b044DFe28DbB8B28ad0"},
        "fill": {12062072: "0x10417734001162Ea139e8b044DFe28DbB8B28ad0"},
    },
    "56": {
        "deposit": {21550595: "0xB80A582fa430645A043bB4f6135321ee01005fEf"},
        "fill": {21550595: "0xB80A582fa430645A043bB4f6135321ee01005fEf"},
    },
    "137": {
        "deposit": {16917268: "0xBA4EEE20F434bC3908A0B18DA496348657133A7E"},
        "fill": {16917268: "0xBA4EEE20F434bC3908A0B18DA496348657133A7E"},
    },
    "324": {
        "deposit": {193: "0x1fa66e2B38d0cC496ec51F81c3e05E6A6708986F"},
        "fill": {193: "0x1fa66e2B38d0cC496ec51F81c3e05E6A6708986F"},
    },
    "1101": {
        "deposit": {15845: "0x65A4b8A0927c7FD899aed24356BF83810f7b9A3f"},
        "fill": {15845: "0x65A4b8A0927c7FD899aed24356BF83810f7b9A3f"},
    },
    "10": {
        "deposit": {96888536: "0x0bCa65bf4b4c8803d2f0B49353ed57CAAF3d66Dc"},
        "fill": {96888536: "0x0bCa65bf4b4c8803d2f0B49353ed57CAAF3d66Dc"},
    },
    "59144": {
        "deposit": {593: "0xcF68a2721394dcf5dCF66F6265C1819720F24528"},
        "fill": {593: "0xcF68a2721394dcf5dCF66F6265C1819720F24528"},
    },
    "8453": {
        "deposit": {1448656: "0x2f59E9086ec8130E21BD052065a9E6B2497bb102"},
        "fill": {1448656: "0x2f59E9086ec8130E21BD052065a9E6B2497bb102"},
    },
    "169": {
        "deposit": {21324: "0x2B4553122D960CA98075028d68735cC6b15DeEB5"},
        "fill": {21324: "0x2B4553122D960CA98075028d68735cC6b15DeEB5"},
    },
    "534352": {
        "deposit": {694: "0x87627c7E586441EeF9eE3C28B66662e897513f33"},
        "fill": {694: "0x87627c7E586441EeF9eE3C28B66662e897513f33"},
    },
    "43114": {
        "deposit": {0: "0x5e023c31E1d3dCd08a1B3e8c96f6EF8Aa8FcaCd1"},
        "fill": {0: "0x5e023c31E1d3dCd08a1B3e8c96f6EF8Aa8FcaCd1"},
    },
    "146": {
        "deposit": {0: "0x5e023c31E1d3dCd08a1B3e8c96f6EF8Aa8FcaCd1"},
        "fill": {0: "0x5e023c31E1d3dCd08a1B3e8c96f6EF8Aa8FcaCd1"},
    },
    "5000": {
        "deposit": {0: "0x5e023c31e1d3dcd08a1b3e8c96f6ef8aa8fcacd1"},
        "fill": {0: "0x5e023c31E1d3dCd08a1B3e8c96f6EF8Aa8FcaCd1"},
    },
    "34443": {
        "deposit": {0: "0x5e023c31e1d3dcd08a1b3e8c96f6ef8aa8fcacd1"},
        "fill": {0: "0x5e023c31E1d3dCd08a1B3e8c96f6EF8Aa8FcaCd1"},
    },
    "167000": {
        "deposit": {0: "0x1Df2De291F909baA50C1456C87C71Edf9Fb199D5"},
        "fill": {0: "0x1Df2De291F909baA50C1456C87C71Edf9Fb199D5"},
    },
}

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(
    os.path.join(current_dir, "..", "abis", "rhinofi.json"), encoding="utf-8"
) as f:
    ETHEREUM_ABI = json.load(f)


def get_contract_address(chain_id, type):
    return CHAINS_TO_CONTRACTS[chain_id][type]


def get_contract_abi(chain_id, type):
    contract_abi = ETHEREUM_ABI

    # deposit and fill contracts may be the same for some protocols
    if type == "deposit":
        return {0: contract_abi}
    elif type == "fill":
        return {0: contract_abi}

    return None


def get_supported_chains():
    return list(CHAINS_TO_CONTRACTS.keys())


def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None


def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return {0: ["BridgedDeposit"]}


def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a
    # fill event filter will not result in reverted txs being picked up
    # TODO: verify rhino.fi does not have any not-successful fills, because
    # there is only one filler and it gets the funds from pre-filled pools, related discord chat:
    # https://discord.com/channels/745570257808130058/745571091438764062/1265924362276438108
    return {0: []}


def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return {
        0: [
            "BridgedWithdrawal",
            "BridgedWithdrawalWithData",
            "BridgedWithdrawalWithNative",
        ]
    }


# --------------------- Solana ----------------------------
DEPOSIT_IDENTIFIER = b"\xf2#\xc6\x89R\xe1\xf2\xb6"
FILL_IDENTIFIER = b'\xb7\x12F\x9c\x94m\xa1"'


class RhinoFiSchema(Parseable):
    def parse(self, data: bytes) -> dict:  # noqa: PLR6301
        identifier = data[:8]
        if identifier == DEPOSIT_IDENTIFIER:
            decoded = deposit_layout.parse(data[8:])
            return {
                "instruction": "deposit",
                "amount": str(decoded.amount),
                "eth_address_upper": str(decoded.eth_address_upper),
                "eth_address_lower": str(decoded.eth_address_lower),
            }
        elif identifier == FILL_IDENTIFIER:
            decoded = withdraw_layout.parse(data[8:])
            return {
                "instruction": "withdraw",
                "amount": str(decoded.amount),
            }
        else:
            raise ValueError(f"Unknown instruction: [{identifier.hex()}]")


class RhinoFiParser(BaseSolanaParser):
    @property
    def protocol_name(self) -> str:
        return PROTOCOL_NAME

    @property
    def program_address(self) -> str:
        return DEPOSIT_SOLANA_PROGRAM_ID

    @property
    def schema(self) -> Parseable:
        return RhinoFiSchema()

    def parse_protocol_specific_fields(  # noqa: PLR6301
        self,
        tx: GetTransactionResp,
        instruction: UiPartiallyDecodedInstruction,
        parsed_instruction_data: dict,
        doc: dict,
    ):
        doc["tx"] = parsed_instruction_data
        doc["scraper_function"] = doc["tx"]["instruction"]

        if doc["tx"]["instruction"] == "deposit":
            doc["source_address"] = str(instruction.accounts[3])
            doc["source_chain"] = doc["scraper_originChain"]
            doc["source_token_address"] = str(instruction.accounts[4])
        else:
            # fill
            doc["destination_address"] = str(instruction.accounts[4])
            doc["destination_chain"] = doc["scraper_originChain"]
            doc["destination_token_address"] = str(instruction.accounts[6])
            doc["filler_address"] = str(instruction.accounts[9])
        return doc


def get_solana_parsers() -> list[BaseSolanaParser]:
    return [RhinoFiParser()]


# ruff: noqa: E501
if __name__ == "__main__":
    # a simple test for dln solana parser
    from solana.rpc.api import Client
    from solders.pubkey import Pubkey

    parsers = get_solana_parsers()
    chain_id = "7565164"

    rpc_url = "https://api.mainnet-beta.solana.com"

    client = Client(rpc_url)

    for parser in parsers:
        pubkey = Pubkey.from_string(parser.program_address)
        tx_status_with_signatures = client.get_signatures_for_address(
            pubkey, limit=20
        ).value
        for tx_status in tx_status_with_signatures:
            signature = tx_status.signature
            tx = client.get_transaction(
                signature, max_supported_transaction_version=1, encoding="jsonParsed"
            )
            result = parser.parse_transaction(chain_id, signature, tx)
            print(json.dumps(result, indent=4))
            print()

        # # fill
        # signatures = [
        #     Signature.from_string(
        # 'W4F2LwF45ThfeBikqtsb3ahte1X25HWrX2Et43AKgBSS8zCqWmdYU1mEhXwuDUs5EJUFuGhYrm5TR74ibX8BHY4')
        # ]

        # for signature in signatures:
        #     tx = client.get_transaction(signature, max_supported_transaction_version=1,
        # encoding="jsonParsed")
        #     result = parser.parse_transaction(chain_id, signature, tx)
        #     print(json.dumps(result, indent=4))
        #     print()
