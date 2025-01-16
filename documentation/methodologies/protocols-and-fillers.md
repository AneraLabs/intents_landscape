# Protocols and Fillers

## Data sources

intent.markets has been created to provide transparent and verifiable insights into the emerging space of Intent based protocols. All information presented on the dashboard is generated using primary and secondary onchain data as the source of truth.

We run a number of workers responsible for ingesting and normalising on-chain data and processing it to generate insights which are then reflected on the dashboard.

For each protocol an ingestion worker monitors the protocol supported chains looking for transactions and events relating to order deposits and fills. The filters for contract addresses, functions and events, as well as normalisation logic, are open source and we encourage contributions and corrections (see Contribution section for more).

- Order Deposits - When users create new orders, we capture:
    - Source and destination chain information
    - Token addresses and amounts
    - Protocol-specific parameters
    - Transaction metadata (timestamps, block numbers, gas costs)
- Fill Attempts - We track both successful fills and failed attempts through:
    - Fill function calls (transactions)
    - Fill events (successful completions)
    - Filler addresses and competition pattern
- Filler balances - We collect ERC20 token balances for filler addresses that have been active on the tracked protocols for the last 7 days.

## Data normalisation

Each protocol implements its own order format and event structure. To enable cross-protocol analytics, we normalize this data into a standardized format through protocol-specific adapters. These normalised deposit events are then used for matching orders to one or more fill events. 

**## Order Matching**

After normalization, our matching service pairs deposit events with their corresponding fill attempts. The matching process:

- Links deposits to all associated fill attempts (both successful and failed)
- Validates that fills correspond to the original order parameters
- Tracks competition between fillers for the same order
- Handles protocol-specific matching rules

## Metrics calculation

Each matched order contains rich information about the transaction lifecycle, from initial deposit to final settlement. 

- The system monitors both successful fills and failed attempts, providing insight into protocol efficiency.
- Value calculations incorporate real-time price data to convert native token amounts into USD equivalents, enabling cross-protocol comparisons.
- The system measures execution performance by tracking the time delta between order creation and settlement.

For cross-chain activity, we track the flow of orders between chains by maintaining counters for each source-destination pair. The system aggregates these flows into route statistics, this helps identify both heavily-utilized routes and potential bottlenecks.

Each specific metric is then calculated aggregated by either protocol or filler address. Many protocols maintain a list of in-the-house filler addresses, that’s why on our website you will see for example “Synapse” being both a protocol and a filler name.