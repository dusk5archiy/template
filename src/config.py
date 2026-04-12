from pydantic import BaseModel
from src.backend import yaml


class ParsedConfig(BaseModel):
    pass


def load_config(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        content = ParsedConfig(**yaml.safe_load(f))

    return content
