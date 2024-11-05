import struct
from abc import ABC, abstractmethod
from typing import Protocol

import base58
from solders.rpc.responses import GetTransactionResp
from solders.signature import Signature
from solders.transaction_status import ParsedAccount, UiPartiallyDecodedInstruction

UNPARSED_INSTRUCTION_FIELD_NAME = "unparsed_instruction_data"

SET_COMPUTE_UNIT_LIMIT_OPCODE = 2
SET_COMPUTE_UNIT_PRICE_OPCODE = 3


def decode_compute_budget_instruction(data):
    # Unpack the first byte to determine the opcode
    opcode = data[0]
    if opcode == SET_COMPUTE_UNIT_LIMIT_OPCODE:
        value = struct.unpack("<I", data[1:5])[
            0
        ]  # Unpack 4-byte integer (little-endian)
        return opcode, value
    elif opcode == SET_COMPUTE_UNIT_PRICE_OPCODE:
        # SetComputeUnitPrice takes in micro lamports
        # https://github.com/solana-labs/solana/blob/ced8f6a512c61e0dd5308095ae8457add4a39e94/program-runtime/src/prioritization_fee.rs#L1-L2
        value = struct.unpack("<Q", data[1:9])[
            0
        ]  # Unpack 8-byte integer (little-endian)
        return opcode, value
    else:
        # more instructions to parse
        # https://github.com/solana-labs/solana/blob/master/sdk/src/compute_budget.rs
        return 0, 0


def get_prioritization_fee(tx):
    instructions = tx.value.transaction.transaction.message.instructions
    # https://solana.com/docs/core/fees#prioritization-fees
    # calculated by multiplying its compute unit limit by the compute unit price
    compute_budget_program_id = "ComputeBudget111111111111111111111111111111"

    # If no SetComputeUnitLimit instruction is provided, the default compute unit limit
    # will be used.
    compute_unit_limit = 200_000

    # If no SetComputeUnitPrice instruction is provided, the transaction will default
    # to no additional elevated fee and the lowest priority (i.e. no prioritization fee)
    compute_unit_price = 0

    for instruction in instructions:
        if str(instruction.program_id) == compute_budget_program_id:
            decoded_data = base58.b58decode(instruction.data)
            opcode, value = decode_compute_budget_instruction(decoded_data)
            if opcode == SET_COMPUTE_UNIT_LIMIT_OPCODE:
                compute_unit_limit = value
            elif opcode == SET_COMPUTE_UNIT_PRICE_OPCODE:
                # convert to lamports
                compute_unit_price = value / 1_000_000

    return round(compute_unit_limit * compute_unit_price)


class Parseable(Protocol):
    def parse(self, data: bytes) -> dict: ...


class BaseSolanaParser(ABC):
    @property
    @abstractmethod
    def protocol_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def program_address(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def schema(self) -> Parseable:
        raise NotImplementedError

    def parse_protocol_specific_fields(  # noqa: PLR6301
        self,
        tx: GetTransactionResp,
        instruction: UiPartiallyDecodedInstruction,
        parsed_instruction_data: dict | None,
        doc: dict,
    ) -> dict:
        return doc

    def is_relevant_instruction(self, instruction) -> bool:
        return str(instruction.program_id) == self.program_address

    def parse_instruction(
        self,
        signature: Signature,
        tx: GetTransactionResp,
        instruction: UiPartiallyDecodedInstruction,
        doc: dict,
    ) -> dict | None:
        """
        Parse the common for most protocols fields of the transaction
        and the instruction.
        All fields of the resulting document can be overwritten
        in the parse_protocol_specific_fields.
        """

        # the inner tx object contains parsed instruction data
        try:
            data = self.schema.parse(base58.b58decode(instruction.data.encode()))
            return data

        except Exception as e:
            print(f"Failed to parse data for [{signature}] : [{e}]")
            # mark docs that have unknown instructions for possible future fix
            doc[UNPARSED_INSTRUCTION_FIELD_NAME] = instruction.data
            return None

    # TODO: fix ruff warnings
    # ruff: noqa: PLR0912
    def parse_transaction(
        self, chain_id: str, signature: Signature, tx: GetTransactionResp
    ) -> dict | None:
        if tx.value is None:
            return None

        tx_data = tx.value.transaction.transaction
        tx_meta = tx.value.transaction.meta
        if tx_meta is None or tx_data is None:
            return None

        message = tx_data.message  # type: ignore[attr-defined]

        doc = {}

        doc["scraper_protocol"] = self.protocol_name
        doc["scraper_originChain"] = chain_id
        doc["scraper_blockNumber"] = tx.value.slot
        doc["scraper_blockTimestamp"] = tx.value.block_time
        scraper_from = message.account_keys[0]
        if isinstance(scraper_from, ParsedAccount):
            doc["scraper_from"] = str(scraper_from.pubkey)
        else:
            doc["scraper_from"] = str(scraper_from)
        doc["scraper_contractAddress"] = self.program_address
        doc["scraper_tx_status"] = "reverted" if tx_meta.err is not None else "ok"
        doc["scraper_tx_hash"] = str(signature)

        doc["scraper_chain_fee"] = tx_meta.fee
        doc["scraper_chain_prioritization_fee"] = get_prioritization_fee(tx)

        parsed_instruction_data = None

        for instruction in message.instructions:
            if self.is_relevant_instruction(instruction):
                doc["instruction_type"] = "outer_instruction"
                parsed_instruction_data = self.parse_instruction(
                    signature,
                    tx,
                    instruction,  # type: ignore
                    doc,
                )
                break

        if (
            tx_meta.inner_instructions is not None
            and parsed_instruction_data is None
            and UNPARSED_INSTRUCTION_FIELD_NAME not in doc
        ):
            for inner_instruction in tx_meta.inner_instructions:
                for instruction in inner_instruction.instructions:
                    if self.is_relevant_instruction(instruction):
                        doc["instruction_type"] = "inner_instruction"
                        parsed_instruction_data = self.parse_instruction(
                            signature,
                            tx,
                            instruction,  # type: ignore
                            doc,
                        )
                        break

        if (
            UNPARSED_INSTRUCTION_FIELD_NAME not in doc
            and parsed_instruction_data is None
        ):
            # we didn't find any relevant instructions
            return None

        if parsed_instruction_data is not None and isinstance(
            instruction, UiPartiallyDecodedInstruction
        ):
            doc = self.parse_protocol_specific_fields(
                tx, instruction, parsed_instruction_data, doc
            )
            return doc
        else:
            print(f"Unexpected parsed_instruction_data for [{signature}]")
            return None
