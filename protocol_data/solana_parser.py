from abc import ABC, abstractmethod
from typing import Protocol

import base58
import struct
from solders.signature import Signature
from solders.rpc.responses import GetTransactionResp
from solders.transaction_status import UiPartiallyDecodedInstruction
from solders.transaction_status import ParsedAccount

UNPARSED_INSTRUCTION_FIELD_NAME = "unparsed_instruction_data"

class Parseable(Protocol):
    def parse(self, data: bytes) -> dict:
        ...

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
    
    @property
    @abstractmethod
    def identifier(self) -> str:
        raise NotImplementedError

    def parse_protocol_specific_fields(self, tx: GetTransactionResp, instruction: UiPartiallyDecodedInstruction,  doc: dict) -> dict:
        return doc
    
    def is_relevant_instruction(self, instruction) -> bool:
        has_parsable_data = isinstance(instruction, UiPartiallyDecodedInstruction)
        if not has_parsable_data:
            return False
        decoded_data_hex = base58.b58decode(instruction.data.encode()).hex()
        return str(instruction.program_id) == self.program_address and decoded_data_hex.startswith(self.identifier)
    
    def decode_compute_budget_instruction(self, data):
        # Unpack the first byte to determine the opcode
        opcode = data[0]
        if opcode == 2:  # SetComputeUnitLimit
            value = struct.unpack('<I', data[1:5])[0]  # Unpack 4-byte integer (little-endian)
            return opcode, value
        elif opcode == 3:  
            # SetComputeUnitPrice takes in micro lamports
            # https://github.com/solana-labs/solana/blob/ced8f6a512c61e0dd5308095ae8457add4a39e94/program-runtime/src/prioritization_fee.rs#L1-L2
            value = struct.unpack('<Q', data[1:9])[0]  # Unpack 8-byte integer (little-endian)
            return opcode, value
        else:
            # more instructions to parse
            # https://github.com/solana-labs/solana/blob/master/sdk/src/compute_budget.rs
            return 0, 0
        
    def get_prioritization_fee(self, tx):
        instructions = tx.value.transaction.transaction.message.instructions
        # https://solana.com/docs/core/fees#prioritization-fees
        # calculated by multiplying its compute unit limit by the compute unit price
        compute_budget_program_id = "ComputeBudget111111111111111111111111111111"

        # If no SetComputeUnitLimit instruction is provided, the default compute unit limit 
        # will be used.
        compute_unit_limit = 200_000

        # If no SetComputeUnitPrice instruction is provided, the transaction will default 
        # to no additional elevated fee and the lowest priority (i.e. no prioritization fee).
        compute_unit_price = 0

        for instruction in instructions:
            if str(instruction.program_id) == compute_budget_program_id:
                decoded_data = base58.b58decode(instruction.data)
                opcode, value = self.decode_compute_budget_instruction(decoded_data)
                if opcode == 2:
                    compute_unit_limit = value
                elif opcode == 3:
                    # convert to lamports
                    compute_unit_price = value / 1_000_000
        
        return round(compute_unit_limit * compute_unit_price)

    def parse_instruction(self, signature: Signature, tx: GetTransactionResp, instruction: UiPartiallyDecodedInstruction, instruction_type: str, doc: dict) -> dict | None:
        '''
        Parse the common for most protocols fields of the transaction and the instruction.
        All fields of the resulting document can be overwritten in the parse_protocol_specific_fields.
        '''
        
        doc['instruction_type'] = instruction_type

        # the inner tx object contains parsed instruction data
        try:
            data = self.schema.parse(base58.b58decode(instruction.data.encode()))
            doc['tx'] = {}
            for key, value in data.items():
                doc['tx'][key] = value
        except Exception as e:
            print(f"Failed to parse data for [{signature}] : [{e}]")
            # record for possible future fix txs that have unknown instructions
            doc[UNPARSED_INSTRUCTION_FIELD_NAME] = instruction.data
            doc['tx'] = {}
            doc['tx']['orderId'] = doc['scraper_tx_hash']

        doc = self.parse_protocol_specific_fields(tx, instruction, doc)

        return doc
    

    def parse_transaction(self, chain_id: str, signature: Signature, tx: GetTransactionResp) -> dict | None:

        assert tx.value is not None
        tx_data = tx.value.transaction.transaction
        tx_meta = tx.value.transaction.meta
        assert tx_meta is not None
        assert tx_data is not None
        message = tx_data.message # type: ignore[attr-defined]

        doc = {}
        
        doc['scraper_originChain'] = chain_id
        doc['scraper_blockNumber'] = tx.value.slot
        doc['scraper_blockTimestamp'] = tx.value.block_time
        scraper_from = message.account_keys[0]
        if isinstance(scraper_from, ParsedAccount):
            doc['scraper_from'] = str(scraper_from.pubkey)
        else:
            doc['scraper_from'] = str(scraper_from)
        doc['scraper_contractAddress'] = self.program_address
        doc['scraper_tx_status'] = "reverted" if tx_meta.err != None else "ok"
        doc['scraper_tx_hash'] = str(signature)

        doc['scraper_chain_fee'] = tx_meta.fee
        doc['scraper_chain_prioritization_fee'] = self.get_prioritization_fee(tx)

        for instruction in message.instructions:
            if self.is_relevant_instruction(instruction):
                tx_doc = self.parse_instruction(signature, tx, instruction, "outer_instruction", doc) # type: ignore[arg-type]
                if tx_doc != None:
                    return tx_doc
        
        if tx_meta.inner_instructions is not None:
            for inner_instruction in tx_meta.inner_instructions:
                for instruction in inner_instruction.instructions:
                    if self.is_relevant_instruction(instruction):
                        tx_doc = self.parse_instruction(signature, tx, instruction, "inner_instruction", doc) # type: ignore[arg-type]
                        if tx_doc != None:
                            return tx_doc

        return None
