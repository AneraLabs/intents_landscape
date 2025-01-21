import hashlib

import base58
from web3 import Web3


def _bytes_as_hex_str(value):
    if isinstance(value, bytes):
        return "0x" + value.hex()
    elif isinstance(value, dict):
        for key, inner_value in value.items():
            value[key] = _bytes_as_hex_str(inner_value)
    elif isinstance(value, list):
        for i in range(len(value)):
            value[i] = _bytes_as_hex_str(value[i])
    return value


def bytes_as_hex_str(doc: dict):
    for key, value in doc.items():
        doc[key] = _bytes_as_hex_str(value)


def stringify_numeric_values(data, key: str | None = None):
    """
    Fixes errors like: OverflowError: MongoDB can only handle up to 8-byte ints
    """
    # other logic depends on these fields being numeric
    if key is not None and (
        key.endswith("_usd")
        or key in {"scraper_blockNumber", "scraper_blockTimestamp", "decimals"}
    ):
        return data

    if isinstance(data, dict):
        return {
            key: stringify_numeric_values(value, key) for key, value in data.items()
        }
    elif isinstance(data, list):
        return [stringify_numeric_values(item) for item in data]
    # should be checked before int (True/False is an instance of int in Python)
    elif isinstance(data, bool):
        return data
    elif isinstance(data, int):
        # floats are fine, only large ints give the error
        return str(data)
    else:
        return data


def normalise_address_if_needed(address):
    if address == "0x":
        return "0x0000000000000000000000000000000000000000"
    return address


# from https://ethereum.org/en/developers/docs/standards/tokens/erc-20/#web3py-example
ERC20_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
        "constant": True,
    },
]
ETH_ADDRESS_LENGTH = 42
TRON_ADDRESS_LENGTH = 34


def is_eth_address(address):
    return address.startswith("0x") and len(address) == ETH_ADDRESS_LENGTH


def is_valid_tron_address(address: str) -> bool:
    if not address.startswith("T"):
        return False
    if len(address) != TRON_ADDRESS_LENGTH:
        return False
    try:
        base58.b58decode_check(address)
        return True
    except:  # noqa: E722
        return False


def safe_checksum_address(address: str) -> str:
    if is_valid_tron_address(address):
        address = tron_to_hex(address)
    if is_eth_address(address):
        return Web3.to_checksum_address(address)
    return address


# https://www.reddit.com/r/Tronix/comments/ja8khn/convert_my_address/
def hex_to_tron(hexaddr):
    hexaddr = "41" + hexaddr.replace("0x", "")
    checksum = (
        hashlib.sha256(hashlib.sha256(bytes.fromhex(hexaddr)).digest())
        .digest()[0:4]
        .hex()
    )
    addrchecksum = hexaddr + checksum
    base58addr = base58.b58encode(bytes.fromhex(addrchecksum)).decode("utf-8")
    return base58addr


def tron_to_hex(tronaddr):
    addrchecksum = base58.b58decode(tronaddr).hex()
    address = addrchecksum[0:42]
    checksum = (
        hashlib.sha256(hashlib.sha256(bytes.fromhex(address)).digest())
        .digest()[0:4]
        .hex()
    )
    if checksum != addrchecksum[42:]:
        raise ValueError("Invalid checksum")
    address = address.replace("41", "0x", 1)
    address = Web3.to_checksum_address(address)
    return address


if __name__ == "__main__":
    assert (
        hex_to_tron("0xa614f803b6fd780986a42c78ec9c7f77e6ded13c")
        == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    )
    assert (
        hex_to_tron("0xa614f803B6FD780986A42c78Ec9c7f77e6DeD13C")
        == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    )
    assert (
        tron_to_hex("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
        == "0xa614f803B6FD780986A42c78Ec9c7f77e6DeD13C"
    )
