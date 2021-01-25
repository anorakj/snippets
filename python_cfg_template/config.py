# -*- coding: utf-8 -*-
import os

if os.environ["APP_ENV"] == "prd":
    from prd import Config
if os.environ["APP_ENV"] == "dev":
    from dev import Config
config = Config()
