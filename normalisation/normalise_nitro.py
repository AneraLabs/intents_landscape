from eth_abi.abi import encode
from web3 import Web3

from normalisation.utils import normalise_address_if_needed


def chain_id_to_bytes(chain_id):
    return ("0x" + memoryview(str.encode(str(chain_id))).hex() + "0" * 66)[:66]


def strip_chain_id(string):
    return "".join(filter(str.isdigit, string))


def bytes_to_chain_id(byte_string):
    return strip_chain_id(bytearray.fromhex(byte_string[2:]).decode("utf-8"))


# used for default routes mapping
NITRO_TOKEN_ADDRESS_KEY = {
    "1": {
        "0xdAC17F958D2ee523a2206206994597C13D831ec7": "usdt",
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": "usdc",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "weth",
        "0x16ECCfDbb4eE1A85A33f3A9B21175Cd7Ae753dB4": "route",
    },
    "10": {
        "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85": "usdc",
        "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58": "usdt",
        "0x4200000000000000000000000000000000000006": "weth",
    },
    "30": {
        "0xef213441a85df4d7acbdae0cf78004e1e486bb96": "usdt",
    },
    "56": {
        "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d": "usdc",
        "0x55d398326f99059fF775485246999027B3197955": "usdt",
        "0x4DB5a66E937A9F4473fA95b1cAF1d1E1D62E29EA": "weth",
    },
    "137": {
        "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619": "weth",
        "0xc2132D05D31c914a87C6611C10748AEb04B58e8F": "usdt",
        "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174": "usdce",
        "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359": "usdc",
    },
    "169": {
        "0xf417F5A458eC102B90352F697D6e2Ac3A3d2851f": "usdt",
        "0xb73603C5d87fA094B7314C74ACE2e64D165016fb": "usdc",
        "0x0Dc808adcE2099A9F62AA87D9670745AbA741746": "weth",
    },
    "288": {
        "0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc": "usdc",
        "0x5DE1677344D3Cb0D7D465c10b72A8f60699C062d": "usdt",
        "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000": "weth",
    },
    "324": {
        "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4": "usdc",
        "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C": "usdt",
        "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91": "weth",
    },
    "1088": {
        "0xEA32A96608495e54156Ae48931A7c20f0dcc1a21": "usdc",
        "0xbB06DCA3AE6887fAbF931640f67cab3e3a16F4dC": "usdt",
    },
    "1101": {
        "0x1E4a5963aBFD975d8c9021ce480b42188849D41d": "usdt",
        "0xA8CE8aee21bC2A48a5EF670afCc9274C7bbbC035": "usdc",
        "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9": "weth",
    },
    "5000": {
        "0x09Bc4E0D864854c6aFB6eB9A9cdF58aC190D0dF9": "usdc",
        "0x201EBa5CC46D216Ce6DC03F6a759e8E766e956aE": "usdt",
        "0xdEAddEaDdeadDEadDEADDEAddEADDEAddead1111": "weth",
    },
    "8453": {
        "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913": "usdc",
        "0x4200000000000000000000000000000000000006": "weth",
    },
    "34443": {
        "0xd988097fb8612cc24eeC14542bC03424c656005f": "usdc",
        "0xf0F161fDA2712DB8b566946122a5af183995e2eD": "usdt",
        "0x4200000000000000000000000000000000000006": "weth",
    },
    "42161": {
        "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9": "usdt",
        "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": "usdc",
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": "weth",
    },
    "43114": {
        "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E": "usdc",
        "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7": "usdt",
        "0x8b82A291F83ca07Af22120ABa21632088fC92931": "weth",
    },
    "59144": {
        "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f": "weth",
        "0x176211869cA2b568f2A7D4EE941E073a821EE1ff": "usdc",
        "0xA219439258ca9da29E9Cc4cE5596924745e12B93": "usdt",
    },
    "81457": {
        "0x4300000000000000000000000000000000000004": "weth",
    },
    "534352": {
        "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4": "usdc",
        "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df": "usdt",
        "0x5300000000000000000000000000000000000004": "weth",
    },
    # "728126428": {
    #     "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t": "usdt",
    #     "TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8": "usdc",
    #     "TXWkP3jLBqRGojUih1ShzNyDaN5Csnebok": "weth"
    # },
    # https://developers.tron.network/docs/account#account-address-format
    # hex version of the base58 address
    # can be converted on https://www.btcschools.net/tron/tron_tool_base58check_hex.php
    "728126428": {
        "41a614f803b6fd780986a42c78ec9c7f77e6ded13c": "usdt",
        "413487b63d30b5b2c87fb7ffa8bcfade38eaac1abe": "usdc",
        "41ec51baf14488ec651270ccc409afda2818af74f2": "weth",
    },
}

