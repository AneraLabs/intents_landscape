import importlib
from enabled_protocols import ENABLED_PROTOCOLS

known_modules = []

for protocol in ENABLED_PROTOCOLS:
    # Dynamically import protocol modules
    protocol_module = importlib.import_module(protocol)
    if protocol_module.PROTOCOL_NAME != protocol:
        print(f"Skipped {protocol} module as reported name doesn't match module name")
        continue

    globals()[protocol] = protocol_module
    known_modules.append(globals()[protocol].PROTOCOL_NAME)

for module in known_modules:
    print(globals()[module].PROTOCOL_NAME)
    print(globals()[module].get_contract_address(1))