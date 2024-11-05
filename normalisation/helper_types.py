from typing import TypedDict


class ProtocolFee(TypedDict):
    chain_id: str
    token_address: str
    amount: int | float


class PartnerFee(TypedDict):
    chain_id: str
    token_address: str
    amount: int | float
    partner_fee_address: str
