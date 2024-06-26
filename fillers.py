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
    with open(f'intents_landscape/fillers/{file}', 'r') as f:
        filler_dict = json.load(f)
        KNOWN_FILLERS.append(Filler.from_dict(filler_dict))