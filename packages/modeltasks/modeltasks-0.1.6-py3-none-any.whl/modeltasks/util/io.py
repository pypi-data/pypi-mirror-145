import json
import pickle
from typing import Any
from pathlib import Path
from modeltasks.config import SETTINGS


def serialize(result: Path, value: Any = None):
    try:
        if value is not None:
            with open(result, 'w') as r:
                json.dump(value, r, sort_keys=True)
    except json.JSONDecodeError:
        if SETTINGS['allow_pickle']:
            try:
                pickle.dump(value, r, 5)
            except pickle.UnpicklingError:
                raise ValueError('Unsupported result value (Cannot serialize)')
        else:
            raise ValueError('Unsupported result value (Cannot serialize)')


def deserialize(result: Path):
    try:
        with open(result, 'r') as r:
            return json.load(r)
    except json.JSONDecodeError:
        if SETTINGS['allow_pickle']:
            try:
                return pickle.load(r)
            except pickle.UnpicklingError:
                raise ValueError('Invalid result file (Cannot deserialize)')
        else:
            raise ValueError('Unsupported result value (Cannot deserialize)')
