import json

PROTOCOL_NAME = "protocol_name"

STARTING_BLOCK_NUMBER = 0

def get_contract_address(chain_id, type):
    # Call by scraping logic to determine where to monitor for events
    contracts = {
        '1': {
            'deposit': { STARTING_BLOCK_NUMBER : '0xeF4fB24aD0916217251F553c0596F8Edc630EB66' },
            'fill': { STARTING_BLOCK_NUMBER : '0xE7351Fd770A37282b91D153Ee690B63579D6dd7f' }
        },
        '10' : { 
            'deposit': { STARTING_BLOCK_NUMBER : '0xeF4fB24aD0916217251F553c0596F8Edc630EB66' },
            'fill': { STARTING_BLOCK_NUMBER : '0xE7351Fd770A37282b91D153Ee690B63579D6dd7f' }
        }
    }
    return contracts[chain_id][type]

def get_function_identifier(chain_id, type):
    # Ids for solana functions (if required)
    identifiers = {
        '7565164': {
            "deposit": "828362be28ce4432",
            "fill": "3dd627f841d49924",
        }
    }
    return identifiers[chain_id][type]

def get_contract_abi(chain_id, type):
    contract_abi = json.loads("""[
    {
        "abi": "as_json"
    }
]""")

    # deposit and fill contracts may be the same for some protocols
    if type == 'deposit':
        return { STARTING_BLOCK_NUMBER : contract_abi }
    elif type == 'fill':
        return { STARTING_BLOCK_NUMBER : contract_abi }
    
    return None

def get_supported_chains():
    # Only chain_ids listed here will be used when scraping data
    return ['1', '10']

def get_deposit_function_filter():
    # To record deposit transactions specify the function name
    # NOTE: this is optional and can be left as None
    return None

def get_deposit_event_filter():
    # To record deposit events specify the deposit function name
    # NOTE: either this or the deposit function filter must be set
    return { STARTING_BLOCK_NUMBER : 'CreatedOrder' }

def get_fill_function_filter():
    # To record fill transcations specify the function name
    # NOTE: to accurately record multiple (attempted or otherwise) fills 
    # for an order where subsequent fills result in rejected transactions
    # it is VERY IMPORTANT to add a fill function filter. Only adding a 
    # fill event filter will not result in reverted txs being picked up
    return { STARTING_BLOCK_NUMBER : 'fulfillOrder' }

def get_fill_event_filter():
    # To record fill events specify the event name
    # NOTE: wherever possible please also include the fill function filter above
    return { STARTING_BLOCK_NUMBER : 'FulfilledOrder' }
