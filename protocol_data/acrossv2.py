import json

PROTOCOL_NAME = "acrossv2"

def get_contract_address(chain_id, type):
    # Optionally configurable to be different per chain_id and based
    # on type which may be 'deposit' or 'fill'
    contracts = {
        '42161': {
            'deposit': '0xe35e9842fceaCA96570B734083f4a58e8F7C5f2A',
            'fill': '0xe35e9842fceaCA96570B734083f4a58e8F7C5f2A'
        },
        '8453': {
            'deposit': '0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64',
            'fill': '0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64'
        },
        '1': {
            'deposit': '0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5',
            'fill': '0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5'
        },
        '10' : { 
            'deposit': '0x3a23F943181408EAC424116Af7b7790c94Cb97a5',
            'fill': '0x6f26Bf09B1C792e3228e5467807a900A503c0281'
        },
        '137': { 
            'deposit': '0x9295ee1d8C5b022Be115A2AD3c30C72E34e7F096',
            'fill': '0x9295ee1d8C5b022Be115A2AD3c30C72E34e7F096'
        },
        '324': { 
            'deposit': '0xE0B015E54d54fc84a6cB9B666099c46adE9335FF',
            'fill': '0xE0B015E54d54fc84a6cB9B666099c46adE9335FF'
        },
    }

    if chain_id in contracts:
        return contracts[chain_id][type]
    
    return None