nitro_token_name_key = {}  # Computed using `nitro_token_address_key`

for chain, tokens in NITRO_TOKEN_ADDRESS_KEY.items():
    for address, token_name in tokens.items():
        if chain not in nitro_token_name_key:
            nitro_token_name_key[chain] = {}
        nitro_token_name_key[chain][token_name] = address


def get_nitro_corresponding_dest_token(original_doc):
    dest_chain_id = bytes_to_chain_id(original_doc["event"]["destChainIdBytes"])

    if (
        original_doc["scraper_originChain"] not in NITRO_TOKEN_ADDRESS_KEY
        or original_doc["event"]["srcToken"]
        not in NITRO_TOKEN_ADDRESS_KEY[original_doc["scraper_originChain"]]
    ):
        print(
            f"Please add token matching for chain: "
            f"{original_doc['scraper_originChain']} "
            f"token_addr: {original_doc['event']['srcToken']} "
            f"hash: {original_doc['scraper_tx_hash']}"
        )
        return None

    src_token_name = NITRO_TOKEN_ADDRESS_KEY[original_doc["scraper_originChain"]][
        original_doc["event"]["srcToken"]
    ]

    if (
        dest_chain_id not in nitro_token_name_key
        or src_token_name not in nitro_token_name_key[dest_chain_id]
    ):
        print(
            f"Please add token matching for chain: {dest_chain_id} "
            f"token_name: {src_token_name} "
            f"hash: {original_doc['scraper_tx_hash']}"
        )
        return None

    dest_token_addr = nitro_token_name_key[dest_chain_id][src_token_name]

    return dest_token_addr


def is_valid_nitro(original_doc):
    """
    Fillers might send invalid data, example
    https://explorer.routernitro.com/tx/0x98e2103cdb02a73322e41578b4a24765716fd08c7204df4a3a25bd0a44e0ddea
    """
    try:
        if (
            "tx" in original_doc
            and "relayData" in original_doc["tx"]
            and "srcChainId" in original_doc["tx"]["relayData"]
        ):
            bytes_to_chain_id(original_doc["tx"]["relayData"]["srcChainId"])
        if "event" in original_doc and "destChainIdBytes" in original_doc["event"]:
            bytes_to_chain_id(original_doc["event"]["destChainIdBytes"])
    except Exception:
        return False
    return True


def normalise_nitro_dest_token(destination_token_address: str, original_doc: dict):
    if destination_token_address in {
        "0x0000000000000000000000000000000000000000",
        "0x",
    }:
        return get_nitro_corresponding_dest_token(original_doc)
    return destination_token_address


