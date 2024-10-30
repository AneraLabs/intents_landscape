# Intent

Rather than crafting and signing a transaction that will result in a state change on chain with a complete declaration of how such a state change will occur, an **Intent** is a signed set of conditionals that specify what a user wants to occur, but leaves the details of how entirely to a protocol and solver.

This is a powerful notion as it decouples the what from the how, allowing specialised entities called Solvers to compute and be rewarded for helping a user find the best way to fulfil an order or provide a service to satisfy their expressed conditionals.

# FCFS

An acronym for **First Come First Served**, used to describe a type of protocol auction system designed for speed of execution where the first bid that comes in from a filler will be accepted for an order as long as it meets the minimum requirements.

This auction type favours order execution speed at the expense of order competitiveness. The first bidder will be accepted irrespective of whether another bid comes afterwards which would have resulted in a better fill price for an order.

# RFQ

An acronym for **Request For Quote**, a mechanism used in auctions to solicit bids for an order within a certain time period. In contrast to FCFS, orders take slightly longer to execute because a fixed time window is always allowed for fillers to submit bids. Conceptually, this creates competition between Fillers who compete on the basis of the execution quality of their bid, resulting in a better price for the order overall.

RFQ auctions are typically run as a **First-price sealed-bid auction (FPSBA)** to hide each bid made by a Filler and promote fairness during the auction period. Once the auction window has closed, the winner that results in the greatest execution quality or best price for the order is nominated to fill the order.

# Protocol

Term used to describe either the dApp generally or the mechanism/architecture it uses to facilitate operation of the platform.

# Fillers

Arguably one of the most important actors in the intent-centric model, **Fillers** listen to orders that express intents submitted by users via Intent protocols and propose bids to satisfy the order. Fillers are vital to protocols as they connect the dots between the inputs and outputs.

# Filler competition

Orders typically can only be filled by a single entity called a Filler. When multiple fillers compete to fill an order, they do so by each attempting to win the order by providing the most compelling bid. Competition for order flow between Fillers drives the equilibrium towards better execution quality for the order originator, meaning they are likely to get a better price or pay a lower fee for their order.

Where orders are uncontested, there is no driving force for Fillers to offer competitive bids to win an auction. This results in worse execution quality (and thus outcome for the order originator) and higher surplus, which is consumed by the Filler as a service fee.

# Execution quality

Intent-based orders specify the actions that should be performed and the minimum acceptable outcome. Conceptually similar to slippage on AMM markets, the minimum acceptable outcome could be, for example, the minimum price accepted in a swap or the minimum amount that should be sent on another chain to a particular address.

The difference between the input and output (if a single token operation) or the current exchange rate between (if a multi-token operation) is the maximum fee (or loss) the user is willing to incur to have the operation executed.

**Execution quality** is the difference between the minimum acceptable outcome for an order and the greatest theoretical outcome.

# Protocol Censorship

Within decentralised systems, there is equal access to services for all participants. Blockchain transactions (assuming appropriate miner/validator fees are paid to warrant inclusion) are an example of where any address or participant has a theoretically equal opportunity to perform an action. Unfortunately, between the cost of implementing auctions entirely on-chain and the reliance on cross-chain messaging and synchronisation mechanisms, most protocols have complex designs that exist at least in some form off-chain.

Protocols that perform some of the calculation or execution logic off-chain (i.e., not entirely on a single chain using a smart contract) introduce a potential source of centralisation. Centralisation negates the guarantees of a decentralised system where if only a single participant is acting honestly and rationally, there is a level playing field for all.

Depending on the design of a protocol, centralisation can occur through multiple mechanisms like off-chain order advertising, order-bid matching, auction execution, cross-chain message passing, permissioned relayers or executors, and others.

The consequences of protocol censorship can range from denial of service prior to funds being in flight through to denial of fulfilment with funds effectively frozen in transit. The mechanisms and risk factors relate to individual protocol architectures and design choices
