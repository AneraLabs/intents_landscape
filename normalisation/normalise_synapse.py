import time
from web3 import Web3
from typing import Any

from normalisation.utils import normalise_address_if_needed
from signal_handler import SignalHandler

# This module will only work within the context of the parent closed source repository because of this import
# TODO: remove after replacing get_synapse_bridge_transaction with a parser with no call to the RPC
try:
    from services.common.rpc_utils import execute_web3_eth_method
except ImportError:
    pass


def normalise_synapse(original_doc, type, normalised_doc, signal_handler: SignalHandler):
    if type == 'tx':
        if original_doc['scraper_function'] != 'relay':
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None
        normalised_doc['name'] = 'order_fill_tx'
        
        decodedTx = get_synapse_bridge_transaction(original_doc, signal_handler)
        if decodedTx is None:
            return None

        if signal_handler.shutdown:
            return None

        [origin_chain_id, dest_chain_id, origin_sender, dest_recepient, origin_token, dest_token, origin_amount, dest_amount, origin_fee_amount, send_chain_gas, deadline, nonce] = decodedTx        

        normalised_doc['source_address'] = origin_sender
        normalised_doc['destination_address'] = dest_recepient

        normalised_doc['source_chain'] = origin_chain_id
        normalised_doc['destination_chain'] = dest_chain_id

        normalised_doc['source_token_address'] = origin_token
        normalised_doc['destination_token_address'] = dest_token

        normalised_doc['source_token_amount'] = origin_amount
        normalised_doc['destination_token_amount'] = dest_amount
        
        normalised_doc['order_id'] = str(normalised_doc['source_chain']) + '_' + str(Web3.solidity_keccak(['bytes'], [original_doc['tx']['request']]).hex())
        normalised_doc['protocol_fee'] = origin_fee_amount

        normalised_doc['filler_address'] = original_doc['scraper_from']

    elif type == 'event':
        if original_doc['scraper_event'] == 'BridgeRequested':
            normalised_doc['name'] = 'order_deposit_event'

            normalised_doc['source_address'] = original_doc['event']['sender']
            normalised_doc['destination_address'] = original_doc['event']['sender']

            normalised_doc['source_chain'] = original_doc['scraper_originChain']
            normalised_doc['destination_chain'] = original_doc['event']['destChainId']

            normalised_doc['source_token_address'] = normalise_address_if_needed(original_doc['event']['originToken'])
            normalised_doc['destination_token_address'] = normalise_address_if_needed(original_doc['event']['destToken'])

            normalised_doc['source_token_amount'] = original_doc['event']['originAmount']
            normalised_doc['destination_token_amount'] = original_doc['event']['destAmount']

            normalised_doc['protocol_fee'] = 0 

        elif original_doc['scraper_event'] == 'BridgeRelayed':
            normalised_doc['name'] = 'order_fill_event'

            normalised_doc['source_address'] = original_doc['event']['to']
            # Note there is a relayExecutionInfo.updatedRecipient, we should check how this is used..
            normalised_doc['destination_address'] = original_doc['event']['to']

            normalised_doc['source_chain'] = original_doc['event']['originChainId']
            normalised_doc['destination_chain'] = original_doc['scraper_originChain']

            normalised_doc['source_token_address'] = normalise_address_if_needed(original_doc['event']['originToken'])
            normalised_doc['destination_token_address'] = normalise_address_if_needed(original_doc['event']['destToken'])

            normalised_doc['source_token_amount'] = original_doc['event']['originAmount']
            normalised_doc['destination_token_amount'] = original_doc['event']['destAmount']
            
            # TODO double check that this is safe, maybe there is a token swap happening?
            normalised_doc['protocol_fee'] = 0

            # Ideally we'd use the value in original_doc['event']['relayer'], however this would be inconsistent with txs
            # which do not expose this. Without looking at the inner txs the originating EOA is the best we can do for now
            normalised_doc['filler_address'] = original_doc['scraper_from']
        else:
            print(f"Unknown event type {original_doc['scraper_event']}")
            return None
        
        normalised_doc['order_id'] = str(normalised_doc['source_chain']) + '_' + str(original_doc['event']['transactionId'])

    # approximate prove and claim gas paid
    if normalised_doc['name'] in ['order_fill_tx', 'order_fill_event'] and 'source_chain' in normalised_doc:
        if normalised_doc['source_chain'] == '1':
            normalised_doc['scraper_prove_gas_paid_usd'] = 2.0
            normalised_doc['scraper_claim_gas_paid_usd'] = 1.8
        else:
            normalised_doc['scraper_prove_gas_paid_usd'] = 0.01
            normalised_doc['scraper_claim_gas_paid_usd'] = 0.01

    return normalised_doc


def get_synapse_bridge_transaction(original_doc, signal_handler: SignalHandler):
    # TODO: This is ugly, open to any PRs that can improve this by decoding inplace
    abi="""[{
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
    }]"""


    chain_id = original_doc["scraper_originChain"]

    contract = execute_web3_eth_method(chain_id, 'contract', signal_handler, address="0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E", abi=abi)
    if contract is None:
        return None

    max_retry = 4
    decodedTx = None

    while max_retry > 0:
        try:
            decodedTx = contract.functions.getBridgeTransaction(original_doc['tx']['request']).call()
            break
        except Exception as e:
            print(f"Call to synapse contract function due to {e}.. retrying {max_retry}")
            time.sleep(2)
            max_retry -= 1

    return decodedTx


def test_get_synapse_bridge_transaction(): 

    mock_original_doc = {
        "_id": "665789c6cb6ffd3353ef669a",
        "scraper_originChain": "1",
        "scraper_blockNumber": 19484048,
        "scraper_blockTimestamp": 1711036379,
        "scraper_from": "0xDc927Bd56CF9DfC2e3779C7E3D6d28dA1C219969",
        "scraper_protocol": "synapse",
        "scraper_contractAddress": "0x5523D3c98809DdDB82C686E152F5C58B1B0fB59E",
        "scraper_function": "relay",
        "scraper_tx_status": "ok",
        "scraper_tx_hash": "0x0cf1d7d3fdc689e68fbfa20d7f5c163c38a9d7845cd76f7a8e31ecb9bf58f586",
        "tx": {
            "request": "0x000000000000000000000000000000000000000000000000000000000000a4b1000000000000000000000000000000000000000000000000000000000000000100000000000000000000000008df3044b520fd001c93e97041d3f257d8c0db7b00000000000000000000000008df3044b520fd001c93e97041d3f257d8c0db7b000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000001cdc2aa1409600000000000000000000000000000000000000000000000000001bb262f6f668a89000000000000000000000000000000000000000000000000000017a598c3a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000065fc65be00000000000000000000000000000000000000000000000000000000000002c5"
        },
    }

    signal_handler = SignalHandler()
    get_synapse_bridge_transaction(mock_original_doc, signal_handler)

if __name__ == "__main__":
    test_get_synapse_bridge_transaction()