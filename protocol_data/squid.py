import json

PROTOCOL_NAME = "squid"

def get_contract_address(chain_id, type):
    # Call by scraping logic to determine where to monitor for events
    contracts = {
		'1': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '42161': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '10': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '59144': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '8453': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '43114': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '137': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '56': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '250': {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '1284' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '5000' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '534352' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '42220' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '2222' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '81457' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}, '252' : {
			'deposit': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666',
			'fill': '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
		}

    }

    return contracts[chain_id][type]

def get_contract_abi(chain_id, type):
    contract_abi = json.loads("""[{"inputs":[{"internalType":"address","name":"_gateway","type":"address"},{"internalType":"address","name":"_gasService","type":"address"},{"internalType":"address","name":"_multicall","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AlreadyExecuted","type":"error"},{"inputs":[],"name":"ApprovalFailed","type":"error"},{"inputs":[],"name":"ContractIsPaused","type":"error"},{"inputs":[],"name":"ExpressExecutorAlreadySet","type":"error"},{"inputs":[],"name":"InsufficientValue","type":"error"},{"inputs":[],"name":"InvalidAddress","type":"error"},{"inputs":[],"name":"InvalidCodeHash","type":"error"},{"inputs":[],"name":"InvalidImplementation","type":"error"},{"inputs":[],"name":"InvalidOwner","type":"error"},{"inputs":[],"name":"InvalidOwnerAddress","type":"error"},{"inputs":[],"name":"NotApprovedByGateway","type":"error"},{"inputs":[],"name":"NotOwner","type":"error"},{"inputs":[],"name":"NotPauser","type":"error"},{"inputs":[],"name":"NotPendingPauser","type":"error"},{"inputs":[],"name":"NotProxy","type":"error"},{"inputs":[],"name":"SetupFailed","type":"error"},{"inputs":[],"name":"TokenTransferFailed","type":"error"},{"inputs":[],"name":"ZeroAddressProvided","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"payloadHash","type":"bytes32"}],"name":"CrossMulticallExecuted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"payloadHash","type":"bytes32"},{"indexed":false,"internalType":"bytes","name":"reason","type":"bytes"},{"indexed":true,"internalType":"address","name":"refundRecipient","type":"address"}],"name":"CrossMulticallFailed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"commandId","type":"bytes32"},{"indexed":false,"internalType":"string","name":"sourceChain","type":"string"},{"indexed":false,"internalType":"string","name":"sourceAddress","type":"string"},{"indexed":false,"internalType":"bytes32","name":"payloadHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"expressExecutor","type":"address"}],"name":"ExpressExecuted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"commandId","type":"bytes32"},{"indexed":false,"internalType":"string","name":"sourceChain","type":"string"},{"indexed":false,"internalType":"string","name":"sourceAddress","type":"string"},{"indexed":false,"internalType":"bytes32","name":"payloadHash","type":"bytes32"},{"indexed":false,"internalType":"string","name":"symbol","type":"string"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"address","name":"expressExecutor","type":"address"}],"name":"ExpressExecutedWithToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"commandId","type":"bytes32"},{"indexed":false,"internalType":"string","name":"sourceChain","type":"string"},{"indexed":false,"internalType":"string","name":"sourceAddress","type":"string"},{"indexed":false,"internalType":"bytes32","name":"payloadHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"expressExecutor","type":"address"}],"name":"ExpressExecutionFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"commandId","type":"bytes32"},{"indexed":false,"internalType":"string","name":"sourceChain","type":"string"},{"indexed":false,"internalType":"string","name":"sourceAddress","type":"string"},{"indexed":false,"internalType":"bytes32","name":"payloadHash","type":"bytes32"},{"indexed":false,"internalType":"string","name":"symbol","type":"string"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"address","name":"expressExecutor","type":"address"}],"name":"ExpressExecutionWithTokenFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"currentPauser","type":"address"},{"indexed":true,"internalType":"address","name":"pendingPauser","type":"address"}],"name":"PauserProposed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingPauser","type":"address"}],"name":"PauserUpdated","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newImplementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"acceptPauser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"bridgedTokenSymbol","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string","name":"destinationChain","type":"string"},{"internalType":"string","name":"destinationAddress","type":"string"},{"internalType":"bytes","name":"payload","type":"bytes"},{"internalType":"address","name":"gasRefundRecipient","type":"address"},{"internalType":"bool","name":"enableExpress","type":"bool"}],"name":"bridgeCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"components":[{"internalType":"enum ISquidMulticall.CallType","name":"callType","type":"uint8"},{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"callData","type":"bytes"},{"internalType":"bytes","name":"payload","type":"bytes"}],"internalType":"struct ISquidMulticall.Call[]","name":"calls","type":"tuple[]"},{"internalType":"string","name":"bridgedTokenSymbol","type":"string"},{"internalType":"string","name":"destinationChain","type":"string"},{"internalType":"string","name":"destinationAddress","type":"string"}],"name":"callBridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"components":[{"internalType":"enum ISquidMulticall.CallType","name":"callType","type":"uint8"},{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"callData","type":"bytes"},{"internalType":"bytes","name":"payload","type":"bytes"}],"internalType":"struct ISquidMulticall.Call[]","name":"calls","type":"tuple[]"},{"internalType":"string","name":"bridgedTokenSymbol","type":"string"},{"internalType":"string","name":"destinationChain","type":"string"},{"internalType":"string","name":"destinationAddress","type":"string"},{"internalType":"bytes","name":"payload","type":"bytes"},{"internalType":"address","name":"gasRefundRecipient","type":"address"},{"internalType":"bool","name":"enableExpress","type":"bool"}],"name":"callBridgeCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"contractId","outputs":[{"internalType":"bytes32","name":"id","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes32","name":"commandId","type":"bytes32"},{"internalType":"string","name":"sourceChain","type":"string"},{"internalType":"string","name":"sourceAddress","type":"string"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"execute","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"commandId","type":"bytes32"},{"internalType":"string","name":"sourceChain","type":"string"},{"internalType":"string","name":"sourceAddress","type":"string"},{"internalType":"bytes","name":"payload","type":"bytes"},{"internalType":"string","name":"tokenSymbol","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"executeWithToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"commandId","type":"bytes32"},{"internalType":"string","name":"sourceChain","type":"string"},{"internalType":"string","name":"sourceAddress","type":"string"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"expressExecute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"commandId","type":"bytes32"},{"internalType":"string","name":"sourceChain","type":"string"},{"internalType":"string","name":"sourceAddress","type":"string"},{"internalType":"bytes","name":"payload","type":"bytes"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"expressExecuteWithToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"components":[{"internalType":"enum ISquidMulticall.CallType","name":"callType","type":"uint8"},{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"callData","type":"bytes"},{"internalType":"bytes","name":"payload","type":"bytes"}],"internalType":"struct ISquidMulticall.Call[]","name":"calls","type":"tuple[]"}],"name":"fundAndRunMulticall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"gateway","outputs":[{"internalType":"contract IAxelarGateway","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"commandId","type":"bytes32"},{"internalType":"string","name":"sourceChain","type":"string"},{"internalType":"string","name":"sourceAddress","type":"string"},{"internalType":"bytes32","name":"payloadHash","type":"bytes32"}],"name":"getExpressExecutor","outputs":[{"internalType":"address","name":"expressExecutor","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"commandId","type":"bytes32"},{"internalType":"string","name":"sourceChain","type":"string"},{"internalType":"string","name":"sourceAddress","type":"string"},{"internalType":"bytes32","name":"payloadHash","type":"bytes32"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getExpressExecutorWithToken","outputs":[{"internalType":"address","name":"expressExecutor","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"implementation_","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"owner_","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"value","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauser","outputs":[{"internalType":"address","name":"value","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"owner_","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingPauser","outputs":[{"internalType":"address","name":"value","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"proposeOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"data","type":"bytes"}],"name":"setup","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPauser","type":"address"}],"name":"updatePauser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes32","name":"newImplementationCodeHash","type":"bytes32"},{"internalType":"bytes","name":"params","type":"bytes"}],"name":"upgrade","outputs":[],"stateMutability":"nonpayable","type":"function"}]""")
    
    # deposit and fill contracts may be the same for some protocols
    if type == 'deposit':
        return contract_abi
    elif type == 'fill':
        return contract_abi

    return None

