from dataclasses import dataclass


@dataclass
class Chain:
    _id: str
    name: str
    iconUrl: str


CHAINS = {
    '1': Chain('1', 'Ethereum', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '10': Chain('10', 'Optimism', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '137': Chain('137', 'Polygon', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '42161': Chain('42161', 'Arbitrum', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '8453': Chain('8453', 'Base', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '324': Chain('324', 'zkSync Era', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '7565164': Chain('7565164', 'Solana', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '43114': Chain('43114', 'Avalanche', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '56': Chain('56', 'BNB Chain', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '59144': Chain('59144', 'Linea', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '81457': Chain('81457', 'Blast', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '534352': Chain('534352', 'Scroll', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '1101': Chain('1101', 'Polygon zkEVM', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '5000': Chain('5000', 'Mantle', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '169': Chain('169', 'Manta', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '30': Chain('30', 'Rootstock', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '728126428': Chain('728126428', 'Tron', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '34443': Chain('34443', 'Mode', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '288': Chain('288', 'Boba Network', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '1088': Chain('1088', 'Metis', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
    '167000': Chain('167000', 'Taiko', 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'),
}


def get_chain_info(chain_id: str) -> Chain:
    return CHAINS[chain_id]