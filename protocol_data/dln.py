import base64
import json
import os
import traceback
from abc import abstractmethod

from anchorpy.coder.event import EventCoder
from anchorpy.coder.instruction import InstructionCoder
from anchorpy.program.common import NamedInstruction
from anchorpy_core.idl import Idl
from base58 import b58decode
from solders.pubkey import Pubkey
from solders.rpc.responses import GetTransactionResp
from solders.transaction_status import UiPartiallyDecodedInstruction

from protocol_data.solana_parser import (
    UNPARSED_INSTRUCTION_FIELD_NAME,
    BaseSolanaParser,
    Parseable,
)

PROTOCOL_NAME = "dln"
DEPOSIT_SOLANA_PROGRAM_ID = "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4"
FILL_SOLANA_PROGRAM_ID = "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo"

# https://github.com/debridge-finance/dln-contracts/blob/d54e94f2b5102bff89a4df506404bb77f3edc148/hardhat.config.ts
# https://docs.dln.trade/the-core-protocol/trusted-smart-contracts
CHAINS_TO_CONTRACTS = {
    "7565164": {
        "deposit": DEPOSIT_SOLANA_PROGRAM_ID,
        "fill": FILL_SOLANA_PROGRAM_ID,
    },
    "42161": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "43114": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "8453": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "56": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "1": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "59144": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "10": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "137": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "250": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "100": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "146": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "245022934": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
    "1088": {
        "deposit": {0: "0xeF4fB24aD0916217251F553c0596F8Edc630EB66"},
        "fill": {0: "0xE7351Fd770A37282b91D153Ee690B63579D6dd7f"},
    },
}


def get_contract_address(chain_id, type):
    return CHAINS_TO_CONTRACTS[chain_id][type]


