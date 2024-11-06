import json

from normalisation.utils import safe_checksum_address

PROTOCOL_NAME = "nitro"


# https://sentry.lcd.routerprotocol.com/router-protocol/router-chain/multichain/contract_config
# choose VOYAGER addresses
NITRO_CHAIN_ID_TO_CONTRACT_ADDRESS = {
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
}


def get_contract_address(chain_id, _type):
    # Call by scraping logic to determine where to monitor for events
    address = safe_checksum_address(NITRO_CHAIN_ID_TO_CONTRACT_ADDRESS[chain_id])

    # 0 to ignore starting block timestamp
    result_doc = {0: address}

    return result_doc


def get_contract_abi(chain_id, type):
    contract_abi = json.loads(
        """[{"inputs":[{"internalType":"address","name":"_wrappedNativeTokenAddress","type":"address"},{"internalType":"address","name":"_gatewayContract","type":"address"},{"internalType":"address","name":"_usdcAddress","type":"address"},{"internalType":"address","name":"_tokenMessenger","type":"address"},{"internalType":"bytes","name":"_routerMiddlewareBase","type":"bytes"},{"internalType":"uint256","name":"_minGasThreshhold","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AmountTooLarge","type":"error"},{"inputs":[],"name":"InvalidAmount","type":"error"},{"inputs":[],"name":"InvalidFee","type":"error"},{"inputs":[],"name":"InvalidGateway","type":"error"},{"inputs":[],"name":"InvalidRefundData","type":"error"},{"inputs":[],"name":"InvalidRequestSender","type":"error"},{"inputs":[],"name":"MessageAlreadyExecuted","type":"error"},{"inputs":[],"name":"MessageExcecutionFailedWithLowGas","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pauser","type":"address"},{"indexed":false,"internalType":"uint256","name":"stakedAmount","type":"uint256"}],"name":"CommunityPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"feeAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"depositId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"eventNonce","type":"uint256"},{"indexed":false,"internalType":"bool","name":"initiatewithdrawal","type":"bool"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"}],"name":"DepositInfoUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"partnerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"destAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"depositId","type":"uint256"},{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"bytes","name":"recipient","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"destToken","type":"bytes"}],"name":"FundsDeposited","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"partnerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"destAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"depositId","type":"uint256"},{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"bytes","name":"recipient","type":"bytes"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"bytes","name":"destToken","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"message","type":"bytes"}],"name":"FundsDepositedWithMessage","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"messageHash","type":"bytes32"},{"indexed":false,"internalType":"address","name":"forwarder","type":"address"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"FundsPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"messageHash","type":"bytes32"},{"indexed":false,"internalType":"address","name":"forwarder","type":"address"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":false,"internalType":"bool","name":"execFlag","type":"bool"},{"indexed":false,"internalType":"bytes","name":"execData","type":"bytes"}],"name":"FundsPaidWithMessage","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"partnerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"usdcNonce","type":"uint256"},{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"bytes32","name":"recipient","type":"bytes32"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"}],"name":"iUSDCDeposited","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TRANSFER_SIZE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_GAS_THRESHHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PAUSER","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RESOURCE_SETTER","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"communityPause","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"depositNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"destDetails","outputs":[{"internalType":"uint32","name":"domainId","type":"uint32"},{"internalType":"uint256","name":"fee","type":"uint256"},{"internalType":"bool","name":"isSet","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"executeRecord","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"gatewayContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"partnerId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destAmount","type":"uint256"},{"internalType":"address","name":"srcToken","type":"address"},{"internalType":"address","name":"refundRecipient","type":"address"},{"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"}],"internalType":"struct IAssetForwarder.DepositData","name":"depositData","type":"tuple"},{"internalType":"bytes","name":"destToken","type":"bytes"},{"internalType":"bytes","name":"recipient","type":"bytes"}],"name":"iDeposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"srcToken","type":"address"},{"internalType":"uint256","name":"feeAmount","type":"uint256"},{"internalType":"uint256","name":"depositId","type":"uint256"},{"internalType":"bool","name":"initiatewithdrawal","type":"bool"}],"name":"iDepositInfoUpdate","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"partnerId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destAmount","type":"uint256"},{"internalType":"address","name":"srcToken","type":"address"},{"internalType":"address","name":"refundRecipient","type":"address"},{"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"}],"internalType":"struct IAssetForwarder.DepositData","name":"depositData","type":"tuple"},{"internalType":"bytes","name":"destToken","type":"bytes"},{"internalType":"bytes","name":"recipient","type":"bytes"},{"internalType":"bytes","name":"message","type":"bytes"}],"name":"iDepositMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"partnerId","type":"uint256"},{"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"internalType":"bytes32","name":"recipient","type":"bytes32"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"iDepositUSDC","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"requestSender","type":"string"},{"internalType":"bytes","name":"packet","type":"bytes"},{"internalType":"string","name":"","type":"string"}],"name":"iReceive","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainId","type":"bytes32"},{"internalType":"uint256","name":"depositId","type":"uint256"},{"internalType":"address","name":"destToken","type":"address"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IAssetForwarder.RelayData","name":"relayData","type":"tuple"}],"name":"iRelay","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainId","type":"bytes32"},{"internalType":"uint256","name":"depositId","type":"uint256"},{"internalType":"address","name":"destToken","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"bytes","name":"message","type":"bytes"}],"internalType":"struct IAssetForwarder.RelayDataMessage","name":"relayData","type":"tuple"}],"name":"iRelayMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"isCommunityPauseEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pauseStakeAmountMax","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauseStakeAmountMin","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"rescue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"routerMiddlewareBase","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_destChainIdBytes","type":"bytes32[]"},{"components":[{"internalType":"uint32","name":"domainId","type":"uint32"},{"internalType":"uint256","name":"fee","type":"uint256"},{"internalType":"bool","name":"isSet","type":"bool"}],"internalType":"struct IAssetForwarder.DestDetails[]","name":"_destDetails","type":"tuple[]"}],"name":"setDestDetails","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"toggleCommunityPause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"tokenMessenger","outputs":[{"internalType":"contract ITokenMessenger","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalStakedAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"address","name":"_gatewayContract","type":"address"},{"internalType":"bytes","name":"_routerMiddlewareBase","type":"bytes"},{"internalType":"uint256","name":"minPauseStakeAmount","type":"uint256"},{"internalType":"uint256","name":"maxPauseStakeAmount","type":"uint256"}],"name":"update","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenMessenger","type":"address"}],"name":"updateTokenMessenger","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"usdc","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdrawStakeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"wrappedNativeToken","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}]"""  # noqa: E501
    )

    # deposit and fill contracts may be the same for some protocols
    if type == "deposit":
        return {0: contract_abi}
    elif type == "fill":
        return {0: contract_abi}

    return None


def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return [
        "1",
        "534352",
        "324",
        "42161",
        "59144",
        "137",
        "81457",
        "10",
        "43114",
        "8453",
        "56",
        "1101",
        "5000",
        "169",
        "728126428",
        "288",
        "34443",
        "1088",
        "167000",
    ]


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
