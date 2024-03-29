import json

PROTOCOL_NAME = "nitro"

def get_contract_address(chain_id, type):
    # Call by scraping logic to determine where to monitor for events
    contracts = {
        '1': {
            'deposit': {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
            'fill':  {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
        }, 
        '534352': {
            'deposit': {
                0 : '0x01B4CE0d48Ce91eB6bcaf5dB33870C65d641b894',
            },
            'fill':  {
                0 : '0x01B4CE0d48Ce91eB6bcaf5dB33870C65d641b894',
            },
        }, 
        '324': {
            'deposit': {
                0 : '0x8B6f1C18c866f37e6EA98AA539e0C117E70178a2',
            },
            'fill':  {
                0 : '0x8B6f1C18c866f37e6EA98AA539e0C117E70178a2',
            },
        }, 
        '42161': {
            'deposit': {
                0 : '0xEF300Fb4243a0Ff3b90C8cCfa1264D78182AdaA4',
            },
            'fill':  {
                0 : '0xEF300Fb4243a0Ff3b90C8cCfa1264D78182AdaA4',
            },
        }, 
        '59144': {
            'deposit': {
                0 : '0x8C4aCd74Ff4385f3B7911432FA6787Aa14406f8B',
            },
            'fill':  {
                0 : '0x8C4aCd74Ff4385f3B7911432FA6787Aa14406f8B',
            },
        }, 
        '137': {
            'deposit': {
                0 : '0x1396F41d89b96Eaf29A7Ef9EE01ad36E452235aE',
            },
            'fill':  {
                0 : '0x1396F41d89b96Eaf29A7Ef9EE01ad36E452235aE',
            },
        }, 
        '81457': {
            'deposit': {
                0 : '0x21c1E74CAaDf990E237920d5515955a024031109',
            },
            'fill':  {
                0 : '0x21c1E74CAaDf990E237920d5515955a024031109',
            },
        }, 
        '10': {
            'deposit': {
                0 : '0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06',
            },
            'fill':  {
                0 : '0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06',
            },
        }, 
        '43114': {
            'deposit': {
                0 : '0xF9f4C3dC7ba8f56737a92d74Fd67230c38AF51f2',
            },
            'fill':  {
                0 : '0xF9f4C3dC7ba8f56737a92d74Fd67230c38AF51f2',
            },
        }, 
        '8453': {
            'deposit': {
                0 : '0x0Fa205c0446cD9EeDCc7538c9E24BC55AD08207f',
            },
            'fill':  {
                0 : '0x0Fa205c0446cD9EeDCc7538c9E24BC55AD08207f',
            },
        }, 
        '56': {
            'deposit': {
                0 : '0x260687eBC6C55DAdd578264260f9f6e968f7B2A5',
            },
            'fill':  {
                0 : '0x260687eBC6C55DAdd578264260f9f6e968f7B2A5',
            },
        }, 
        '1101': {
            'deposit': {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
            'fill':  {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
        }, 
        '5000': {
            'deposit': {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
            'fill':  {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
        }, 
        '169': {
            'deposit': {
                0 : '0x21c1E74CAaDf990E237920d5515955a024031109',
            },
            'fill':  {
                0 : '0x21c1E74CAaDf990E237920d5515955a024031109',
            },
        }, 
        '30': {
            'deposit': {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
            'fill':  {
                0 : '0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9',
            },
        }, 
        '728126428': {
            'deposit': {
                0 : '0x9D25B8289c0f3789237c1b3a88264882eeD6c610',
            },
            'fill':  {
                0 : '0x9D25B8289c0f3789237c1b3a88264882eeD6c610',
            },
        },
        '288': {
            'deposit': {
                0: '0xc21e4ebd1d92036cb467b53fe3258f219d909eb9'
            },
            'fill':  {
                0 : '0xc21e4ebd1d92036cb467b53fe3258f219d909eb9',
            },
        },
        '34443': {
            'deposit': {
                0: '0xc21e4ebd1d92036cb467b53fe3258f219d909eb9'
            },
            'fill':  {
                0 : '0xc21e4ebd1d92036cb467b53fe3258f219d909eb9',
            },
        }, 
        '1088': {
            'deposit': {
                0: '0xc21e4ebd1d92036cb467b53fe3258f219d909eb9'
            },
            'fill':  {
                0 : '0xc21e4ebd1d92036cb467b53fe3258f219d909eb9',
            },
        }
    }

    return contracts[chain_id][type]

def get_contract_abi(chain_id, type):
    contract_abi = json.loads("""[{"inputs":[{"internalType":"address","name":"_wrappedNativeTokenAddress","type":"address"},{"internalType":"address","name":"_gatewayContract","type":"address"},{"internalType":"address","name":"_usdcAddress","type":"address"},{"internalType":"address","name":"_tokenMessenger","type":"address"},{"internalType":"bytes","name":"_routerMiddlewareBase","type":"bytes"},{"internalType":"uint256","name":"_minGasThreshhold","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AmountTooLarge","type":"error"},{"inputs":[],"name":"InvalidAmount","type":"error"},{"inputs":[],"name":"InvalidFee","type":"error"},{"inputs":[],"name":"InvalidGateway","type":"error"},{"inputs":[],"name":"InvalidRefundData","type":"error"},{"inputs":[],"name":"InvalidRequestSender","type":"error"},{"inputs":[],"name":"MessageAlreadyExecuted","type":"error"},{"inputs":[],"name":"MessageExcecutionFailedWithLowGas","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pauser","type":"address"},{"indexed":false,"internalType":"uint256","name":"stakedAmount","type":"uint256"}],"name":"CommunityPaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"feeAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"depositId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"eventNonce","type":"uint256"},{"indexed":false,"internalType":"bool","name":"initiatewithdrawal","type":"bool"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"}],"name":"DepositInfoUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"partnerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"destAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"depositId","type":"uint256"},{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"bytes","name":"recipient","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"destToken","type":"bytes"}],"name":"FundsDeposited","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"partnerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"destAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"depositId","type":"uint256"},{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"bytes","name":"recipient","type":"bytes"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"bytes","name":"destToken","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"message","type":"bytes"}],"name":"FundsDepositedWithMessage","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"messageHash","type":"bytes32"},{"indexed":false,"internalType":"address","name":"forwarder","type":"address"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"FundsPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"messageHash","type":"bytes32"},{"indexed":false,"internalType":"address","name":"forwarder","type":"address"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":false,"internalType":"bool","name":"execFlag","type":"bool"},{"indexed":false,"internalType":"bytes","name":"execData","type":"bytes"}],"name":"FundsPaidWithMessage","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"partnerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"usdcNonce","type":"uint256"},{"indexed":false,"internalType":"address","name":"srcToken","type":"address"},{"indexed":false,"internalType":"bytes32","name":"recipient","type":"bytes32"},{"indexed":false,"internalType":"address","name":"depositor","type":"address"}],"name":"iUSDCDeposited","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TRANSFER_SIZE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_GAS_THRESHHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PAUSER","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RESOURCE_SETTER","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"communityPause","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"depositNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"destDetails","outputs":[{"internalType":"uint32","name":"domainId","type":"uint32"},{"internalType":"uint256","name":"fee","type":"uint256"},{"internalType":"bool","name":"isSet","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"executeRecord","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"gatewayContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"partnerId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destAmount","type":"uint256"},{"internalType":"address","name":"srcToken","type":"address"},{"internalType":"address","name":"refundRecipient","type":"address"},{"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"}],"internalType":"struct IAssetForwarder.DepositData","name":"depositData","type":"tuple"},{"internalType":"bytes","name":"destToken","type":"bytes"},{"internalType":"bytes","name":"recipient","type":"bytes"}],"name":"iDeposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"srcToken","type":"address"},{"internalType":"uint256","name":"feeAmount","type":"uint256"},{"internalType":"uint256","name":"depositId","type":"uint256"},{"internalType":"bool","name":"initiatewithdrawal","type":"bool"}],"name":"iDepositInfoUpdate","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"partnerId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destAmount","type":"uint256"},{"internalType":"address","name":"srcToken","type":"address"},{"internalType":"address","name":"refundRecipient","type":"address"},{"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"}],"internalType":"struct IAssetForwarder.DepositData","name":"depositData","type":"tuple"},{"internalType":"bytes","name":"destToken","type":"bytes"},{"internalType":"bytes","name":"recipient","type":"bytes"},{"internalType":"bytes","name":"message","type":"bytes"}],"name":"iDepositMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"partnerId","type":"uint256"},{"internalType":"bytes32","name":"destChainIdBytes","type":"bytes32"},{"internalType":"bytes32","name":"recipient","type":"bytes32"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"iDepositUSDC","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"requestSender","type":"string"},{"internalType":"bytes","name":"packet","type":"bytes"},{"internalType":"string","name":"","type":"string"}],"name":"iReceive","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainId","type":"bytes32"},{"internalType":"uint256","name":"depositId","type":"uint256"},{"internalType":"address","name":"destToken","type":"address"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IAssetForwarder.RelayData","name":"relayData","type":"tuple"}],"name":"iRelay","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes32","name":"srcChainId","type":"bytes32"},{"internalType":"uint256","name":"depositId","type":"uint256"},{"internalType":"address","name":"destToken","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"bytes","name":"message","type":"bytes"}],"internalType":"struct IAssetForwarder.RelayDataMessage","name":"relayData","type":"tuple"}],"name":"iRelayMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"isCommunityPauseEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pauseStakeAmountMax","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauseStakeAmountMin","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"rescue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"routerMiddlewareBase","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_destChainIdBytes","type":"bytes32[]"},{"components":[{"internalType":"uint32","name":"domainId","type":"uint32"},{"internalType":"uint256","name":"fee","type":"uint256"},{"internalType":"bool","name":"isSet","type":"bool"}],"internalType":"struct IAssetForwarder.DestDetails[]","name":"_destDetails","type":"tuple[]"}],"name":"setDestDetails","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"toggleCommunityPause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"tokenMessenger","outputs":[{"internalType":"contract ITokenMessenger","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalStakedAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"address","name":"_gatewayContract","type":"address"},{"internalType":"bytes","name":"_routerMiddlewareBase","type":"bytes"},{"internalType":"uint256","name":"minPauseStakeAmount","type":"uint256"},{"internalType":"uint256","name":"maxPauseStakeAmount","type":"uint256"}],"name":"update","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenMessenger","type":"address"}],"name":"updateTokenMessenger","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"usdc","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdrawStakeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"wrappedNativeToken","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}]""")

    # deposit and fill contracts may be the same for some protocols
    if type == 'deposit':
        return { 0: contract_abi }
    elif type == 'fill':
        return { 0: contract_abi }

    return None

def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return ['1', '534352', '324', '42161', '59144', '137', '81457', '10', '43114','8453','56','1101','5000','169','30','728126428', '288', '34443', '1088']

def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None

def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return { 0: ['FundsDeposited','FundsDepositedWithMessage'] }

def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills 
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a 
    # fill event filter will not result in reverted txs being picked up
    return { 0: ['iRelay', 'iRelayMessage'] }

def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return { 0: ['FundsPaid', 'FundsPaidWithMessage'] }
