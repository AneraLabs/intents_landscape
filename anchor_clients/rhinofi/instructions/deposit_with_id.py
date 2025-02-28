from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class DepositWithIdArgs(typing.TypedDict):
    amount: int
    commitment_id: int


layout = borsh.CStruct("amount" / borsh.U64, "commitment_id" / borsh.U128)


class DepositWithIdAccounts(typing.TypedDict):
    bridge: Pubkey
    pool: Pubkey
    pool_authority: Pubkey
    depositor: Pubkey
    mint: Pubkey
    pool_account: Pubkey
    depositor_account: Pubkey
    payer: Pubkey
    event_authority: Pubkey
    program: Pubkey


def deposit_with_id(
    args: DepositWithIdArgs,
    accounts: DepositWithIdAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["bridge"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pool"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["pool_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["depositor"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pool_account"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["depositor_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdfH\x96\xc2\xbe\xf5\xf5\x8f"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
            "commitment_id": args["commitment_id"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