# TODO: Move to abi json file
def get_contract_abi(chain_id, type):
    contract_dlnsource_abi = json.loads(
        """[{"inputs":[],"name":"AdminBadRole","type":"error"},{"inputs":[],"name":"CallProxyBadRole","type":"error"},{"inputs":[{"internalType":"bytes32","name":"orderId","type":"bytes32"},{"internalType":"uint48","name":"takeChainId","type":"uint48"},{"internalType":"uint256","name":"submissionsChainIdFrom","type":"uint256"}],"name":"CriticalMismatchTakeChainId","type":"error"},{"inputs":[],"name":"EthTransferFailed","type":"error"},{"inputs":[],"name":"GovMonitoringBadRole","type":"error"},{"inputs":[],"name":"IncorrectOrderStatus","type":"error"},{"inputs":[],"name":"MismatchNativeGiveAmount","type":"error"},{"inputs":[],"name":"MismatchedOrderId","type":"error"},{"inputs":[],"name":"MismatchedTransferAmount","type":"error"},{"inputs":[{"internalType":"bytes","name":"nativeSender","type":"bytes"},{"internalType":"uint256","name":"chainIdFrom","type":"uint256"}],"name":"NativeSenderBadRole","type":"error"},{"inputs":[],"name":"NotSupportedDstChain","type":"error"},{"inputs":[],"name":"SignatureInvalidV","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"inputs":[],"name":"UnknownEngine","type":"error"},{"inputs":[],"name":"WrongAddressLength","type":"error"},{"inputs":[],"name":"WrongAffiliateFeeLength","type":"error"},{"inputs":[],"name":"WrongArgument","type":"error"},{"inputs":[],"name":"WrongChain","type":"error"},{"inputs":[{"internalType":"uint256","name":"received","type":"uint256"},{"internalType":"uint256","name":"actual","type":"uint256"}],"name":"WrongFixedFee","type":"error"},{"inputs":[],"name":"ZeroAddress","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"_orderId","type":"bytes32"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"},{"indexed":false,"internalType":"uint256","name":"affiliateFee","type":"uint256"},{"indexed":false,"internalType":"address","name":"giveTokenAddress","type":"address"}],"name":"AffiliateFeePaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"},{"indexed":false,"internalType":"uint256","name":"paidAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"giveTokenAddress","type":"address"}],"name":"ClaimedOrderCancel","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"},{"indexed":false,"internalType":"uint256","name":"giveAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"giveTokenAddress","type":"address"}],"name":"ClaimedUnlock","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint64","name":"makerOrderNonce","type":"uint64"},{"internalType":"bytes","name":"makerSrc","type":"bytes"},{"internalType":"uint256","name":"giveChainId","type":"uint256"},{"internalType":"bytes","name":"giveTokenAddress","type":"bytes"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"bytes","name":"givePatchAuthoritySrc","type":"bytes"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"}],"indexed":false,"internalType":"struct DlnOrderLib.Order","name":"order","type":"tuple"},{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"bytes","name":"affiliateFee","type":"bytes"},{"indexed":false,"internalType":"uint256","name":"nativeFixFee","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"percentFee","type":"uint256"},{"indexed":false,"internalType":"uint32","name":"referralCode","type":"uint32"},{"indexed":false,"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"CreatedOrder","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"},{"indexed":false,"internalType":"uint256","name":"takeChainId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"submissionChainIdFrom","type":"uint256"}],"name":"CriticalMismatchChainId","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint88","name":"oldGlobalFixedNativeFee","type":"uint88"},{"indexed":false,"internalType":"uint88","name":"newGlobalFixedNativeFee","type":"uint88"}],"name":"GlobalFixedNativeFeeUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"oldGlobalTransferFeeBps","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"newGlobalTransferFeeBps","type":"uint16"}],"name":"GlobalTransferFeeBpsUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"orderGiveFinalAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"finalPercentFee","type":"uint256"}],"name":"IncreasedGiveAmount","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"chainIdTo","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"dlnDestinationAddress","type":"bytes"},{"indexed":false,"internalType":"enum DlnOrderLib.ChainEngine","name":"chainEngine","type":"uint8"}],"name":"SetDlnDestinationAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"enum DlnSource.OrderGiveStatus","name":"status","type":"uint8"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"}],"name":"UnexpectedOrderStatusForCancel","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderId","type":"bytes32"},{"indexed":false,"internalType":"enum DlnSource.OrderGiveStatus","name":"status","type":"uint8"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"}],"name":"UnexpectedOrderStatusForClaim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"beneficiary","type":"address"}],"name":"WithdrawnFee","type":"event"},{"inputs":[],"name":"BPS_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EVM_ADDRESS_LENGTH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GOVMONITORING_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_ADDRESS_LENGTH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SOLANA_ADDRESS_LENGTH","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"chainEngines","outputs":[{"internalType":"enum DlnOrderLib.ChainEngine","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_orderIds","type":"bytes32[]"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"claimBatchCancel","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_orderIds","type":"bytes32[]"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"claimBatchUnlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_orderId","type":"bytes32"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"claimCancel","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_orderId","type":"bytes32"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"claimUnlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"collectedFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"giveTokenAddress","type":"address"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"address","name":"givePatchAuthoritySrc","type":"address"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"}],"internalType":"struct DlnOrderLib.OrderCreation","name":"_orderCreation","type":"tuple"},{"internalType":"bytes","name":"_affiliateFee","type":"bytes"},{"internalType":"uint32","name":"_referralCode","type":"uint32"},{"internalType":"bytes","name":"_permitEnvelope","type":"bytes"}],"name":"createOrder","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"giveTokenAddress","type":"address"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"address","name":"givePatchAuthoritySrc","type":"address"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"}],"internalType":"struct DlnOrderLib.OrderCreation","name":"_orderCreation","type":"tuple"},{"internalType":"uint64","name":"_salt","type":"uint64"},{"internalType":"bytes","name":"_affiliateFee","type":"bytes"},{"internalType":"uint32","name":"_referralCode","type":"uint32"},{"internalType":"bytes","name":"_permitEnvelope","type":"bytes"},{"internalType":"bytes","name":"_metadata","type":"bytes"}],"name":"createSaltedOrder","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"deBridgeGate","outputs":[{"internalType":"contract IDeBridgeGate","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"dlnDestinationAddresses","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getChainId","outputs":[{"internalType":"uint256","name":"cid","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"makerOrderNonce","type":"uint64"},{"internalType":"bytes","name":"makerSrc","type":"bytes"},{"internalType":"uint256","name":"giveChainId","type":"uint256"},{"internalType":"bytes","name":"giveTokenAddress","type":"bytes"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"bytes","name":"givePatchAuthoritySrc","type":"bytes"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"}],"internalType":"struct DlnOrderLib.Order","name":"_order","type":"tuple"}],"name":"getOrderId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"giveOrders","outputs":[{"internalType":"enum DlnSource.OrderGiveStatus","name":"status","type":"uint8"},{"internalType":"uint160","name":"giveTokenAddress","type":"uint160"},{"internalType":"uint88","name":"nativeFixFee","type":"uint88"},{"internalType":"uint48","name":"takeChainId","type":"uint48"},{"internalType":"uint208","name":"percentFee","type":"uint208"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"address","name":"affiliateBeneficiary","type":"address"},{"internalType":"uint256","name":"affiliateAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"givePatches","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"globalFixedNativeFee","outputs":[{"internalType":"uint88","name":"","type":"uint88"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"globalTransferFeeBps","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IDeBridgeGate","name":"_deBridgeGate","type":"address"},{"internalType":"uint88","name":"_globalFixedNativeFee","type":"uint88"},{"internalType":"uint16","name":"_globalTransferFeeBps","type":"uint16"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"masterNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"makerOrderNonce","type":"uint64"},{"internalType":"bytes","name":"makerSrc","type":"bytes"},{"internalType":"uint256","name":"giveChainId","type":"uint256"},{"internalType":"bytes","name":"giveTokenAddress","type":"bytes"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"bytes","name":"givePatchAuthoritySrc","type":"bytes"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"}],"internalType":"struct DlnOrderLib.Order","name":"_order","type":"tuple"},{"internalType":"uint256","name":"_addGiveAmount","type":"uint256"},{"internalType":"bytes","name":"_permitEnvelope","type":"bytes"}],"name":"patchOrderGive","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_chainIdTo","type":"uint256"},{"internalType":"bytes","name":"_dlnDestinationAddress","type":"bytes"},{"internalType":"enum DlnOrderLib.ChainEngine","name":"_chainEngine","type":"uint8"}],"name":"setDlnDestinationAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"unclaimedAffiliateETHFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"unexpectedOrderStatusForCancel","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"unexpectedOrderStatusForClaim","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint88","name":"_globalFixedNativeFee","type":"uint88"},{"internalType":"uint16","name":"_globalTransferFeeBps","type":"uint16"}],"name":"updateGlobalFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"giveTokenAddress","type":"address"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"address","name":"givePatchAuthoritySrc","type":"address"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"}],"internalType":"struct DlnOrderLib.OrderCreation","name":"_orderCreation","type":"tuple"},{"internalType":"address","name":"_signer","type":"address"},{"internalType":"uint64","name":"_salt","type":"uint64"}],"name":"validateCreationOrder","outputs":[{"components":[{"internalType":"uint64","name":"makerOrderNonce","type":"uint64"},{"internalType":"bytes","name":"makerSrc","type":"bytes"},{"internalType":"uint256","name":"giveChainId","type":"uint256"},{"internalType":"bytes","name":"giveTokenAddress","type":"bytes"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"bytes","name":"givePatchAuthoritySrc","type":"bytes"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"}],"internalType":"struct DlnOrderLib.Order","name":"order","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"giveTokenAddress","type":"address"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"address","name":"givePatchAuthoritySrc","type":"address"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"}],"internalType":"struct DlnOrderLib.OrderCreation","name":"_orderCreation","type":"tuple"},{"internalType":"address","name":"_signer","type":"address"}],"name":"validateCreationOrder","outputs":[{"components":[{"internalType":"uint64","name":"makerOrderNonce","type":"uint64"},{"internalType":"bytes","name":"makerSrc","type":"bytes"},{"internalType":"uint256","name":"giveChainId","type":"uint256"},{"internalType":"bytes","name":"giveTokenAddress","type":"bytes"},{"internalType":"uint256","name":"giveAmount","type":"uint256"},{"internalType":"uint256","name":"takeChainId","type":"uint256"},{"internalType":"bytes","name":"takeTokenAddress","type":"bytes"},{"internalType":"uint256","name":"takeAmount","type":"uint256"},{"internalType":"bytes","name":"receiverDst","type":"bytes"},{"internalType":"bytes","name":"givePatchAuthoritySrc","type":"bytes"},{"internalType":"bytes","name":"orderAuthorityAddressDst","type":"bytes"},{"internalType":"bytes","name":"allowedTakerDst","type":"bytes"},{"internalType":"bytes","name":"allowedCancelBeneficiarySrc","type":"bytes"},{"internalType":"bytes","name":"externalCall","type":"bytes"}],"internalType":"struct DlnOrderLib.Order","name":"order","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address[]","name":"_tokens","type":"address[]"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"withdrawFee","outputs":[],"stateMutability":"nonpayable","type":"function"}]"""
    )
    contract_dlndestination_abi = json.loads("""[
    {
      "inputs": [],
      "name": "AdminBadRole",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "bytes",
          "name": "expectedBeneficiary",
          "type": "bytes"
        }
      ],
      "name": "AllowOnlyForBeneficiary",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "CallProxyBadRole",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "EthTransferFailed",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ExternalCallIsBlocked",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "GovMonitoringBadRole",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "IncorrectOrderStatus",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "MismatchGiveChainId",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "MismatchNativeTakerAmount",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "MismatchTakerAmount",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "MismatchedOrderId",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "MismatchedTransferAmount",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "bytes",
          "name": "nativeSender",
          "type": "bytes"
        },
        {
          "internalType": "uint256",
          "name": "chainIdFrom",
          "type": "uint256"
        }
      ],
      "name": "NativeSenderBadRole",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "NotSupportedDstChain",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ProposedFeeTooHigh",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "SignatureInvalidV",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "TheSameFromTo",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "TransferAmountNotCoverFees",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "Unauthorized",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "UnexpectedBatchSize",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "UnknownEngine",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "WrongAddressLength",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "WrongArgument",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "WrongAutoArgument",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "WrongChain",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "WrongToken",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ZeroAddress",
      "type": "error"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "orderId",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "orderTakeFinalAmount",
          "type": "uint256"
        }
      ],
      "name": "DecreasedTakeAmount",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "indexed": false,
          "internalType": "struct DlnBase.Order",
          "name": "order",
          "type": "tuple"
        },
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "orderId",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "unlockAuthority",
          "type": "address"
        }
      ],
      "name": "FulfilledOrder",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "uint8",
          "name": "version",
          "type": "uint8"
        }
      ],
      "name": "Initialized",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Paused",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "previousAdminRole",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "newAdminRole",
          "type": "bytes32"
        }
      ],
      "name": "RoleAdminChanged",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        }
      ],
      "name": "RoleGranted",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        }
      ],
      "name": "RoleRevoked",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "indexed": false,
          "internalType": "struct DlnBase.Order",
          "name": "order",
          "type": "tuple"
        },
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "orderId",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "bytes",
          "name": "cancelBeneficiary",
          "type": "bytes"
        },
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "submissionId",
          "type": "bytes32"
        }
      ],
      "name": "SentOrderCancel",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "orderId",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "bytes",
          "name": "beneficiary",
          "type": "bytes"
        },
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "submissionId",
          "type": "bytes32"
        }
      ],
      "name": "SentOrderUnlock",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "chainIdFrom",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "bytes",
          "name": "dlnSourceAddress",
          "type": "bytes"
        },
        {
          "indexed": false,
          "internalType": "enum DlnBase.ChainEngine",
          "name": "chainEngine",
          "type": "uint8"
        }
      ],
      "name": "SetDlnSourceAddress",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Unpaused",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "BPS_DENOMINATOR",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "DEFAULT_ADMIN_ROLE",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "EVM_ADDRESS_LENGTH",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "GOVMONITORING_ROLE",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "MAX_ADDRESS_LENGTH",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "MAX_ORDER_COUNT_PER_BATCH_EVM_UNLOCK",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "NATIVE_AMOUNT_DIVIDER_FOR_TRANSFER_TO_SOLANA",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "SOLANA_ADDRESS_LENGTH",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "SOLANA_CHAIN_ID",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "chainEngines",
      "outputs": [
        {
          "internalType": "enum DlnBase.ChainEngine",
          "name": "",
          "type": "uint8"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "deBridgeGate",
      "outputs": [
        {
          "internalType": "contract IDeBridgeGate",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "dlnSourceAddresses",
      "outputs": [
        {
          "internalType": "bytes",
          "name": "",
          "type": "bytes"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "internalType": "struct DlnBase.Order",
          "name": "_order",
          "type": "tuple"
        },
        {
          "internalType": "uint256",
          "name": "_fulFillAmount",
          "type": "uint256"
        },
        {
          "internalType": "bytes32",
          "name": "_orderId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes",
          "name": "_permitEnvelope",
          "type": "bytes"
        },
        {
          "internalType": "address",
          "name": "_unlockAuthority",
          "type": "address"
        }
      ],
      "name": "fulfillOrder",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getChainId",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "cid",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "internalType": "struct DlnBase.Order",
          "name": "_order",
          "type": "tuple"
        }
      ],
      "name": "getOrderId",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        }
      ],
      "name": "getRoleAdmin",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "grantRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "hasRole",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "contract IDeBridgeGate",
          "name": "_deBridgeGate",
          "type": "address"
        }
      ],
      "name": "initialize",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "internalType": "struct DlnBase.Order",
          "name": "_order",
          "type": "tuple"
        },
        {
          "internalType": "uint256",
          "name": "_newSubtrahend",
          "type": "uint256"
        }
      ],
      "name": "patchOrderTake",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "pause",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "paused",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "renounceRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "revokeRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_orderIds",
          "type": "bytes32[]"
        },
        {
          "internalType": "address",
          "name": "_beneficiary",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_executionFee",
          "type": "uint256"
        }
      ],
      "name": "sendBatchEvmUnlock",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "internalType": "struct DlnBase.Order",
          "name": "_order",
          "type": "tuple"
        },
        {
          "internalType": "address",
          "name": "_cancelBeneficiary",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_executionFee",
          "type": "uint256"
        }
      ],
      "name": "sendEvmOrderCancel",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_orderId",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "_beneficiary",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_executionFee",
          "type": "uint256"
        }
      ],
      "name": "sendEvmUnlock",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "internalType": "struct DlnBase.Order",
          "name": "_order",
          "type": "tuple"
        },
        {
          "internalType": "bytes32",
          "name": "_cancelBeneficiary",
          "type": "bytes32"
        },
        {
          "internalType": "uint256",
          "name": "_executionFee",
          "type": "uint256"
        },
        {
          "internalType": "uint64",
          "name": "_reward1",
          "type": "uint64"
        },
        {
          "internalType": "uint64",
          "name": "_reward2",
          "type": "uint64"
        }
      ],
      "name": "sendSolanaOrderCancel",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "components": [
            {
              "internalType": "uint64",
              "name": "makerOrderNonce",
              "type": "uint64"
            },
            {
              "internalType": "bytes",
              "name": "makerSrc",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "giveTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "giveAmount",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "takeChainId",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "takeTokenAddress",
              "type": "bytes"
            },
            {
              "internalType": "uint256",
              "name": "takeAmount",
              "type": "uint256"
            },
            {
              "internalType": "bytes",
              "name": "receiverDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "givePatchAuthoritySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "orderAuthorityAddressDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedTakerDst",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "allowedCancelBeneficiarySrc",
              "type": "bytes"
            },
            {
              "internalType": "bytes",
              "name": "externalCall",
              "type": "bytes"
            }
          ],
          "internalType": "struct DlnBase.Order",
          "name": "_order",
          "type": "tuple"
        },
        {
          "internalType": "bytes32",
          "name": "_beneficiary",
          "type": "bytes32"
        },
        {
          "internalType": "uint256",
          "name": "_executionFee",
          "type": "uint256"
        },
        {
          "internalType": "uint64",
          "name": "_solanaExternalCallReward1",
          "type": "uint64"
        },
        {
          "internalType": "uint64",
          "name": "_solanaExternalCallReward2",
          "type": "uint64"
        }
      ],
      "name": "sendSolanaUnlock",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_chainIdFrom",
          "type": "uint256"
        },
        {
          "internalType": "bytes",
          "name": "_dlnSourceAddress",
          "type": "bytes"
        },
        {
          "internalType": "enum DlnBase.ChainEngine",
          "name": "_chainEngine",
          "type": "uint8"
        }
      ],
      "name": "setDlnSourceAddress",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes4",
          "name": "interfaceId",
          "type": "bytes4"
        }
      ],
      "name": "supportsInterface",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "name": "takeOrders",
      "outputs": [
        {
          "internalType": "enum DlnDestination.OrderTakeStatus",
          "name": "status",
          "type": "uint8"
        },
        {
          "internalType": "address",
          "name": "takerAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "giveChainId",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "name": "takePatches",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "unpause",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "version",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    }
  ]""")

    if type == "deposit":
        return {0: contract_dlnsource_abi}
    elif type == "fill":
        return {0: contract_dlndestination_abi}

    return None


