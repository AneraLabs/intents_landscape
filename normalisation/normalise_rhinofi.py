from normalisation.constants import NATIVE_TOKEN_ADDRESS
from protocol_data.solana_parser import UNPARSED_INSTRUCTION_FIELD_NAME


def normalise_rhinofi(original_doc, type, normalised_doc) -> dict | None:
    '''
    A lot of data is filled later during matching.
    '''
    if type == 'event':
        normalised_doc['order_id'] = original_doc['scraper_tx_hash']
        if original_doc['scraper_event'] == 'BridgedDeposit':
            normalised_doc['name'] = 'order_deposit_event'

            normalised_doc['source_chain'] = original_doc['scraper_originChain']
            normalised_doc['source_token_address'] = original_doc['event']['token']
            normalised_doc['source_token_amount'] = original_doc['event']['amount']

            if 'user' in original_doc['event']:
                normalised_doc['source_address'] = original_doc['event']['user']
            else:
                normalised_doc['source_address'] = original_doc['scraper_from']

            if normalised_doc['source_token_address'] == '0x0000000000000000000000000000000000000000':
                normalised_doc['source_token_address'] = NATIVE_TOKEN_ADDRESS

        elif original_doc['scraper_event'] in {'BridgedWithdrawal', 'BridgedWithdrawalWithData', 'BridgedWithdrawalWithNative'}:
            normalised_doc['name'] = 'order_fill_event'
            normalised_doc['filler_address'] = original_doc['scraper_from']
            normalised_doc['destination_chain'] = original_doc['scraper_originChain']
            normalised_doc['destination_token_address'] = original_doc['event']['token']
            if 'amount' in original_doc['event']:
                normalised_doc['destination_token_amount'] = original_doc['event']['amount']
            elif 'amountToken' in original_doc['event']:
                normalised_doc['destination_token_amount'] = original_doc['event']['amountToken']
            else:
                raise ValueError(f"No amount found in event [{original_doc['event']}]")

            if 'user' in original_doc['event']:
                normalised_doc['destination_address'] = original_doc['event']['user']
            elif 'scraper_to' in original_doc:
                normalised_doc['destination_address'] = original_doc['scraper_to']
            else:
                print(f"No destination address found in event [{original_doc}]")
                return None

            if normalised_doc['destination_token_address'] == '0x0000000000000000000000000000000000000000':
                normalised_doc['destination_token_address'] = NATIVE_TOKEN_ADDRESS
        else:
            print(f"Unknown event type [{original_doc['scraper_event']}] for rhino.fi doc: [{original_doc}]")
            return None
    else:
        if original_doc['scraper_originChain'] == '7565164': # solana
            if UNPARSED_INSTRUCTION_FIELD_NAME in original_doc:
                return None
            normalised_doc['order_id'] = original_doc['scraper_tx_hash']
            if original_doc['tx']['instruction'] == "deposit":
                normalised_doc['name'] = 'order_deposit_tx'
                normalised_doc['source_address'] = original_doc['source_address']
                normalised_doc['source_chain'] = original_doc['scraper_originChain']
                normalised_doc['source_token_address'] = original_doc['source_token_address']
                normalised_doc['source_token_amount'] = original_doc['tx']['amount']
            else:
                normalised_doc['name'] = 'order_fill_tx'
                normalised_doc['destination_address'] = original_doc['destination_address']
                normalised_doc['destination_chain'] = original_doc['scraper_originChain']
                normalised_doc['destination_token_address'] = original_doc['destination_token_address']
                normalised_doc['destination_token_amount'] = original_doc['tx']['amount']
                normalised_doc['filler_address'] = original_doc['filler_address']
        else:
            raise ValueError(f"Unknown type [{type}] for rhino.fi doc: [{original_doc}]")

    return normalised_doc