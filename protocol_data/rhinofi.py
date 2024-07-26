import json

PROTOCOL_NAME = "rhinofi"

def get_contract_address(chain_id, type):
    # Call by scraping logic to determine where to monitor for events
    # source: https://github.com/rhinofi/contracts_public/
    contracts = {

        # ethereum is not clear, there is no bridge contract
        # there is a deposit contract but no fill contract
        # '1': {
        #     'deposit': { 12062072 : '0xeD9d63a96c27f87B07115b56b2e3572827f21646' },
        #     'fill': { STARTING_BLOCK_NUMBER : '' }
        # },
        '42161' : { 
            'deposit': { 12062072 : '0x10417734001162Ea139e8b044DFe28DbB8B28ad0' },
            'fill': { 12062072 : '0x10417734001162Ea139e8b044DFe28DbB8B28ad0' },
        },
        '56' : { 
            'deposit': { 21550595 : '0xB80A582fa430645A043bB4f6135321ee01005fEf' },
            'fill': { 21550595 : '0xB80A582fa430645A043bB4f6135321ee01005fEf' },
        },
        '137': {
            'deposit': { 16917268 : '0xBA4EEE20F434bC3908A0B18DA496348657133A7E' },
            'fill': { 16917268 : '0xBA4EEE20F434bC3908A0B18DA496348657133A7E' }
        },
        '324': {
            'deposit': { 193 : '0x1fa66e2B38d0cC496ec51F81c3e05E6A6708986F' },
            'fill': { 193 : '0x1fa66e2B38d0cC496ec51F81c3e05E6A6708986F' }
        },
        '1101': {
            'deposit': { 15845 : '0x65A4b8A0927c7FD899aed24356BF83810f7b9A3f' },
            'fill': { 15845 : '0x65A4b8A0927c7FD899aed24356BF83810f7b9A3f' }
        },
        '10': {
            'deposit': { 96888536 : '0x0bCa65bf4b4c8803d2f0B49353ed57CAAF3d66Dc' },
            'fill': { 96888536 : '0x0bCa65bf4b4c8803d2f0B49353ed57CAAF3d66Dc' }
        },
        '59144': {
            'deposit': { 593 : '0xcF68a2721394dcf5dCF66F6265C1819720F24528' },
            'fill': { 593 : '0xcF68a2721394dcf5dCF66F6265C1819720F24528' }
        },
        '8453': {
            'deposit': { 1448656 : '0x2f59E9086ec8130E21BD052065a9E6B2497bb102' },
            'fill': { 1448656 : '0x2f59E9086ec8130E21BD052065a9E6B2497bb102' }
        },
        '169': {
            'deposit': { 21324 : '0x2B4553122D960CA98075028d68735cC6b15DeEB5' },
            'fill': { 21324 : '0x2B4553122D960CA98075028d68735cC6b15DeEB5' }
        },
        '534352': {
            'deposit': { 694 : '0x87627c7E586441EeF9eE3C28B66662e897513f33' },
            'fill': { 694 : '0x87627c7E586441EeF9eE3C28B66662e897513f33' }
        },
    }
    return contracts[chain_id][type]

# TODO: find solana contracts, they are absent in https://github.com/rhinofi/contracts_public/
def get_function_identifier(chain_id, type):
    # Ids for solana functions (if required)
    identifiers = {
        # '7565164': {
        #     "deposit": "828362be28ce4432",
        #     "fill": "3dd627f841d49924",
        # }
    }
    return identifiers[chain_id][type]

def get_contract_abi(chain_id, type):
    contract_abi = json.loads("""
[
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "BridgedDeposit",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "string",
                "name": "withdrawalId",
                "type": "string"
            }
        ],
        "name": "BridgedWithdrawal",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amountToken",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amountNative",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "bytes",
                "name": "ref",
                "type": "bytes"
            }
        ],
        "name": "BridgedWithdrawalWithData",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amountToken",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amountNative",
                "type": "uint256"
            }
        ],
        "name": "BridgedWithdrawalWithNative",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "uint8",
                "name": "version",
                "type": "uint8"
            }
        ],
        "name": "Initialized",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "addFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "addFundsNative",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "tokenAddress",
                "type": "address"
            },
            {
                "internalType": "int256",
                "name": "maxAmount",
                "type": "int256"
            }
        ],
        "name": "allowDeposits",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bool",
                "name": "value",
                "type": "bool"
            }
        ],
        "name": "allowDepositsGlobal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "value",
                "type": "bool"
            }
        ],
        "name": "authorize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "authorized",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "checkMaxDepositAmount",
        "outputs": [],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "createVMContract",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "depositNative",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "depositsDisallowed",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "initialize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "maxDepositAmount",
        "outputs": [
            {
                "internalType": "int256",
                "name": "",
                "type": "int256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "name": "processedWithdrawalIds",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "removeFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "removeFundsNative",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "withdrawNativeV2",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "withdrawV2",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountToken",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountNative",
                "type": "uint256"
            }
        ],
        "name": "withdrawV2WithNative",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            }
        ],
        "name": "withdrawVmFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountNative",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "target",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct BridgeVM.Call[]",
                "name": "datas",
                "type": "tuple[]"
            },
            {
                "internalType": "bytes",
                "name": "ref",
                "type": "bytes"
            }
        ],
        "name": "withdrawWithData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]
""")

    # deposit and fill contracts may be the same for some protocols
    if type == 'deposit':
        return { 0 : contract_abi }
    elif type == 'fill':
        return { 0 : contract_abi }
    
    return None

def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    # TODO: add more chains
    return ['42161', '56', '137', '324', '1101', '10', '59144', '8453', '169', '534352']

def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None

def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return { 0 : ['BridgedDeposit'] }

def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills 
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a 
    # fill event filter will not result in reverted txs being picked up
    # TODO: verify rhino.fi does not have any not-successful fills, because
    # there is only one filler and it gets the funds from pre-filled pools, related discord chat:
    # https://discord.com/channels/745570257808130058/745571091438764062/1265924362276438108
    return { 0 : [] }

def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return { 0 : ['BridgedWithdrawal', 'BridgedWithdrawalWithData', 'BridgedWithdrawalWithNative'] }
