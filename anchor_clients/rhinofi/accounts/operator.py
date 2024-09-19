import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class OperatorJSON(typing.TypedDict):
    operator: str
    is_allowed: bool


@dataclass
class Operator:
    discriminator: typing.ClassVar = b"\xdb\x1f\xbc\x91E\x8b\xccu"
    layout: typing.ClassVar = borsh.CStruct(
        "operator" / BorshPubkey, "is_allowed" / borsh.Bool
    )
    operator: Pubkey
    is_allowed: bool

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Operator"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["Operator"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Operator"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Operator":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Operator.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            operator=dec.operator,
            is_allowed=dec.is_allowed,
        )

    def to_json(self) -> OperatorJSON:
        return {
            "operator": str(self.operator),
            "is_allowed": self.is_allowed,
        }

    @classmethod
    def from_json(cls, obj: OperatorJSON) -> "Operator":
        return cls(
            operator=Pubkey.from_string(obj["operator"]),
            is_allowed=obj["is_allowed"],
        )
