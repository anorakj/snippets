# -*- coding: utf-8 -*-
from pydantic import BaseModel

from prd import TrainConfig, TestConfig


class DevTrainConfig(TrainConfig):
    debug: bool = True


class DevTestConfig(TestConfig):
    debug: bool = True


class Config(BaseModel):
    train_config: DevTrainConfig = DevTrainConfig()
    test_config: DevTestConfig = DevTestConfig()


if __name__ == "__main__":
    config = Config()
    print(config)