def get_supported_chains():
    return list(CHAINS_TO_CONTRACTS.keys())


def get_deposit_function_filter():
    return None


def get_deposit_event_filter():
    return {0: ["CreatedOrder"]}


def get_fill_function_filter():
    return {0: ["fulfillOrder"]}


def get_fill_event_filter():
    return {0: ["FulfilledOrder"]}


# --------------------- Solana ----------------------------

# make the script launchable from any directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DEPOSIT_IDL_PATH = os.path.join(PARENT_DIR, "idls", "dln_deposit.json")
FILL_IDL_PATH = os.path.join(PARENT_DIR, "idls", "dln_fill.json")


with open(DEPOSIT_IDL_PATH, encoding="utf-8") as f:
    DEPOSIT_IDL = json.load(f)
DEPOSIT_CODER = InstructionCoder(Idl.from_json(json.dumps(DEPOSIT_IDL)))

with open(FILL_IDL_PATH, encoding="utf-8") as f:
    FILL_IDL = json.load(f)
FILL_CODER = InstructionCoder(Idl.from_json(json.dumps(FILL_IDL)))


def get_order_id_from_logs(logs) -> str | None:
    try:
        json_string = json.dumps(DEPOSIT_IDL)
        coder = EventCoder(Idl.from_json(json_string))
    except Exception as e:
        print("Coder Error", e)

    for log in logs:
        try:
            parsed_event = coder.parse(
                base64.b64decode(log.replace("Program data: ", ""))
            )

            if parsed_event.name == "CreatedOrderId":
                return hex(int.from_bytes(parsed_event.data.order_id))
        except Exception:
            pass


