PROTOCOL_NAME = "dln"

def get_contract_address(chain_id):
    # Optionally configurable to be different per chain_id
    return "0x1234"

def get_supported_chains():
    return [1, 10]

def get_deposit_function_filter():
    return "" # or None if no filter to use

def get_deposit_event_filter():
    return "" # or None if no  filter to use

def get_fill_function_filter():
    return "" # or None if no filter to use

def get_fill_event_filter():
    return "" # or None if no  filter to use
