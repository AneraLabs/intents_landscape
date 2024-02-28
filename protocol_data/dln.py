from borsh_construct import Option,CStruct,U32,U64,Bytes,U8

PROTOCOL_NAME = "dln"

contracts = {
    "7565164": {
        "deposit": "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4",
        "fill": "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo",
    }
}

identifiers = {
    "7565164": {
        "deposit": "828362be28ce4432",
        "fill": "3dd627f841d49924",
    }
}

abi = {
   "7565164": {
        "deposit": CStruct(
            "identifier" / U8[8],
            "orderArgs" / CStruct(
                "giveOriginalAmount" / U64,
                "take" / CStruct(
                    "chainId" / U8[32],
                    "tokenAddress" / Bytes,
                    "amount" / U8[32] 
                ),
                "receiverDst" / Bytes,
                "externalCall" / Option(Bytes),
                "givePatchAuthoritySrc" / U8[32],
                "allowedCancelBeneficiarySrc" / Option(U8[32]),
                "orderAuthorityAddressDst" / Bytes,
                "allowedTakerDst" / Option(Bytes)
            ),
            "affiliateFee" / Option(
                CStruct(
                    "beneficiary" / Bytes,
                    "amount" / U64
                )
            ),
            "referralCode" / Option(U32)
        ),
        "fill":  CStruct(
            "identifier" / U8[8],
            "unvalidatedOrder" / CStruct(
                "makerOrderNonce" / U64,
                "makerSrc" / Bytes,
                "give" / CStruct(
                    "chainId" / U8[32],
                    "tokenAddress" / Bytes,
                    "amount" / U8[32] 
                ),
                "take" / CStruct(
                    "chainId" / U8[32],
                    "tokenAddress" / Bytes,
                    "amount" / U8[32] 
                ),
                "receiverDst" / Bytes,
                "givePatchAuthoritySrc" / Bytes,
                "orderAuthorityAddressDst" / Bytes,
                "allowedTakerDst" / Option(Bytes),
                "allowedCancelBeneficiarySrc" / Option(Bytes),
                "externalCall" / Option(
                    CStruct(
                        "externalCallShortcut" / U8[32]
                    )
                ),
            ),
            "orderId" / U8[32],
            "unlockAuthority" / U8[32]
        )
   }
}


def get_contract_address(chain_id, contract_name):
    # Optionally configurable to be different per chain_id
    return contracts[chain_id][contract_name]

def get_function_identifier(chain_id, contract_name):
    return identifiers[chain_id][contract_name]

def get_contract_abi(chain_id, contract_name):
    return abi[chain_id][contract_name]

def get_supported_chains():
    return ["7565164"]

def get_deposit_function_filter():
    return None

def get_deposit_event_filter():
    return None

def get_fill_function_filter():
    return None

def get_fill_event_filter():
    return None
