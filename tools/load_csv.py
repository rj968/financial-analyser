# cache/core.py
from __future__ import annotations
from pathlib import Path
from typing import Callable
import pandas as pd


class DataCache:
    def __init__(self, data_dir: str = "data", cache_dir: str = "cache") -> None:
        self.data_dir = Path(data_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        name: str,
        df: pd.DataFrame,
        *,
        transform: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    ) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected a DataFrame, got {type(df).__name__}")
        df = transform(df) if transform else df
        df.to_parquet(self._cache_path(name), index=False)
        return df

    def load(
        self,
        name: str,
        *,
        force_refresh: bool = False,
        transform: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    ) -> pd.DataFrame:
        stem = Path(name).stem
        csv_file = self.data_dir / f"{stem}.csv"
        cache_file = self._cache_path(name)

        cache_is_fresh = (
            not force_refresh
            and cache_file.exists()
            and (
                not csv_file.exists()
                or cache_file.stat().st_mtime > csv_file.stat().st_mtime
            )
        )

        if cache_is_fresh:
            try:
                return pd.read_parquet(cache_file)
            except Exception:
                pass

        if not csv_file.exists():
            raise FileNotFoundError(
                f"No CSV at {csv_file} and no valid cache for '{name}'. "
                "Use store() to cache a DataFrame directly."
            )

        df = pd.read_csv(csv_file)
        df = transform(df) if transform else df
        df.to_parquet(cache_file, index=False)
        return df

    def _cache_path(self, name: str) -> Path:
        return self.cache_dir / f"{Path(name).stem}.parquet"