def get_contract_abi(chain_id, type):
    contract_deposits_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_router","type":"address"},{"internalType":"address","name":"_wethAddress","type":"address"},{"internalType":"address","name":"_socketGateway","type":"address"},{"internalType":"address","name":"_socketDeployFactory","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"OnlySocketDeployer","type":"error"},{"inputs":[],"name":"OnlySocketGatewayOwner","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"toChainId","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"bridgeName","type":"bytes32"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"bytes32","name":"metadata","type":"bytes32"}],"name":"SocketBridge","type":"event"},{"inputs":[],"name":"BRIDGE_AFTER_SWAP_SELECTOR","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CONNECT_NATIVE_EXTERNAL_BRIDGE_FUNCTION_SELECTOR","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CONNEXT_ERC20_EXTERNAL_BRIDGE_FUNCTION_SELECTOR","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CONNEXT_SWAP_BRIDGE_SELECTOR","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NATIVE_TOKEN_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UINT256_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"bridgeData","type":"bytes"}],"name":"bridgeAfterSwap","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"toChainId","type":"uint256"},{"internalType":"uint256","name":"slippage","type":"uint256"},{"internalType":"uint256","name":"relayerFee","type":"uint256"},{"internalType":"uint32","name":"dstChainDomain","type":"uint32"},{"internalType":"address","name":"receiverAddress","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"bytes32","name":"metadata","type":"bytes32"},{"internalType":"bytes","name":"callData","type":"bytes"}],"name":"bridgeERC20To","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"toChainId","type":"uint256"},{"internalType":"uint256","name":"slippage","type":"uint256"},{"internalType":"uint256","name":"relayerFee","type":"uint256"},{"internalType":"uint32","name":"dstChainDomain","type":"uint32"},{"internalType":"address","name":"receiverAddress","type":"address"},{"internalType":"bytes32","name":"metadata","type":"bytes32"},{"internalType":"bytes","name":"callData","type":"bytes"}],"name":"bridgeNativeTo","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"connextIndetifier","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"killme","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"userAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"rescueEther","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"userAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"rescueFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"router","outputs":[{"internalType":"contract IConnextHandler","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"socketDeployFactory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"socketGateway","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"socketRoute","outputs":[{"internalType":"contract ISocketRoute","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"swapId","type":"uint32"},{"internalType":"bytes","name":"swapData","type":"bytes"},{"components":[{"internalType":"uint256","name":"toChainId","type":"uint256"},{"internalType":"uint256","name":"slippage","type":"uint256"},{"internalType":"uint256","name":"relayerFee","type":"uint256"},{"internalType":"uint32","name":"dstChainDomain","type":"uint32"},{"internalType":"address","name":"receiverAddress","type":"address"},{"internalType":"bytes32","name":"metadata","type":"bytes32"},{"internalType":"bytes","name":"callData","type":"bytes"}],"internalType":"struct ConnextImpl.ConnextBridgeNoTokenData","name":"connextBridgeData","type":"tuple"}],"name":"swapAndBridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"wethAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
    contract_fills_abi = json.loads('[{"inputs":[],"name":"NotCrossChainCall","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"rootBundleId","type":"uint256"}],"name":"EmergencyDeleteRootBundle","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"originToken","type":"address"},{"indexed":true,"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"EnabledDepositRoute","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountToReturn","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"chainId","type":"uint256"},{"indexed":false,"internalType":"uint256[]","name":"refundAmounts","type":"uint256[]"},{"indexed":true,"internalType":"uint32","name":"rootBundleId","type":"uint32"},{"indexed":true,"internalType":"uint32","name":"leafId","type":"uint32"},{"indexed":false,"internalType":"address","name":"l2TokenAddress","type":"address"},{"indexed":false,"internalType":"address[]","name":"refundAddresses","type":"address[]"},{"indexed":false,"internalType":"address","name":"caller","type":"address"}],"name":"ExecutedRelayerRefundRoot","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalFilledAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fillAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"repaymentChainId","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"originChainId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"indexed":false,"internalType":"int64","name":"relayerFeePct","type":"int64"},{"indexed":false,"internalType":"int64","name":"realizedLpFeePct","type":"int64"},{"indexed":true,"internalType":"uint32","name":"depositId","type":"uint32"},{"indexed":false,"internalType":"address","name":"destinationToken","type":"address"},{"indexed":false,"internalType":"address","name":"relayer","type":"address"},{"indexed":true,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"bytes","name":"message","type":"bytes"},{"components":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"int64","name":"relayerFeePct","type":"int64"},{"internalType":"bool","name":"isSlowRelay","type":"bool"},{"internalType":"int256","name":"payoutAdjustmentPct","type":"int256"}],"indexed":false,"internalType":"struct SpokePool.RelayExecutionInfo","name":"updatableRelayData","type":"tuple"}],"name":"FilledRelay","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"originChainId","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"indexed":false,"internalType":"int64","name":"relayerFeePct","type":"int64"},{"indexed":true,"internalType":"uint32","name":"depositId","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"quoteTimestamp","type":"uint32"},{"indexed":false,"internalType":"address","name":"originToken","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":true,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"bytes","name":"message","type":"bytes"}],"name":"FundsDeposited","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"l2Token","type":"address"},{"indexed":false,"internalType":"address","name":"target","type":"address"},{"indexed":false,"internalType":"uint256","name":"numberOfTokensBridged","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"l1Gas","type":"uint256"}],"name":"OptimismTokensBridged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"isPaused","type":"bool"}],"name":"PausedDeposits","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"isPaused","type":"bool"}],"name":"PausedFills","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"relayer","type":"address"},{"indexed":false,"internalType":"address","name":"refundToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"originChainId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"indexed":false,"internalType":"int64","name":"realizedLpFeePct","type":"int64"},{"indexed":true,"internalType":"uint32","name":"depositId","type":"uint32"},{"indexed":false,"internalType":"uint256","name":"fillBlock","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"previousIdenticalRequests","type":"uint256"}],"name":"RefundRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"rootBundleId","type":"uint32"},{"indexed":true,"internalType":"bytes32","name":"relayerRefundRoot","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"slowRelayRoot","type":"bytes32"}],"name":"RelayedRootBundle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"int64","name":"newRelayerFeePct","type":"int64"},{"indexed":true,"internalType":"uint32","name":"depositId","type":"uint32"},{"indexed":true,"internalType":"address","name":"depositor","type":"address"},{"indexed":false,"internalType":"address","name":"updatedRecipient","type":"address"},{"indexed":false,"internalType":"bytes","name":"updatedMessage","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"depositorSignature","type":"bytes"}],"name":"RequestedSpeedUpDeposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"newBuffer","type":"uint32"}],"name":"SetDepositQuoteTimeBuffer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newHubPool","type":"address"}],"name":"SetHubPool","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"newL1Gas","type":"uint32"}],"name":"SetL1Gas","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"l2Token","type":"address"},{"indexed":true,"internalType":"address","name":"tokenBridge","type":"address"}],"name":"SetL2TokenBridge","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newAdmin","type":"address"}],"name":"SetXDomainAdmin","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountToReturn","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"chainId","type":"uint256"},{"indexed":true,"internalType":"uint32","name":"leafId","type":"uint32"},{"indexed":true,"internalType":"address","name":"l2TokenAddress","type":"address"},{"indexed":false,"internalType":"address","name":"caller","type":"address"}],"name":"TokensBridged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"MAX_TRANSFER_SIZE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SLOW_FILL_MAX_TOKENS_TO_SEND","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UPDATE_DEPOSIT_DETAILS_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_initialDepositId","type":"uint32"},{"internalType":"address","name":"_crossDomainAdmin","type":"address"},{"internalType":"address","name":"_hubPool","type":"address"},{"internalType":"address","name":"_l2Eth","type":"address"},{"internalType":"address","name":"_wrappedNativeToken","type":"address"}],"name":"__OvmSpokePool_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_initialDepositId","type":"uint32"},{"internalType":"address","name":"_crossDomainAdmin","type":"address"},{"internalType":"address","name":"_hubPool","type":"address"},{"internalType":"address","name":"_wrappedNativeTokenAddress","type":"address"}],"name":"__SpokePool_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chainId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"crossDomainAdmin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"originToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"int64","name":"relayerFeePct","type":"int64"},{"internalType":"uint32","name":"quoteTimestamp","type":"uint32"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"uint256","name":"maxCount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"depositCounter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"originToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"int64","name":"relayerFeePct","type":"int64"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"uint256","name":"maxCount","type":"uint256"}],"name":"depositNow","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"depositQuoteTimeBuffer","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rootBundleId","type":"uint256"}],"name":"emergencyDeleteRootBundle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"enabledDepositRoutes","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"rootBundleId","type":"uint32"},{"components":[{"internalType":"uint256","name":"amountToReturn","type":"uint256"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"uint256[]","name":"refundAmounts","type":"uint256[]"},{"internalType":"uint32","name":"leafId","type":"uint32"},{"internalType":"address","name":"l2TokenAddress","type":"address"},{"internalType":"address[]","name":"refundAddresses","type":"address[]"}],"internalType":"struct SpokePoolInterface.RelayerRefundLeaf","name":"relayerRefundLeaf","type":"tuple"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"executeRelayerRefundLeaf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"depositor","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"destinationToken","type":"address"},{"internalType":"uint256","name":"totalRelayAmount","type":"uint256"},{"internalType":"uint256","name":"originChainId","type":"uint256"},{"internalType":"int64","name":"realizedLpFeePct","type":"int64"},{"internalType":"int64","name":"relayerFeePct","type":"int64"},{"internalType":"uint32","name":"depositId","type":"uint32"},{"internalType":"uint32","name":"rootBundleId","type":"uint32"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"int256","name":"payoutAdjustment","type":"int256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"executeSlowRelayLeaf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"fillCounter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"depositor","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"destinationToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"maxTokensToSend","type":"uint256"},{"internalType":"uint256","name":"repaymentChainId","type":"uint256"},{"internalType":"uint256","name":"originChainId","type":"uint256"},{"internalType":"int64","name":"realizedLpFeePct","type":"int64"},{"internalType":"int64","name":"relayerFeePct","type":"int64"},{"internalType":"uint32","name":"depositId","type":"uint32"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"uint256","name":"maxCount","type":"uint256"}],"name":"fillRelay","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"depositor","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"updatedRecipient","type":"address"},{"internalType":"address","name":"destinationToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"maxTokensToSend","type":"uint256"},{"internalType":"uint256","name":"repaymentChainId","type":"uint256"},{"internalType":"uint256","name":"originChainId","type":"uint256"},{"internalType":"int64","name":"realizedLpFeePct","type":"int64"},{"internalType":"int64","name":"relayerFeePct","type":"int64"},{"internalType":"int64","name":"updatedRelayerFeePct","type":"int64"},{"internalType":"uint32","name":"depositId","type":"uint32"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"bytes","name":"updatedMessage","type":"bytes"},{"internalType":"bytes","name":"depositorSignature","type":"bytes"},{"internalType":"uint256","name":"maxCount","type":"uint256"}],"name":"fillRelayWithUpdatedDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getCurrentTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hubPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_initialDepositId","type":"uint32"},{"internalType":"address","name":"_crossDomainAdmin","type":"address"},{"internalType":"address","name":"_hubPool","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"l1Gas","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"l2Eth","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"messenger","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"numberOfDeposits","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"pause","type":"bool"}],"name":"pauseDeposits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"pause","type":"bool"}],"name":"pauseFills","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pausedDeposits","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pausedFills","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"refundsRequested","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"relayFills","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"relayerRefundRoot","type":"bytes32"},{"internalType":"bytes32","name":"slowRelayRoot","type":"bytes32"}],"name":"relayRootBundle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"refundToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"originChainId","type":"uint256"},{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"int64","name":"realizedLpFeePct","type":"int64"},{"internalType":"uint32","name":"depositId","type":"uint32"},{"internalType":"uint256","name":"fillBlock","type":"uint256"},{"internalType":"uint256","name":"maxCount","type":"uint256"}],"name":"requestRefund","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rootBundles","outputs":[{"internalType":"bytes32","name":"slowRelayRoot","type":"bytes32"},{"internalType":"bytes32","name":"relayerRefundRoot","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newCrossDomainAdmin","type":"address"}],"name":"setCrossDomainAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"newDepositQuoteTimeBuffer","type":"uint32"}],"name":"setDepositQuoteTimeBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"originToken","type":"address"},{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"bool","name":"enabled","type":"bool"}],"name":"setEnableRoute","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newHubPool","type":"address"}],"name":"setHubPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"newl1Gas","type":"uint32"}],"name":"setL1GasLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"l2Token","type":"address"},{"internalType":"address","name":"tokenBridge","type":"address"}],"name":"setTokenBridge","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"depositor","type":"address"},{"internalType":"int64","name":"updatedRelayerFeePct","type":"int64"},{"internalType":"uint32","name":"depositId","type":"uint32"},{"internalType":"address","name":"updatedRecipient","type":"address"},{"internalType":"bytes","name":"updatedMessage","type":"bytes"},{"internalType":"bytes","name":"depositorSignature","type":"bytes"}],"name":"speedUpDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"tokenBridges","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"wrappedNativeToken","outputs":[{"internalType":"contract WETH9Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')

    if type == 'deposit':
        return contract_fills_abi#contract_deposits_abi
    elif type == 'fill':
        return contract_fills_abi
    
    return None

def get_supported_chains():
    return ['42161', '8453', '1', '10', '137', '324']

def get_deposit_function_filter():
    return None

def get_deposit_event_filter():
    return 'FundsDeposited'

def get_fill_function_filter():
    return 'fillRelay'

def get_fill_event_filter():
    return 'FilledRelay'