def snake_to_camel(snake_str):
    prefix = ""
    if snake_str.startswith("_"):
        prefix = "_"
        snake_str = snake_str[1:]

    components = snake_str.split("_")
    return prefix + components[0] + "".join(x.title() for x in components[1:])


# TODO: fix ruff warnings
# ruff: noqa: PLR0912
def process_instruction_data(doc: dict, data):
    try:
        # record as many fields as possible
        if isinstance(data, dict):
            items = list(data.items())
        else:
            items = []
            for attr in dir(data):
                if not attr.startswith("__"):
                    attr_value = getattr(data, attr)
                    if not callable(attr_value):
                        items.append((attr, attr_value))

        for key_snake, value in items:
            # to stay consistent with previously ingested data
            key = snake_to_camel(key_snake)
            if key in {"_io", "externalCall"}:
                continue
            if key == "unvalidatedOrder":
                key = "_order"

            if value is None:
                doc[key] = None
            elif key in {"orderId"}:
                doc[key] = hex(int.from_bytes(value))
            elif key in {"orderArgs", "take", "give", "affiliateFee", "_order"}:
                doc[key] = {}
                process_instruction_data(doc[key], value)
            elif key in {"chainId", "amount"}:
                if isinstance(value, int) or isinstance(value, str):
                    doc[key] = str(value)
                else:
                    doc[key] = str(int.from_bytes(value))
            elif isinstance(value, bytes):
                # dln often passes addresses as bytes
                try:
                    solana_key_value = Pubkey(value)
                    doc[key] = str(solana_key_value)
                except ValueError:
                    # if couldn't convert to pubkey, most likely the field is an EVM address
                    # store it as hex by default
                    doc[key] = hex(int.from_bytes(value))
            elif (
                isinstance(value, int)
                or isinstance(value, float)
                or isinstance(value, str)
            ):
                doc[key] = value
            elif isinstance(value, Pubkey):
                doc[key] = str(value)

    except Exception as e:
        # print stack trace
        print(
            f"Warning: failed to process key: [{key}] with error: [{e}], stack trace:"
        )
        traceback.print_exc()
        print(f"Key: {key}, e: {e}")


