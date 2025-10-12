import json
from typing import Any


def save_to_json(data: Any, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_from_json(filename: str) -> Any:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
