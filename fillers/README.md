# Intents Landscape Fillers

## Methodology for grouping filler addresses to names

- start with an address that we know for sure is that filler, (e.g. address
  [`0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010) belongs to `Across`)
- see if there were transactions from this address to other filler addresses
  (and if yes, add them to the list of addresses for that filler)

### Edge cases (need more research)

- `0x53323e9bE41473E747001CDe9076e6A2c29C1b3E` received funds from 3 fillers:

  - [`Across`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010)
  - [`DLN Trade`](https://platform.arkhamintelligence.com/explorer/address/0x555CE236C0220695b68341bc48C68d52210cC35b)
  - [`Synapse`](https://platform.arkhamintelligence.com/explorer/address/0xDc927Bd56CF9DfC2e3779C7E3D6d28dA1C219969)

- `0xeF1eC136931Ab5728B0783FD87D109c9D15D31F1` received funds from:

  - [`Across`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010)
  - [`DLN Trade`](https://platform.arkhamintelligence.com/explorer/address/0x555CE236C0220695b68341bc48C68d52210cC35b)

- known [`Nitro` filler](https://platform.arkhamintelligence.com/explorer/address/0x00051d55999c7cd91B17Af7276cbecD647dBC000) received funds from [`Across`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010)

- `0x74726F7574017B05A6aDCB2d4e11E7aDcF80F06C` received funds from [`Across`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010) but it was just one small transaction: more than half a year ago for about $150 (was not added to Across)

- `0xFe6f5EC250eb8513468600709e0ebE9C3D9ADB4A` received funds from:

  - [`Across`](https://platform.arkhamintelligence.com/explorer/address/0x428AB2BA90Eba0a4Be7aF34C9Ac451ab061AC010)
  - [`DLN Trade`](https://platform.arkhamintelligence.com/explorer/address/0x555CE236C0220695b68341bc48C68d52210cC35b) (more funds and more regular transactions from DLN Trade)

- `0x6eb459849f2C95a986f2620F4968C3Ef8498b786` received funds from:

  - [`DLN Trade`](https://platform.arkhamintelligence.com/explorer/address/0x555CE236C0220695b68341bc48C68d52210cC35b) (more funds and more regular transactions from DLN Trade)
  - [`Synapse`](https://platform.arkhamintelligence.com/explorer/address/0xDc927Bd56CF9DfC2e3779C7E3D6d28dA1C219969)
  - has associated DNS: `lalo1.eth`
