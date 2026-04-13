from pydantic import BaseModel
from src.backend import yaml


class InitialConfig(BaseModel):
    @classmethod
    def load(cls):
        with open("config/config.yml", encoding="utf-8") as f:
            content = yaml.safe_load(f)
            return InitialConfig(**(content if content is not None else {}))
