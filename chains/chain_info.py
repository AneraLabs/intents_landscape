from dataclasses import dataclass


@dataclass
class Chain:
    _id: str
    name: str
    icon_url: str


CHAINS = {
    '1': Chain('1', 'Ethereum', 'https://icons.llamao.fi/icons/chains/rsz_ethereum.jpg'),
    '10': Chain('10', 'Optimism', 'https://icons.llamao.fi/icons/chains/rsz_optimism.jpg'),
    '137': Chain('137', 'Polygon', 'https://icons.llamao.fi/icons/chains/rsz_polygon.jpg'),
    '42161': Chain('42161', 'Arbitrum', 'https://icons.llamao.fi/icons/chains/rsz_arbitrum.jpg'),
    '8453': Chain('8453', 'Base', 'https://icons.llamao.fi/icons/chains/rsz_base.jpg'),
    '324': Chain('324', 'zkSync Era', 'https://icons.llamao.fi/icons/chains/rsz_zksync-era.jpg'),
    '7565164': Chain('7565164', 'Solana', 'https://icons.llamao.fi/icons/chains/rsz_solana.jpg'),
    '43114': Chain('43114', 'Avalanche', 'https://icons.llamao.fi/icons/chains/rsz_avalanche.jpg'),
    '56': Chain('56', 'BNB Chain', 'https://icons.llamao.fi/icons/chains/rsz_binance.jpg'),
    '59144': Chain('59144', 'Linea', 'https://icons.llamao.fi/icons/chains/rsz_linea.jpg'),
    '81457': Chain('81457', 'Blast', 'https://icons.llamao.fi/icons/chains/rsz_blast.jpg'),
    '534352': Chain('534352', 'Scroll', 'https://icons.llamao.fi/icons/chains/rsz_scroll.jpg'),
    '1101': Chain('1101', 'Polygon zkEVM', 'https://icons.llamao.fi/icons/chains/rsz_polygon-zkevm.jpg'),
    '5000': Chain('5000', 'Mantle', 'https://icons.llamao.fi/icons/chains/rsz_mantle.jpg'),
    '169': Chain('169', 'Manta', 'https://icons.llamao.fi/icons/chains/rsz_manta.jpg'),
    '30': Chain('30', 'Rootstock', 'https://icons.llamao.fi/icons/chains/rsz_rootstock.jpg'),
    '728126428': Chain('728126428', 'Tron', 'https://icons.llamao.fi/icons/chains/rsz_tron.jpg'),
    '34443': Chain('34443', 'Mode', 'https://icons.llamao.fi/icons/chains/rsz_mode.jpg'),
    '288': Chain('288', 'Boba Network', 'https://icons.llamao.fi/icons/chains/rsz_boba.jpg'),
    '1088': Chain('1088', 'Metis', 'https://icons.llamao.fi/icons/chains/rsz_metis.jpg'),
    '167000': Chain('167000', 'Taiko', 'https://icons.llamao.fi/icons/chains/rsz_taiko.jpg'),
}


def get_chain_info(chain_id: str) -> Chain:
    return CHAINS[chain_id]

def is_supported(chain_id: str) -> bool:
    return chain_id in CHAINS