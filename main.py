from pathlib import Path

import numpy as np
import pandas as pd 
import scipy.stats as stats

from tools.load_csv import load_dataframe

df = load_dataframe("NIFTY 50-10-06-2025-to-10-06-2026.csv")
print(df.head())