def normalise_nitro(original_doc, type, normalised_doc):
    if not is_valid_nitro(original_doc):
        return None

    # url = 'https://api-beta.pathfinder.routerprotocol.com/api/v2/status?srcTxHash=' +
    # original_doc['scraper_tx_hash']

    # max_retries = 10
    # retry_count = 0

    # while True:
    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         response_json = response.json()
    #         break
    #     except Exception as e:
    #         retry_timeout = min(2 ** retry_count, 32)
    #         retry_count += 1
    #         if retry_count > max_retries:
    #             print(f"Failed to fetch nitro dest token: {url}\nRetried {max_retries}
    #                    times, giving up.")
    #             return None
    #         print(f"Failed to fetch nitro dest token: {url}\nError: {e}\nRetrying
    #               {retry_count} / {max_retries} in {retry_timeout} seconds...")
    #         time.sleep(retry_timeout)

    # TODO: maybe get from https://sentry.lcd.routerprotocol.com/router-protocol/router-chain/multichain/contract_config

    chain_id_to_contract_address = {
        "1": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "534352": "0x01B4CE0d48Ce91eB6bcaf5dB33870C65d641b894",
        "324": "0x8B6f1C18c866f37e6EA98AA539e0C117E70178a2",
        "42161": "0xEF300Fb4243a0Ff3b90C8cCfa1264D78182AdaA4",
        "59144": "0x8C4aCd74Ff4385f3B7911432FA6787Aa14406f8B",
        "137": "0x1396F41d89b96Eaf29A7Ef9EE01ad36E452235aE",
        "81457": "0x21c1E74CAaDf990E237920d5515955a024031109",
        "10": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "43114": "0xF9f4C3dC7ba8f56737a92d74Fd67230c38AF51f2",
        "8453": "0x0Fa205c0446cD9EeDCc7538c9E24BC55AD08207f",
        "56": "0x260687eBC6C55DAdd578264260f9f6e968f7B2A5",
        "1101": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "5000": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "169": "0x21c1E74CAaDf990E237920d5515955a024031109",
        "30": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "728126428": "0x9D25B8289c0f3789237c1b3a88264882eeD6c610",
        "288": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "34443": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "1088": "0xC21e4ebD1d92036Cb467b53fE3258F219d909Eb9",
        "167000": "0x7bd616192fb2b364f9d29b2026165281a5f2ff2f",
    }

    def encode_bytes(
        input_amount,
        src_chain_id,
        deposit_id,
        dest_token,
        recipient,
        contract_address,
        message_bytes,
    ):
        return encode(
            ["uint256", "bytes32", "uint256", "address", "address", "address", "bytes"],
            [
                int(input_amount),
                bytearray.fromhex(src_chain_id[2:]),
                deposit_id,
                normalise_address_if_needed(dest_token),
                normalise_address_if_needed(recipient),
                normalise_address_if_needed(contract_address),
                bytearray.fromhex(message_bytes[2:]),
            ],
        )

    def get_message_hash(
        input_amount, src_chain_id, deposit_id, dest_token, recipient, contract_address
    ):
        def pad_addr(addr):
            return "0x" + addr[2:].rjust(64, "0")

        # pylint: disable=no-value-for-parameter
        return Web3.solidity_keccak(
            abi_types=["uint256", "bytes32", "uint256", "bytes", "bytes", "bytes"],
            values=[
                int(input_amount),
                src_chain_id,
                int(deposit_id),
                pad_addr(dest_token),
                pad_addr(recipient),
                pad_addr(contract_address),
            ],
        ).hex()

    # TODO: fix ruff warnings
    # ruff: noqa: PLR0913, PLR0917
    def get_message_hash_with_calldata(
        input_amount,
        src_chain_id,
        deposit_id,
        dest_token,
        recipient,
        contract_address,
        message_bytes,
    ):
        return Web3.keccak(
            encode_bytes(
                int(input_amount),
                src_chain_id,
                int(deposit_id),
                dest_token,
                recipient,
                contract_address,
                message_bytes,
            )
        ).hex()

    if type == "tx":
        if original_doc["scraper_function"] == "iRelay":
            normalised_doc["name"] = "order_fill_tx"

            normalised_doc["source_chain"] = bytes_to_chain_id(
                original_doc["tx"]["relayData"]["srcChainId"]
            )
            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["destination_address"] = normalise_address_if_needed(
                original_doc["tx"]["relayData"]["recipient"]
            )

            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["tx"]["relayData"]["destToken"]
            )

            normalised_doc["destination_token_amount"] = original_doc["tx"][
                "relayData"
            ]["amount"]

            normalised_doc["filler_address"] = original_doc["scraper_from"]
            normalised_doc["order_id"] = get_message_hash(
                original_doc["tx"]["relayData"]["amount"],
                original_doc["tx"]["relayData"]["srcChainId"],
                original_doc["tx"]["relayData"]["depositId"],
                original_doc["tx"]["relayData"]["destToken"],
                original_doc["tx"]["relayData"]["recipient"],
                original_doc["scraper_contractAddress"],
            )
        elif original_doc["scraper_function"] == "iRelayMessage":
            normalised_doc["name"] = "order_fill_tx"

            normalised_doc["source_chain"] = bytes_to_chain_id(
                original_doc["tx"]["relayData"]["srcChainId"]
            )
            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["destination_address"] = original_doc["tx"]["relayData"][
                "recipient"
            ]

            normalised_doc["destination_token_address"] = normalise_address_if_needed(
                original_doc["tx"]["relayData"]["destToken"]
            )

            normalised_doc["destination_token_amount"] = original_doc["tx"][
                "relayData"
            ]["amount"]

            normalised_doc["filler_address"] = original_doc["scraper_from"]
            normalised_doc["order_id"] = get_message_hash_with_calldata(
                original_doc["tx"]["relayData"]["amount"],
                original_doc["tx"]["relayData"]["srcChainId"],
                original_doc["tx"]["relayData"]["depositId"],
                original_doc["tx"]["relayData"]["destToken"],
                original_doc["tx"]["relayData"]["recipient"],
                original_doc["scraper_contractAddress"],
                original_doc["tx"]["relayData"]["message"],
            )
        else:
            print(f"Unknown function type {original_doc['scraper_function']}")
            return None

    elif type == "event":
        if original_doc["scraper_event"] == "FundsDeposited":
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )

            normalised_doc["source_address"] = original_doc["event"]["depositor"]
            normalised_doc["destination_address"] = original_doc["event"]["recipient"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["srcToken"]
            )
            normalised_doc["destination_token_address"] = normalise_nitro_dest_token(
                original_doc["event"]["destToken"], original_doc
            )

            normalised_doc["source_token_amount"] = original_doc["event"]["amount"]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "destAmount"
            ]

            destination_chain = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )
            if destination_chain not in chain_id_to_contract_address:
                print(
                    f"Nitro contract address for chain id {destination_chain} "
                    "not found, skipping"
                )
                return None

            destination_chain_contract_address = chain_id_to_contract_address[
                destination_chain
            ]

            if normalised_doc["destination_token_address"] is None:
                print(
                    "Could not normalise destination token address for nitro doc: "
                    f'[{original_doc.get("_id", "N/A")}], skipping document...'
                )
                return None

            normalised_doc["order_id"] = get_message_hash(
                normalised_doc["destination_token_amount"],
                chain_id_to_bytes(original_doc["scraper_originChain"]),
                original_doc["event"]["depositId"],
                normalised_doc["destination_token_address"],
                original_doc["event"]["recipient"],
                destination_chain_contract_address,
            )

        elif original_doc["scraper_event"] == "FundsPaid":
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["order_id"] = original_doc["event"]["messageHash"]
            normalised_doc["filler_address"] = original_doc["event"]["forwarder"]

        elif original_doc["scraper_event"] == "FundsDepositedWithMessage":
            normalised_doc["name"] = "order_deposit_event"

            normalised_doc["source_chain"] = original_doc["scraper_originChain"]
            normalised_doc["destination_chain"] = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )

            normalised_doc["source_address"] = original_doc["event"]["depositor"]
            normalised_doc["destination_address"] = original_doc["event"]["recipient"]

            normalised_doc["source_token_address"] = normalise_address_if_needed(
                original_doc["event"]["srcToken"]
            )
            normalised_doc["destination_token_address"] = normalise_nitro_dest_token(
                original_doc["event"]["destToken"], original_doc
            )

            normalised_doc["source_token_amount"] = original_doc["event"]["amount"]
            normalised_doc["destination_token_amount"] = original_doc["event"][
                "destAmount"
            ]

            destination_chain = bytes_to_chain_id(
                original_doc["event"]["destChainIdBytes"]
            )
            destination_chain_contract_address = chain_id_to_contract_address[
                destination_chain
            ]

            if not destination_chain_contract_address:
                print(
                    f"Nitro contract address for chain id "
                    f"[{destination_chain}] not found"
                )
                return None

            if normalised_doc["destination_token_address"] is None:
                print(
                    f'Could not normalise destination token address for nitro doc: '
                    f'[{original_doc.get("_id", "N/A")}], skipping document...'
                )
                return None

            normalised_doc["order_id"] = get_message_hash_with_calldata(
                normalised_doc["destination_token_amount"],
                chain_id_to_bytes(original_doc["scraper_originChain"]),
                original_doc["event"]["depositId"],
                normalised_doc["destination_token_address"],
                original_doc["event"]["recipient"],
                destination_chain_contract_address,
                original_doc["event"]["message"],
            )

        elif original_doc["scraper_event"] == "FundsPaidWithMessage":
            normalised_doc["name"] = "order_fill_event"

            normalised_doc["destination_chain"] = original_doc["scraper_originChain"]

            normalised_doc["order_id"] = original_doc["event"]["messageHash"]
            normalised_doc["filler_address"] = original_doc["event"]["forwarder"]

        else:
            print(f"Unknown event type {original_doc['scraper_event']}")
            return None

    # approximate gas paid for claim events
    if normalised_doc["name"] in {"order_fill_tx", "order_fill_event"}:
        # nitro claim happens on their own chain
        normalised_doc["scraper_claim_gas_paid_usd"] = 0.01

    return normalised_doc


