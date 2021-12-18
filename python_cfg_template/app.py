import os
from importlib import reload

"""Using pydantic to manage and validate config file"""

if __name__ == "__main__":
    os.environ["APP_ENV"] = "prd"
    import config

    print(config.config.train_config.debug)

    os.environ["APP_ENV"] = "dev"
    reload(config)
    print(config.config.train_config.debug)
