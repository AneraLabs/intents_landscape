from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class DepositArgs(typing.TypedDict):
    amount: int
    eth_address_upper: int
    eth_address_lower: int


layout = borsh.CStruct(
    "amount" / borsh.U64,
    "eth_address_upper" / borsh.U32,
    "eth_address_lower" / borsh.U128,
)


class DepositAccounts(typing.TypedDict):
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


def deposit(
    args: DepositArgs,
    accounts: DepositAccounts,
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
    identifier = b"\xf2#\xc6\x89R\xe1\xf2\xb6"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
            "eth_address_upper": args["eth_address_upper"],
            "eth_address_lower": args["eth_address_lower"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