class DlnParser(BaseSolanaParser):
    # shared fields for deposit and fill

    @property
    def protocol_name(self) -> str:
        return "dln"

    @property
    @abstractmethod
    def identifier(self) -> str:
        raise NotImplementedError

    def is_relevant_instruction(self, instruction) -> bool:
        has_parsable_data = isinstance(instruction, UiPartiallyDecodedInstruction)
        if not has_parsable_data:
            return False
        decoded_data_hex = b58decode(instruction.data.encode()).hex()
        return str(
            instruction.program_id
        ) == self.program_address and decoded_data_hex.startswith(self.identifier)

    def parse_protocol_specific_fields(  # noqa: PLR6301
        self,
        tx: GetTransactionResp,
        instruction: UiPartiallyDecodedInstruction,
        parsed_instruction: NamedInstruction,
        doc: dict,
    ):
        if parsed_instruction is not None:
            data = parsed_instruction.data
            doc["tx"] = {}
            doc["tx"]["identifier"] = snake_to_camel(parsed_instruction.name)
            process_instruction_data(doc["tx"], data)

        return doc


class DlnDepositParser(DlnParser):
    @property
    def identifier(self) -> str:
        return "828362be28ce4432"

    @property
    def program_address(self) -> str:
        return DEPOSIT_SOLANA_PROGRAM_ID

    @property
    def schema(self) -> Parseable:
        return DEPOSIT_CODER

    def parse_protocol_specific_fields(
        self,
        tx: GetTransactionResp,
        instruction: UiPartiallyDecodedInstruction,
        parsed_instruction_data: NamedInstruction,
        doc: dict,
    ):
        doc = super().parse_protocol_specific_fields(
            tx, instruction, parsed_instruction_data, doc
        )

        if UNPARSED_INSTRUCTION_FIELD_NAME not in doc:
            doc["scraper_function"] = "deposit"
            doc["tx"]["orderArgs"]["giveTokenAddress"] = str(instruction.accounts[2])
            assert tx.value is not None
            tx_meta = tx.value.transaction.meta
            assert tx_meta is not None
            doc["tx"]["orderId"] = get_order_id_from_logs(tx_meta.log_messages)

        return doc


