import json

PROTOCOL_NAME = "synapse"

def get_contract_address(chain_id, type):
    # Call by scraping logic to determine where to monitor for events
    contracts = {
        '42161': {
                'deposit': {
                    0 : '0x6C0771aD91442D670159a8171C35F4828E19aFd2',
                    189700328 : '0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E'
                },
                'fill':  {
                    0 : '0x6C0771aD91442D670159a8171C35F4828E19aFd2',
                    189700328 : '0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E'
                },
        }, '1': {
                'deposit': {
                    0 : '0x4983DB49336fD4f95e864aB6DA9135e057EF0be1',
                    19421323 : '0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E',
                },
                'fill':  {
                    0 : '0x4983DB49336fD4f95e864aB6DA9135e057EF0be1',
                    19421323 : '0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E',
                },
        }, '10': {
                'deposit': {
                    0 : '0x6C0771aD91442D670159a8171C35F4828E19aFd2',
                    117334308 : '0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E',
                },
                'fill': {
                    0 : '0x6C0771aD91442D670159a8171C35F4828E19aFd2',
                    117334308 : '0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E',
                },
        }, '81457': {
                'deposit': {
                    0 : '0xD1734b283d58C1E36fE5187F20Ae17A3Da7e702f'
                },
                'fill': {
                    0 : '0xD1734b283d58C1E36fE5187F20Ae17A3Da7e702f'
                },
        }, 
    }

    return contracts[chain_id][type]

def get_contract_abi(chain_id, type):
    contract_abi = json.loads("""[
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
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
        "name": "BridgeDepositClaimed",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
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
        "name": "BridgeDepositRefunded",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            }
        ],
        "name": "BridgeProofDisputed",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "bytes32",
                "name": "transactionHash",
                "type": "bytes32"
            }
        ],
        "name": "BridgeProofProvided",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint32",
                "name": "originChainId",
                "type": "uint32"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "originToken",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "destToken",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "originAmount",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "destAmount",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "chainGasAmount",
                "type": "uint256"
            }
        ],
        "name": "BridgeRelayed",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "bytes",
                "name": "request",
                "type": "bytes"
            },
            {
                "indexed": false,
                "internalType": "uint32",
                "name": "destChainId",
                "type": "uint32"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "originToken",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "destToken",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "originAmount",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "destAmount",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "bool",
                "name": "sendChainGas",
                "type": "bool"
            }
        ],
        "name": "BridgeRequested",
        "type": "event"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "dstChainId",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "sender",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "originToken",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "destToken",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "originAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "destAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "sendChainGas",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "deadline",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IFastBridge.BridgeParams",
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "bridge",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            }
        ],
        "name": "canClaim",
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
                "internalType": "bytes",
                "name": "request",
                "type": "bytes"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            }
        ],
        "name": "claim",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "transactionId",
                "type": "bytes32"
            }
        ],
        "name": "dispute",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "request",
                "type": "bytes"
            }
        ],
        "name": "getBridgeTransaction",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "originChainId",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "destChainId",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "originSender",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "destRecipient",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "originToken",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "destToken",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "originAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "destAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "originFeeAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "sendChainGas",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "deadline",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "nonce",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IFastBridge.BridgeTransaction",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "request",
                "type": "bytes"
            },
            {
                "internalType": "bytes32",
                "name": "destTxHash",
                "type": "bytes32"
            }
        ],
        "name": "prove",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "request",
                "type": "bytes"
            }
        ],
        "name": "refund",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "request",
                "type": "bytes"
            }
        ],
        "name": "relay",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
    ]""")

    # deposit and fill contracts may be the same for some protocols
    if type == 'deposit':
        return { 0: contract_abi }
    elif type == 'fill':
        return { 0: contract_abi }

    return None

def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return ['42161', '81457', '1', '10']

def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None

def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return { 0: 'BridgeRequested' }

def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills 
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a 
    # fill event filter will not result in reverted txs being picked up
    return { 0: 'relay' }

def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return { 0: 'BridgeRelayed' }
