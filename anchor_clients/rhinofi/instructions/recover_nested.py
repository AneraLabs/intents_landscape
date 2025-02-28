from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class RecoverNestedAccounts(typing.TypedDict):
    bridge: Pubkey
    pool: Pubkey
    operator_storage: Pubkey
    pool_authority: Pubkey
    mint: Pubkey
    pool_account: Pubkey
    nested_pool_account: Pubkey
    operator: Pubkey
    payer: Pubkey


def recover_nested(
    accounts: RecoverNestedAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["bridge"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pool"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["operator_storage"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["pool_authority"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pool_account"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["nested_pool_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["operator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x08\xbe\xc9:\xc8y\xd2\x8f"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
