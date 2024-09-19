from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class AllowOperatorArgs(typing.TypedDict):
    is_allowed: bool


layout = borsh.CStruct("is_allowed" / borsh.Bool)


class AllowOperatorAccounts(typing.TypedDict):
    bridge: Pubkey
    operator_storage: Pubkey
    operator: Pubkey
    admin: Pubkey
    payer: Pubkey


def allow_operator(
    args: AllowOperatorArgs,
    accounts: AllowOperatorAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["bridge"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["operator_storage"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["operator"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x1e\x1eI\xd7\xf7E\xcf\x89"
    encoded_args = layout.build(
        {
            "is_allowed": args["is_allowed"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