def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return [
		'1', # Ethereum
		'42161', # Arbitrum
		'10', # Optimism
		'59144', # Linea 
		'8453', # Base
		'43114', # Avalanche
		'137', # Polygon
		'56', # BSC
		'250', # Fantom
		'1284', # Moonbeam
		'5000', # Mantle
		'534352', # Scroll
		'42220', # Celo 
		'2222', # Kava EVM
		'81457', # Blast
		'252', # Fraxtal
		# 'osmosis', # Osmosis
		# 'cosmoshub', # cosmos-hub
		# 'dydx', # DyDx - Not there on axelar
		# 'celestia', 
		# 'kujira',
		# 'neutron',
		# 'stargaze',
		# 'axelar', # Not found on axelar
		# 'noble', # Not found on axelar
		# 'umee',
		# 'secret-snip',
		# 'persistence',
		# 'sommelier',
		# 'stride',
		# 'injective',
		# 'crescent',
		# 'terra-2',
		# 'juno',
		# 'sei',
		# 'carbon',
		# 'regen',
		# 'agoric',
		# 'chihuahua',
		# 'akash', # Not found on axelar
		# 'comdex',
		# 'archway',
		# 'quicksilver', # not found
		# 'omniflix', # not found
		# 'coreum',# not found
		# 'migaloo',
		# 'mars-hub',# not found
		# 'terra', # Terra Classic
		# 'assetmantle',# not found
		# 'gravitybridge',# not found
		# 'bitcanna',# not found
		# 'bitsong',# not found
		# 'cheqd',# not found
		# 'decentr',# not found
		# 'desmos',# not found
		# 'irisnet',# not found
		# 'impacts-hub',# not found
		# 'jackal',# not found
		# 'likecoin',# not found
		# 'lumnetwork',# not found
		# 'sentinel',# not found
		# 'nolus',# not found
		# 'kava_ibc',# not found
		# 'teritori',
		# 'humans',# not found
		# 'evmos',
		# 'dymension'
	]

def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return "callBridgeCall"

def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return None

def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills 
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a 
    # fill event filter will not result in reverted txs being picked up
    return 'expressExecuteWithToken'

def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return 'ExpressExecutedWithToken'