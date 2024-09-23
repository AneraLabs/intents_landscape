import typing
from anchorpy.error import ProgramError


class DepositNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "DEPOSIT_NOT_ALLOWED")

    code = 6000
    name = "DepositNotAllowed"
    msg = "DEPOSIT_NOT_ALLOWED"


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "UNAUTHORIZED")

    code = 6001
    name = "Unauthorized"
    msg = "UNAUTHORIZED"


class NotEnoughLiquidity(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "NOT_ENOUGH_LIQUIDITY")

    code = 6002
    name = "NotEnoughLiquidity"
    msg = "NOT_ENOUGH_LIQUIDITY"


class NotEnoughBalance(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "NOT_ENOUGH_BALANCE")

    code = 6003
    name = "NotEnoughBalance"
    msg = "NOT_ENOUGH_BALANCE"


class InvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "INVALID_AMOUNT")

    code = 6004
    name = "InvalidAmount"
    msg = "INVALID_AMOUNT"


CustomError = typing.Union[
    DepositNotAllowed, Unauthorized, NotEnoughLiquidity, NotEnoughBalance, InvalidAmount
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: DepositNotAllowed(),
    6001: Unauthorized(),
    6002: NotEnoughLiquidity(),
    6003: NotEnoughBalance(),
    6004: InvalidAmount(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
