from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class WithdrawArgs(typing.TypedDict):
    amount: int


layout = borsh.CStruct("amount" / borsh.U64)


class WithdrawAccounts(typing.TypedDict):
    bridge: Pubkey
    pool: Pubkey
    pool_authority: Pubkey
    operator_storage: Pubkey
    recipient: Pubkey
    operator: Pubkey
    mint: Pubkey
    pool_account: Pubkey
    recipient_account: Pubkey
    payer: Pubkey


def withdraw(
    args: WithdrawArgs,
    accounts: WithdrawAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["bridge"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pool"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["pool_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["operator_storage"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["recipient"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["operator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pool_account"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["recipient_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b'\xb7\x12F\x9c\x94m\xa1"'
    encoded_args = layout.build(
        {
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
