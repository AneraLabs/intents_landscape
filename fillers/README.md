# Intents Landscape Fillers

## Methodology for grouping filler addresses to names

- start with an address that we know for sure is that filler, (e.g. address
  [`0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010) belongs to `Across`)
- see if there were any direct transactions (without involving the protocol contract)
  from this address to other filler addresses
  (and if yes, add them to the list of addresses for that filler)

### Across

> known address: `0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010`

- `0xf7bAc63fc7CEaCf0589F25454Ecf5C2ce904997c`:
  - https://blastscan.io/tx/0x62615ef78418de38f42c81fbfa8d32a1d0c15d30ed0593904407e70c8b0fbf20
  - https://optimistic.etherscan.io/tx/0x7d432b3c14b2b8f44dee4983e7dfeeda5ce550e6fc1a432033621a2956c5937e
- `0x9A8f92a830A5cB89a3816e3D267CB7791c16b04D`:
  - https://lineascan.build/tx/0x1c15fadde173bb26d7994e59f9722252d5680038780565b385d8cbd468cdc2fe

### DLN Trade

> known address: `0x555CE236C0220695b68341bc48C68d52210cC35b`

- `0x2eF7604E98E9A3ae72A39CC9fc15234F48B4e93c`:
  - https://optimistic.etherscan.io/tx/0x4b308db20b3057efd0cb2284ea9a52455810ec0655c94f1fd677110c9a391584
