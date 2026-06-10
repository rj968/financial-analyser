# Made using AI :(

from __future__ import annotations
from pathlib import Path
import pandas as pd


class DataCache:
    """
    Loads CSVs from `data_dir`, caching them as Parquet in `cache_dir`.
    Re-reads the CSV only when it is newer than the cached file.
    """

    def __init__(self, data_dir: str = "data", cache_dir: str = "cache") -> None:
        self.data_dir = Path(data_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, name: str, *, force_refresh: bool = False) -> pd.DataFrame:
        """Load `name` (with or without .csv extension), using cache when fresh."""
        stem = Path(name).stem          # strips .csv if present
        csv_file = self.data_dir / f"{stem}.csv"
        cache_file = self.cache_dir / f"{stem}.parquet"

        if not csv_file.exists():
            raise FileNotFoundError(f"CSV not found: {csv_file}")

        cache_is_fresh = (
            not force_refresh
            and cache_file.exists()
            and cache_file.stat().st_mtime > csv_file.stat().st_mtime
        )

        if cache_is_fresh:
            try:
                return pd.read_parquet(cache_file)
            except Exception:
                # Corrupt or incomplete cache — fall through to re-read
                pass

        df = pd.read_csv(csv_file)
        df.to_parquet(cache_file, index=False)
        return df


# Module-level convenience — initialised lazily so import-time CWD doesn't matter
_default_cache: DataCache | None = None


def load_dataframe(
    name: str,
    *,
    data_dir: str = "data",
    cache_dir: str = "cache",
    force_refresh: bool = False,
) -> pd.DataFrame:
    """Load a dataframe by name using the default cache, with optional overrides."""
    global _default_cache
    if _default_cache is None:
        _default_cache = DataCache(data_dir=data_dir, cache_dir=cache_dir)
    return _default_cache.load(name, force_refresh=force_refresh)