class DlnFillParser(DlnParser):
    @property
    def identifier(self) -> str:
        return "3dd627f841d49924"

    @property
    def program_address(self) -> str:
        return FILL_SOLANA_PROGRAM_ID

    @property
    def schema(self) -> Parseable:
        return FILL_CODER

    def parse_protocol_specific_fields(
        self,
        tx: GetTransactionResp,
        instruction: UiPartiallyDecodedInstruction,
        parsed_instruction_data: NamedInstruction,
        doc: dict,
    ):
        doc = super().parse_protocol_specific_fields(
            tx, instruction, parsed_instruction_data, doc
        )

        if UNPARSED_INSTRUCTION_FIELD_NAME not in doc:
            doc["scraper_function"] = "fulfillOrder"

        return doc


def get_solana_parsers() -> list[BaseSolanaParser]:
    return [DlnDepositParser(), DlnFillParser()]


# ruff: noqa: E501
if __name__ == "__main__":
    # a simple test for dln solana parser
    from deepdiff import DeepDiff
    from solana.rpc.api import Client
    from solders.pubkey import Pubkey
    from solders.signature import Signature

    parsers = get_solana_parsers()
    chain_id = "7565164"

    rpc_url = "https://api.mainnet-beta.solana.com"

    client = Client(rpc_url)

    def print_diff(expected, result):
        diff = DeepDiff(expected, result, verbose_level=2)

        if diff:
            print(json.dumps(diff, indent=4, default=str))

            print("Reult doc:")
            print(json.dumps(result, indent=4, default=str))
        else:
            print("No differences found")

    def get_tx_and_parse(signature, parser):
        tx = client.get_transaction(
            signature, max_supported_transaction_version=1, encoding="jsonParsed"
        )
        result = parser.parse_transaction(chain_id, signature, tx)
        return result

    # signatures with Claim Unlock (no relevant instructions, should result in null)
    # signatures_to_check = [
    #     Signature.from_string('3miQh98v3eMoS9thVBd4cbUuuyAocMdtbcr2ZWZ43WmiqGSpSdks9EwswEHiyidusosxd62CguVyMBbvaWqdiXBh'),
    #     Signature.from_string('2xDYud2StWxWWk6D2yLANrRgTMaQC6Df5BEGZ8tjVp47uq5ysCGuojhfm4V2DZVRMP5feRgrCGD5APdzYuVXyjLm'),
    #     Signature.from_string('wtQtS6chBDmz6cJ8wRjvC5VQrbZ7sxtGj2a5avp27Dj9bEsL6zWkstRTNWoKFT3yZyfJTqoDfGsmdNuZ8orHrze')
    # ]
    # for signature in signatures_to_check:
    #     tx = client.get_transaction(signature, max_supported_transaction_version=1, encoding="jsonParsed")
    #     result = parsers[0].parse_transaction(chain_id, signature, tx)
    #     print(json.dumps(result, indent=4))
    #     print()

    # with affiliate fee
    signature = Signature.from_string(
        "5Rxmv4h5ntR8Yozp1L7rLG54HWVgDUDpiC7EXfLwKg6N7z8qQFFwX9YJfAWxeA9vDvxGwRFArzMk24oCRoYCS5zQ"
    )
    result = get_tx_and_parse(signature, parsers[0])
    print(json.dumps(result, indent=4, default=str))

    # with no affiliate fee (was successful with old parser)
    signature = Signature.from_string(
        "37p3XLDxPcNbwDKNw2Adma3YDgbuyoAGwoc3TK4XnP8dyaKW8QaTH6CGqXQYch2hfcYsLpvH1azMQ33kgnS15v83"
    )
    expected_deposit_doc = {
        "scraper_originChain": "7565164",
        "scraper_blockNumber": 281109590,
        "scraper_blockTimestamp": 1722595729,
        "scraper_from": "C2ptaYeY83ndFt1axQaE3w7F9fxWzmCibnv9cmNUFbER",
        "scraper_protocol": "dln",
        "scraper_contractAddress": "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4",
        "scraper_tx_status": "ok",
        "scraper_tx_hash": "37p3XLDxPcNbwDKNw2Adma3YDgbuyoAGwoc3TK4XnP8dyaKW8QaTH6CGqXQYch2hfcYsLpvH1azMQ33kgnS15v83",
        "instruction_type": "outer_instruction",
        "tx": {
            "identifier": "createOrderWithNonce",
            "orderArgs": {
                "giveOriginalAmount": 2981416279,
                "take": {
                    "chainId": "56",
                    "tokenAddress": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
                    "amount": "2977793444404504181799",
                },
                "receiverDst": "0xa2e9370d8e888a79e8cb83d9c002d0f481b7e0c8",
                "givePatchAuthoritySrc": "C2ptaYeY83ndFt1axQaE3w7F9fxWzmCibnv9cmNUFbER",
                "allowedCancelBeneficiarySrc": None,
                "orderAuthorityAddressDst": "0xa2e9370d8e888a79e8cb83d9c002d0f481b7e0c8",
                "allowedTakerDst": None,
                "giveTokenAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            },
            "affiliateFee": None,
            "referralCode": 5022,
            "orderId": "0xbc4eac2ca927e3a9d3d8aa87333e939580af9e151ef2afde39b67f5d58fb886a",
            "nonce": 1722595724071,
            "metadata": "0x101010000a3e4120000000000000000000000000000000000273c62f9a8802f6da10000000000000000000000000000000000000000000000000000000000000000",
        },
        "scraper_function": "deposit",
        "scraper_chain_fee": 15001,
        "scraper_chain_prioritization_fee": 10000,
    }

    result = get_tx_and_parse(signature, parsers[0])
    print_diff(expected_deposit_doc, result)

    # fill example
    signature = Signature.from_string(
        "4hxiKWW5FGosAhevnKkUjkRDWVmGoC7KZeQYB4itvAeD2R3rtffRJkSAmqBniXcRbHGdm4Xzp1u1nA9MoijZeXoY"
    )
    expected_fill_doc = {
        "scraper_originChain": "7565164",
        "scraper_blockNumber": 276792628,
        "scraper_blockTimestamp": 1720631355,
        "scraper_from": "7FfB2zQRYUQwpPzkRxAeg2mCBGeCRKp4PCEeULJA9xTo",
        "scraper_protocol": "dln",
        "scraper_contractAddress": "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo",
        "scraper_tx_status": "ok",
        "scraper_tx_hash": "4hxiKWW5FGosAhevnKkUjkRDWVmGoC7KZeQYB4itvAeD2R3rtffRJkSAmqBniXcRbHGdm4Xzp1u1nA9MoijZeXoY",
        "instruction_type": "outer_instruction",
        "scraper_chain_fee": 1005001,
        "scraper_chain_prioritization_fee": 1000000,
        "tx": {
            "identifier": "fulfillOrder",
            "orderId": "0xafd3e671a10a838cb41703166182c46698793e0dfcab2e8d593d3558819795bc",
            "unlockAuthority": "7FfB2zQRYUQwpPzkRxAeg2mCBGeCRKp4PCEeULJA9xTo",
            "_order": {
                "makerOrderNonce": 1720631333780,
                "makerSrc": "0x25b60226c170fe88192b054666c90a00f52c4698",
                "give": {
                    "chainId": "42161",
                    "tokenAddress": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                    "amount": "1173693309",
                },
                "take": {
                    "chainId": "7565164",
                    "tokenAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    "amount": "1172807627",
                },
                "receiverDst": "2AueoQsAR2JQn9bVq6FCBhmEBRH31Cw5Dg5uayp8C8aB",
                "givePatchAuthoritySrc": "0x25b60226c170fe88192b054666c90a00f52c4698",
                "orderAuthorityAddressDst": "2AueoQsAR2JQn9bVq6FCBhmEBRH31Cw5Dg5uayp8C8aB",
                "allowedTakerDst": None,
                "allowedCancelBeneficiarySrc": None,
            },
        },
        "scraper_function": "fulfillOrder",
    }
    result = get_tx_and_parse(signature, parsers[1])
    print_diff(expected_fill_doc, result)
