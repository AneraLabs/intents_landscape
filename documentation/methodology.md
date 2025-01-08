# Liquidity Provisions

Our data collection and processing methodology is designed to provide real-time insights into DeFi protocol activities. We focus on major protocols including **Uniswap V2/V3**, **Curve**, and **Balancer V2**, tracking their on-chain activities through a two-phase approach.

## Blockchain Data Ingestion

For each protocol, we track specific events like:

- Swaps
- Liquidity additions/removals
- Fee collections
- Price updates

## Aggregating Data into Daily Buckets

To ensure precise metrics calculations, we implement **real-time token balance tracking at the block level**. When relevant events occur, our system captures the current state of pool balances, maintaining historical data for comprehensive analysis.

In the metrics processing phase, we calculate these core intermediate step aggregations:

- Trading volume
- Value locked
- Fees
- The deltas of token amounts that happen within each block due to trading activity (called **swap deltas**)

The system aggregates data into time-based buckets (daily) and uses these aggregations to calculate two important metrics: **APY** and **utilization rate**.

## Metrics Calculation

### Annual Percentage Yield (APY)

Annual Percentage Yield (APY) is calculated by analyzing the relationship between fees earned and value locked in the protocol. For each time bucket, we:

1. Take the total fees collected in USD.
2. Divide it by the average total value locked (TVL) during that period.
3. Annualize the daily rate by multiplying by 365.
4. Convert the result to a percentage.

This calculation gives liquidity providers an understanding of their potential returns on an annual basis.

### Utilization Rate

The utilization rate provides insight into how actively a pool's liquidity is being used. It is calculated by:

1. Comparing the average **swap delta** (the net change in token amounts from trading activity) against the average total value locked (TVL) in the pool.
2. Expressing this ratio as a percentage, where a higher percentage indicates more active usage of the available liquidity.

For example, if a pool with $1 million in liquidity processes $100,000 in swap deltas during a period, its utilization rate would be **10%**.

## Protocol Comparisons and Accuracy

Both metrics are calculated across all supported protocols, with the system maintaining separate aggregations for each protocol and token set. Data for different pools is averaged within a protocol, allowing for detailed comparisons of protocol performance among each other.

To ensure accuracy, the system calculates these metrics only when there is sufficient data—specifically, when both TVL measurements and swap activities are recorded in a given time bucket. This prevents misleading results that could arise from incomplete or anomalous data.
