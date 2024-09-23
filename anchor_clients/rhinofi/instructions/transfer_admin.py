from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class TransferAdminAccounts(typing.TypedDict):
    bridge: Pubkey
    new_admin: Pubkey
    admin: Pubkey


def transfer_admin(
    accounts: TransferAdminAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["bridge"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["new_admin"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"*\xf2Bj\xe4\no\x9c"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
