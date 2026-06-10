# cache/__init__.py
from .load_csv import DataCache
from pathlib import Path
from typing import Callable
import pandas as pd

_default: DataCache | None = None


def _get_default() -> DataCache:
    global _default
    if _default is None:
        _default = DataCache()
    return _default


def load(
    name: str,
    *,
    force_refresh: bool = False,
    transform: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
) -> pd.DataFrame:
    return _get_default().load(name, force_refresh=force_refresh, transform=transform)


def store(
    name: str,
    df: pd.DataFrame,
    *,
    transform: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
) -> pd.DataFrame:
    return _get_default().store(name, df, transform=transform)


def configure(data_dir: str = "data", cache_dir: str = "cache") -> None:
    """Call this once at startup to override default paths."""
    global _default
    _default = DataCache(data_dir=data_dir, cache_dir=cache_dir)


__all__ = ["DataCache", "load", "store", "configure"]