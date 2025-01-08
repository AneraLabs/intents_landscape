from dataclasses import dataclass


@dataclass(frozen=True)
class Chain:
    _id: str
    name: str
    icon_url: str
    average_block_time: float | None
    native_token_symbol: str = "ETH"
    native_token_icon_url: str = "https://icons.llamao.fi/icons/chains/rsz_ethereum.jpg"
    native_token_decimals: int = 18
    native_token_coingecko_id: str = "ethereum"


# https://github.com/DefiLlama/icons/tree/v2/assets/chains
CHAINS = {
    "1": Chain(
        "1", "Ethereum", "https://icons.llamao.fi/icons/chains/rsz_ethereum.jpg", 12.0
    ),
    "10": Chain(
        "10", "Optimism", "https://icons.llamao.fi/icons/chains/rsz_optimism.jpg", 2.0
    ),
    "137": Chain(
        "137",
        "Polygon",
        "https://icons.llamao.fi/icons/chains/rsz_polygon.jpg",
        2.0,
        native_token_symbol="MATIC",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_polygon.jpg",
        native_token_coingecko_id="matic-network",
    ),
    "42161": Chain(
        "42161",
        "Arbitrum",
        "https://icons.llamao.fi/icons/chains/rsz_arbitrum.jpg",
        0.26,
    ),
    "8453": Chain(
        "8453", "Base", "https://icons.llamao.fi/icons/chains/rsz_base.jpg", 2.0
    ),
    "324": Chain(
        "324",
        "zkSync Era",
        "https://icons.llamao.fi/icons/chains/rsz_zksync-era.jpg",
        1.1,
    ),
    "7565164": Chain(
        "7565164",
        "Solana",
        "https://icons.llamao.fi/icons/chains/rsz_solana.jpg",
        0.46,
        native_token_symbol="SOL",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_solana.jpg",
        native_token_decimals=9,
        native_token_coingecko_id="solana",
    ),
    "43114": Chain(
        "43114",
        "Avalanche",
        "https://icons.llamao.fi/icons/chains/rsz_avalanche.jpg",
        2.1,
        native_token_symbol="AVAX",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_avalanche.jpg",
        native_token_decimals=18,
        native_token_coingecko_id="avalanche-2",
    ),
    "56": Chain(
        "56",
        "BNB Chain",
        "https://icons.llamao.fi/icons/chains/rsz_binance.jpg",
        3.1,
        native_token_symbol="BNB",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_binance.jpg",
        native_token_coingecko_id="binancecoin",
    ),
    "59144": Chain(
        "59144", "Linea", "https://icons.llamao.fi/icons/chains/rsz_linea.jpg", 2.0
    ),
    # even though coingecko api says that the native token is BLAST
    # using ETH because the explorers show fees in ETH
    # example: https://blastexplorer.io/tx/0x07504f40b0a6487941d866b0eab374b4545be79aa84b47b06fb0b6d5d244a72c
    # block time is from https://cryptoapis.io/blockchains/blast
    "81457": Chain(
        "81457", "Blast", "https://icons.llamao.fi/icons/chains/rsz_blast.jpg", 2.0
    ),
    # https://scrollscan.com/
    "534352": Chain(
        "534352", "Scroll", "https://icons.llamao.fi/icons/chains/rsz_scroll.jpg", 2.96
    ),
    # https://zkevm.polygonscan.com/
    "1101": Chain(
        "1101",
        "Polygon zkEVM",
        "https://icons.llamao.fi/icons/chains/rsz_polygon-zkevm.jpg",
        3.0,
    ),
    # https://mantlescan.info/
    "5000": Chain(
        "5000",
        "Mantle",
        "https://icons.llamao.fi/icons/chains/rsz_mantle.jpg",
        None,
        native_token_symbol="MNT",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_mantle.jpg",
        native_token_decimals=18,
        native_token_coingecko_id="mantle",
    ),
    "169": Chain(
        "169", "Manta", "https://icons.llamao.fi/icons/chains/rsz_manta.jpg", 10.0
    ),
    # '30': Chain('30', 'Rootstock', 'https://icons.llamao.fi/icons/chains/rsz_rootstock.jpg',
    #             None,
    #             # TODO: verify RBTC has 18 decimals
    #             native_token_symbol='RBTC',
    #             native_token_icon_url='https://icons.llamao.fi/icons/chains/rsz_rootstock.jpg'),
    "728126428": Chain(
        "728126428",
        "Tron",
        "https://icons.llamao.fi/icons/chains/rsz_tron.jpg",
        3.0,
        native_token_symbol="TRX",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_tron.jpg",
        native_token_decimals=6,
        native_token_coingecko_id="tron",
    ),
    # even though coingecko api says that the native token is mode
    # block scanners show ETH
    # https://modescan.io/block/13469670
    "34443": Chain(
        "34443", "Mode", "https://icons.llamao.fi/icons/chains/rsz_mode.jpg", None
    ),
    # https://bobascan.com/
    "288": Chain(
        "288", "Boba Network", "https://icons.llamao.fi/icons/chains/rsz_boba.jpg", None
    ),
    # https://explorer.metis.io/
    "1088": Chain(
        "1088",
        "Metis",
        "https://icons.llamao.fi/icons/chains/rsz_metis.jpg",
        None,
        native_token_symbol="METIS",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_metis.jpg",
        native_token_decimals=18,
        native_token_coingecko_id="metis-token",
    ),
    # even though coingecko api says that the native token is taiko
    # block scanners show ETH
    # https://taikoscan.io/
    "167000": Chain(
        "167000", "Taiko", "https://icons.llamao.fi/icons/chains/rsz_taiko.jpg", None
    ),
    # https://blockscout.lisk.com/
    "1135": Chain(
        "1135",
        "Lisk",
        "https://coin-images.coingecko.com/coins/images/385/small/Lisk_logo.png?1722338450",
        2.0,
    ),
    # https://explorer.redstone.xyz/
    "690": Chain(
        "690",
        "Redstone",
        "https://raw.githubusercontent.com/blockscout/frontend-configs/main/configs/network-icons/redstone-light.svg",
        2.0,
    ),
    # https://explorer.zora.energy/
    "7777777": Chain(
        "7777777", "Zora", "https://icons.llamao.fi/icons/chains/rsz_zora.jpg", 2.0
    ),
    # https://evm-explorer.alephzero.org/
    "41455": Chain(
        "41455",
        "Aleph Zero",
        "https://icons.llamao.fi/icons/chains/rsz_aleph-zero-evm.png",
        3.5,
        native_token_symbol="AZERO",
        native_token_icon_url="https://icons.llamao.fi/icons/chains/rsz_aleph-zero-evm.png",
        native_token_decimals=12,
        native_token_coingecko_id="aleph-zero",
    ),
    # https://explorer.inkonchain.com/
    "57073": Chain(
        "57073", "Ink", "https://icons.llamao.fi/icons/chains/rsz_ink.jpg", 1.0
    ),
    "480": Chain(
        "480",
        "World Chain",
        "https://icons.llamao.fi/icons/chains/rsz_worldchain.png",
        2.0,
    ),
}


