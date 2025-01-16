import json
import os

from normalisation.utils import safe_checksum_address

PROTOCOL_NAME = "nitro"


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

with open(os.path.join(PARENT_DIR, "abis", "nitro.json"), encoding="utf-8") as f:
    PROTOCOL_ABI = json.load(f)

# https://sentry.lcd.routerprotocol.com/router-protocol/router-chain/multichain/contract_config
# choose VOYAGER addresses
CHAINS_TO_CONTRACTS = {
    "1": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "10": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
    "1088": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "1101": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "1313161554": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "137": "0x1396F41d89b96Eaf29A7Ef9EE01ad36E452235aE",
    "167000": "0x7BD616192fB2B364f9d29B2026165281a5f2ff2F",
    "169": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "196": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "1997": "0xF0773508C585246BD09BfB401Aa18B72685b03F9",
    "2000": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "200901": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "2040": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "23294": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "250": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "288": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "30": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "324": "0x39eed28843281B17215cB2aCCaA3d4475713E8cd",
    "34443": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "42161": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "43114": "0x140BD2e8332E02171e1235a3677044602E48254f",
    "5000": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
    "534352": "0x01B4CE0d48Ce91eB6bcaf5dB33870C65d641b894",
    "56": "0x260687eBC6C55DAdd578264260f9f6e968f7B2A5",
    "570": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "5845": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "59144": "0x8C4aCd74Ff4385f3B7911432FA6787Aa14406f8B",
    "698": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "7225878": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "728126428": "0x500F531D11C04C604E6EC7c7E381ceEC2277a2Cf",
    "81457": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "8453": "0x0Fa205c0446cD9EeDCc7538c9E24BC55AD08207f",
    "995": "0x7BD616192fB2B364f9d29B2026165281a5f2ff2F",
    "4061": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "1689": "0x21c1E74CAaDf990E237920d5515955a024031109",
    "151": "0xF0773508C585246BD09BfB401Aa18B72685b03F9",
}


def get_contract_address(chain_id, _type):
    # Call by scraping logic to determine where to monitor for events
    address = safe_checksum_address(CHAINS_TO_CONTRACTS[chain_id])

    # 0 to ignore starting block timestamp
    result_doc = {0: address}

    return result_doc


def get_contract_abi(_chain_id, type):
    if type in {"deposit", "fill"}:
        return {0: PROTOCOL_ABI}

    return None


def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return list(CHAINS_TO_CONTRACTS.keys())


def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None


def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return {0: ["FundsDeposited", "FundsDepositedWithMessage"]}


def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a
    # fill event filter will not result in reverted txs being picked up
    return {0: ["iRelay", "iRelayMessage"]}


def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return {0: ["FundsPaid", "FundsPaidWithMessage"]}
