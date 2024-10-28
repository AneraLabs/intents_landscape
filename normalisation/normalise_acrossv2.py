from normalisation.utils import normalise_address_if_needed


def normalise_across_v2(original_doc, type, normalised_doc):
    if type == 'tx':
        if original_doc['scraper_function'] != 'fillRelay':
            print(f"Unknown funciton type {original_doc['scraper_function']}")
            return None
        normalised_doc['name'] = 'order_fill_tx'

        normalised_doc['source_address'] = original_doc['tx']['depositor']
        normalised_doc['destination_address'] = original_doc['tx']['recipient']

        normalised_doc['source_chain'] = original_doc['tx']['originChainId']
        normalised_doc['destination_chain'] = int(normalised_doc['scraper_originChain'])

        # This may be a dangerous assumption
        #normalised_doc['source_token_address'] = normalise_address_if_needed(original_doc['tx']['destinationToken'])
        normalised_doc['destination_token_address'] = normalise_address_if_needed(original_doc['tx']['destinationToken'])

        #normalised_doc['source_token_amount'] = original_doc['tx']['amount']
        normalised_doc['destination_token_amount'] = original_doc['tx']['amount']

        normalised_doc['order_id'] = str(normalised_doc['source_chain']) + '_' + str(original_doc['tx']['depositId'])
        normalised_doc['protocol_fee'] = int(original_doc['tx']['realizedLpFeePct']) + int(original_doc['tx']['relayerFeePct'])

        normalised_doc['filler_address'] = original_doc['scraper_from']

    elif type == 'event':
        if original_doc['scraper_event'] == 'FundsDeposited':
            normalised_doc['name'] = 'order_deposit_event'

            normalised_doc['source_address'] = original_doc['event']['depositor']
            normalised_doc['destination_address'] = original_doc['event']['recipient']

            normalised_doc['source_chain'] = original_doc['event']['originChainId']
            normalised_doc['destination_chain'] = original_doc['event']['destinationChainId']

            normalised_doc['source_token_address'] = normalise_address_if_needed(original_doc['event']['originToken'])
            #normalised_doc['destination_token_address'] = normalise_address_if_needed(original_doc['event']['originToken'])

            normalised_doc['source_token_amount'] = original_doc['event']['amount']
            #normalised_doc['destination_token_amount'] = original_doc['event']['amount']

            normalised_doc['protocol_fee'] = int(original_doc['event']['relayerFeePct'])

        elif original_doc['scraper_event'] == 'FilledRelay':
            normalised_doc['name'] = 'order_fill_event'

            normalised_doc['source_address'] = original_doc['event']['relayer']
            normalised_doc['destination_address'] = original_doc['event']['recipient']

            normalised_doc['source_chain'] = original_doc['event']['originChainId']
            normalised_doc['destination_chain'] = original_doc['event']['destinationChainId']

            #normalised_doc['source_token_address'] = normalise_address_if_needed(original_doc['event']['destinationToken'])
            normalised_doc['destination_token_address'] = normalise_address_if_needed(original_doc['event']['destinationToken'])

            #normalised_doc['source_token_amount'] = original_doc['event']['fillAmount']
            normalised_doc['destination_token_amount'] = original_doc['event']['fillAmount']

            normalised_doc['protocol_fee'] = int(original_doc['event']['realizedLpFeePct']) + int(original_doc['event']['relayerFeePct'])

            # Ideally we'd use the value in original_doc['event']['relayer'], however this would be inconsistent with txs
            # which do not expose this. Without looking at the inner txs the originating EOA is the best we can do for now
            normalised_doc['filler_address'] = original_doc['scraper_from']
        else:
            print(f"Unknown event type {original_doc['scraper_event']}")
            return None

        normalised_doc['order_id'] = str(normalised_doc['source_chain']) + '_' + str(original_doc['event']['depositId'])

    return normalised_doc