def get_chain_info(chain_id: str) -> Chain:
    return CHAINS[chain_id]


def is_supported(chain_id: str) -> bool:
    return chain_id in CHAINS


"""
Sources for average block times:
1. Ethereum: ~12 seconds (https://ethereum.org/en/developers/docs/blocks/)
2. Optimism: ~2 seconds (https://community.optimism.io/docs/developers/build/differences/)
3. Polygon: ~2 seconds (https://polygonscan.com/chart/blocktime)
4. Arbitrum: ~0.26 seconds (https://chainspect.app/chain/arbitrum)
5. Base: ~2 seconds (https://base.blockscout.com/stats)
6. zkSync Era: ~1.1 second (https://zksync.blockscout.com/)
7. Solana: ~0.46 seconds (https://chainspect.app/chain/solana)
8. Avalanche: ~2 seconds (https://chainspect.app/chain/avalanche)
9. BNB Chain: ~3 seconds (https://chainspect.app/chain/bnb-chain)
10. Linea: ~2 seconds (https://blockchair.com/linea)
11. Blast: ~2 seconds (https://mainnet.blastblockchain.com/)
12. Scroll: ~3 seconds (https://chainspect.app/chain/scroll)
13. Polygon zkEVM: ~3 seconds (https://zkevm.polygonscan.com/)
14. Mantle: https://docs.mantle.xyz/network/introduction/faqs#q.-whats-the-average-block-time-on-mantle-network
New blocks are generated on L2 every time a new transaction is received, and each 
block contains a single transaction. 
Thus, the block time on Mantle Network depends on the transaction volume 
at any given time.

15. Manta: ~10 seconds (https://pacific-explorer.manta.network/)
16. Rootstock: ?(https://dev.rootstock.io/kb/faqs/)
On average, the network currently generates a block every 30 seconds. 
Miners can reduce the average block time to 15 seconds by optimizing their 
merge-mining operations. 
Systems that receive payments over Rootstock in exchange for a good or service 
outside the Rootstock blockchain 
should wait a variable number of confirmation blocks, depending on the 
amount involved in the payments. 
A minimum of 12 confirmations is recommended, corresponding to 
an average delay of 6 minutes.


17. Tron: ~3 seconds (https://tronprotocol.github.io/documentation-en/introduction/dpos/)
18. Mode: - hard to find, https://modescan.io/ does not have the info
19. Boba - hard to find
20. Metis: - hard to find https://andromeda-explorer.metis.io/ does not have the info
21. Taiko: - hard to find, https://taikoscan.io/ looks like blocks are produced 
each 12 or 24 seconds
"""
