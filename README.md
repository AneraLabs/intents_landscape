# Introduction

All data on the dashboard is build from open sources that can be contributed to by anyone to update existing protocols, add new ones or correct mistakes to improve the quality of the data we provide.

> Spotted a mistake? Want to add a new intent based protocol? We are grateful for all contributions - this page explains how to contribute.

## Data sources

[intent.markets](https://intent.markets) has been created to provide transparent and verifiable insights into the emerging space of Intent based protocols. As such, all information presented on the dashboard is generated using on-chain data as the source of truth.

We run a number of workers responsible for ingesting and normalising on-chain data and processing it to generate insights which are then reflected on the dashboard.

For each protocol an ingestion worker monitors the protocol supported chains looking for transactions and events relating to order deposits and fills. The filters for contract addresses, functions and events, as well as normalisation logic, are open source (stored within the intents_landscape repository) and we encourage contributions and corrections.

Of the ingested events (for simplicity we will call transactions and events just 'events' from now) workers normalise the data from the protocol specific format into a common internal format which is then used for matching orders to one or more bids. This normalised and processed dataset is then used to generate the stats, metrics and graphs on the dashboard each day.

## Environment setup

### Requirements

- Python 3.11
- pip (latest version recommended)

### Installation

```bash
# Create a virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Adding a protocol

To add a new protocol, you will need to fork the intents_landscape repo and add 3 new files (protocol filter python file, a static data file, and normalisation logic file) by following the steps in this section.

If updating you will also need to fork the repo, but will instead make changes to the relevant files for the protocol in question.

> Note : if the changes relate to a major new version of the protocol which has breaking changes either in contract address / function or event names, please consider instead adding the new version as a new protocol and not updating the existing protocol definition files.
>
> For example, for Across protocol there are two distinct versions that are each treated independently as `acrossv2` and `acrossv3`.

### Part 1: Add information about how to scrap data for the protocol

Using [protocol_data/\_example.py](https://github.com/AneraLabs/intents_landscape/blob/main/protocol_data/_example.py) as a template, copy this file and name it after the protocol you wish to add. Once this is done, provide the following information in the python file:

- Contract addresses for the protocol
- ABI (and/or function identifiers if needed) for referenced contracts
- Supported chains for protocol
- Deposit and fill function and event names

When specifying deposit information, only a deposit event is needed (deposit transactions are optional), however when providing fill information it is important to add a fill function name. Since most protocols will reject multiple transactions attempting to fill an already filled order, to accurately record multiple attempted or otherwise fills it is VERY IMPORTANT to add a fill function filter as reverted events will not be recorded on the blockchain. Only adding a fill event filter will not result in reverted txs being picked up and thus will not fully provide filler competitive dynamics data.

Once a new protocol has been added, make sure to add it to the ENABLE_PROTOCOLS key in [protocol_data/enabled_protocols.py](https://github.com/AneraLabs/intents_landscape/blob/main/protocol_data/enabled_protocols.py) .

### Part 2: Add static information about protocol

Using the relevant protocol entry in [protocols](https://github.com/AneraLabs/intents_landscape/tree/main/protocols) make the required changes.

Please be especially careful with the following fields as it's important to consider how the design of the protocol results in possible scores in these categories and clearly explain the justification.

- auction_design / auction_design_ranking / auction_design_details
- auction_openness / auction_openness_details
- filler_diversity / filler_diversity_details
- censorship_resistance / censorship_resistance_details
- filler_failure_resistance / filler_failure_resistance_details

The only accepted values for auction_openness, filler_diversity, censorship_resistance and filler_failure_resistance are `Excellent` / `Good` / `Average` / `Poor`.

## Contributions guidelines

All changes are accepted via PRs to the `staging` branch.

We happily accept contributions that improve the data we collect and add additional intent centric protocols whether or not they are live. For protocols that are on testnet we do not collect deposit and fill data and the stats do not contribute to the overall volume charts. Testnet protocols are shown in a different table.

We review all submissions to ensure that they meet the quality standards we expect in terms of:

- The code running correctly
- No inclusion of unnecessary or overly complex logic within filter code
- No additional dependencies, external calls or HTTP requests
- Protocol information being accurate
- Only making changes to ONE protocol per PR
