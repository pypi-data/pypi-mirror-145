"""Caching decorator for functions returning pd.DataFrame objects"""
import datetime as dt
import os
from functools import wraps
from typing import Any

import pandas as pd

from .logger import get_logger

log = get_logger(__name__)


def df_cache(func):
    """Caching decorator for functions returning pd.DataFrame"""
    cache_dir = "cache/"

    @wraps(func)
    def inner_func(*args: Any, **kwargs: Any):
        """Function to be decorated"""
        file_name = cache_dir + func.__name__
        if not args and not kwargs:
            file_name += f"_run_{dt.date.today().isoformat()}.snappy.parquet"
        else:
            file_name = (
                file_name
                + "_"
                + "_".join(map(str, args))
                + "_"
                + "_".join([f"{str(k)}__{str(v)}" for k, v in kwargs.items()])
                + ".snappy.parquet"
            )
        if os.path.isfile(file_name):
            log.info("Reading %s from cache", func.__name__)
            return pd.read_parquet(file_name)

        result = func(*args, **kwargs)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        log.info("Caching %s", func.__name__)
        result.to_parquet(file_name)
        return result

    return inner_func
