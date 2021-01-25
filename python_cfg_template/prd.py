# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel


class TrainConfig(BaseModel):
    epochs: int = 10
    debug: bool = False
    hidden_layers: List[int] = [1024, 512]


class TestConfig(BaseModel):
    debug: bool = False
    output_file: str = "output.csv"


class Config(BaseModel):
    train_config: TrainConfig = TrainConfig()
    test_config: TestConfig = TestConfig()


if __name__ == "__main__":
    config = Config()
    print(config)
