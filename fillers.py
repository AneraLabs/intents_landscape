import json
import os
from dataclasses import dataclass


@dataclass
class Filler:
    name: str
    addresses: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Filler':
        return cls(**data)


KNOWN_FILLERS: list[Filler] = []


# all files in the fillers folder
for file in os.listdir('intents_landscape/fillers'):
    if file.endswith('.json'):
        with open(f'intents_landscape/fillers/{file}', 'r') as f:
            filler_dict = json.load(f)
        KNOWN_FILLERS.append(Filler.from_dict(filler_dict))


def get_filler_by_address(address: str) -> Filler | None:
    for filler in KNOWN_FILLERS:
        if address in filler.addresses:
            return filler
    return None


def get_filler_by_name(name: str) -> Filler | None:
    for filler in KNOWN_FILLERS:
        if filler.name == name:
            return filler
    return None


if __name__ == '__main__':
    # check if all fillers are loaded with no errors
    for filler in KNOWN_FILLERS:
        print(filler.name)