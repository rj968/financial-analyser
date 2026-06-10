from pathlib import Path

import numpy as np
import pandas as pd 
import scipy.stats as stats

import tools

df = tools.load("NIFTY 50-10-06-2025-to-10-06-2026.csv")
print(df.head())
