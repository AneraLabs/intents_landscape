# Introduction

All data on the dashboard is built from open sources that can be contributed to by anyone to update existing protocols, add new ones, or correct mistakes to improve the quality of the data we provide.

Spotted a mistake? Want to add a new intent-based protocol? We are grateful for all contributions—this page explains how to contribute.

# How the dashboard gets data

The Intents dashboard has been created to provide transparent and verifiable insights into the emerging space of intent-based protocols. As such, all information presented is generated using on-chain data as the source of truth.

We run a number of workers responsible for ingesting and normalizing on-chain data and processing it to generate insights which are then reflected on the dashboard.

For each protocol, an ingestion worker monitors the protocol-supported chains looking for transactions and events relating to order deposits and fills. The filters for contract addresses, functions, and events are open source (stored within the [intents_landscape](https://github.com/AneraLabs/intents_landscape) repository) and we encourage contributions and corrections.

Of the ingested events (for simplicity we will call transactions and events just 'events' from now), workers normalize the data from the protocol-specific format into a common internal format which is then used for matching orders to one or more bids. This normalized and processed dataset is then used to generate the stats, metrics, and graphs on the dashboard each day.

# Adding a new protocol

To add a new protocol, you will need to fork the [intents_landscape](https://github.com/AneraLabs/intents_landscape) repo and add two new files (protocol filter Python file and a static data file) by following the steps in this section.

If updating, you will also need to fork the repo, but will instead make changes to the relevant files for the protocol in question.

## Part 1: Add information about how to scrape data for the protocol

Using [_example.py](https://github.com/AneraLabs/intents_landscape/blob/main/protocol_data/_example.py) as a template, copy this file and name it after the protocol you wish to add. Once this is done, provide the following information in the Python file:

- Contract addresses for the protocol
- ABI (and/or function identifiers if needed) for referenced contracts
- Supported chains for the protocol
- Deposit and fill function and event names

When specifying deposit information, only a deposit event is needed (deposit transactions are optional). However, when providing fill information it is important to add a fill function name. Since most protocols will reject multiple transactions attempting to fill an already filled order, to accurately record multiple attempted (or otherwise) fills it is **VERY IMPORTANT** to add a fill function filter as reverted events will not be recorded on the blockchain. Only adding a fill event filter will not result in reverted transactions being picked up and thus will not fully provide filler competitive dynamics data.

Once a new protocol has been added, make sure to add it to the `ENABLE_PROTOCOLS` key in [enabled_protocols.py](https://github.com/AneraLabs/intents_landscape/blob/main/protocol_data/enabled_protocols.py).

## Part 2: Add static information about the protocol

Using the relevant protocol entry in [intents_landscape](https://github.com/AneraLabs/intents_landscape/tree/main/protocols), make the required changes.

Please be especially careful with the following fields as it's important to consider carefully how the design of the protocol results in possible scores in these categories and clearly explain the justification.

- `auction_design` / `auction_design_ranking` / `auction_design_details`
- `auction_openness` / `auction_openness_details`
- `filler_diversity` / `filler_diversity_details`
- `censorship_resistance` / `censorship_resistance_details`
- `filler_failure_resistance` / `filler_failure_resistance_details`

The only accepted values for `auction_openness`, `filler_diversity`, `censorship_resistance`, and `filler_failure_resistance` are **Excellent**, **Good**, **Average**, **Poor**.

## Part 3: Submit a PR

After double-checking the steps above to ensure the submission is valid (also see [Contributions guidelines](#contributions-guidelines)), please open a PR to merge your changes to the `main` branch. Please only make changes to **ONE** protocol per PR.

# Updating an existing protocol

To update information about an existing protocol, you will need to fork the [intents_landscape](https://github.com/AneraLabs/intents_landscape) and make changes to the relevant files for the protocol in question.

Note: If the changes relate to a major new version of the protocol which has breaking changes either in contract address, function, or event names, please consider instead adding the new version as a new protocol and not updating the existing protocol definition files.

For example, for Across protocol there are two distinct versions that are each treated independently as `acrossv2` and `acrossv3`.

## Part 1: Add information about how to scrape data for the protocol

If the changes relate to metadata or general information about the protocol, skip to Part 2.

Using the relevant protocol entry in [protocol_data](https://github.com/AneraLabs/intents_landscape/tree/main/protocol_data), make the required changes to any of the following:

- Contract addresses for the protocol
- ABI (and/or function identifiers if needed) for referenced contracts
- Supported chains for the protocol
- Deposit and fill function and event names

When specifying deposit information, only a deposit event is needed (deposit transactions are optional). However, when providing fill information it is important to add a fill function name. Since most protocols will reject multiple transactions attempting to fill an already filled order, to accurately record multiple attempted (or otherwise) fills it is **VERY IMPORTANT** to add a fill function filter as reverted events will not be recorded on the blockchain. Only adding a fill event filter will not result in reverted transactions being picked up and thus will not fully provide filler competitive dynamics data.

## Part 2: Add static information about the protocol

Using the relevant protocol entry in [intents_landscape](https://github.com/AneraLabs/intents_landscape/tree/main/protocols), make the required changes.

Please be especially careful with the following fields as it’s important to consider carefully how the design of the protocol results in possible scores in these categories and clearly explain the justification.

- `auction_design` / `auction_design_ranking` / `auction_design_details`
- `auction_openness` / `auction_openness_details`
- `filler_diversity` / `filler_diversity_details`
- `censorship_resistance` / `censorship_resistance_details`
- `filler_failure_resistance` / `filler_failure_resistance_details`

The only accepted values for `auction_openness`, `filler_diversity`, `censorship_resistance`, and `filler_failure_resistance` are **Excellent**, **Good**, **Average**, **Poor**.

## Part 3: Submit a PR

After double-checking the steps above to ensure the submission is valid (also see [Contributions guidelines](#contributions-guidelines)), please only make changes to **ONE** protocol per PR.

# Contributions guidelines

We happily accept contributions that improve the data we collect and add additional intent-centric protocols whether or not they are live. For protocols that are on testnet, we do not collect deposit and fill data and the stats do not contribute to the overall volume charts. Testnet protocols are shown in a different table.

We review all submissions to ensure that they meet the quality standards we expect in terms of:

- The code running correctly
- No inclusion of unnecessary or overly complex logic within filter code
- No additional dependencies, external calls, or HTTP requests
- Protocol information being accurate