# ruff: noqa: E501
if __name__ == "__main__":
    event = {
        "_id": {
            "protocol": "nitro",
            "origin_chain_id": "10",
            "tx_hash": "10e5aa6666eab0154410c220f496ec35542f3b6c73bfa69d69c3c0407cb53549",
            "protocol_order_id": "0xc8fc4831e6dd256954120f01c4a1783ed04f89bc54526981fd65f1f601ac6f19",
        },
        "scraper_originChain": "10",
        "scraper_blockNumber": 126094746,
        "scraper_tx_hash": "10e5aa6666eab0154410c220f496ec35542f3b6c73bfa69d69c3c0407cb53549",
        "scraper_blockTimestamp": 1727788269,
        "scraper_protocol": "nitro",
        "scraper_contractAddress": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_event": "FundsPaid",
        "scraper_from": "0x00051d55999c7cd91B17Af7276cbecD647dBC000",
        "scraper_to": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_effectiveGasPrice": "1359600",
        "scraper_gasUsed": "89643",
        "event": {
            "messageHash": "0xc8fc4831e6dd256954120f01c4a1783ed04f89bc54526981fd65f1f601ac6f19",
            "forwarder": "0x00051d55999c7cd91B17Af7276cbecD647dBC000",
            "nonce": "171974",
        },
    }

    normalised_doc = {
        "scraper_originChain": "10",
        "scraper_blockNumber": 126094746,
        "scraper_tx_hash": "10e5aa6666eab0154410c220f496ec35542f3b6c73bfa69d69c3c0407cb53549",
        "scraper_blockTimestamp": 1727788269,
        "scraper_protocol": "nitro",
        "scraper_contractAddress": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_event": "FundsPaid",
        "scraper_from": "0x00051d55999c7cd91B17Af7276cbecD647dBC000",
        "scraper_to": "0x8201c02d4AB2214471E8C3AD6475C8b0CD9F2D06",
        "scraper_effectiveGasPrice": "1359600",
        "scraper_gasUsed": "89643",
    }

    normalised_doc = normalise_nitro(event, "event", normalised_doc)
    print(normalised_doc)
