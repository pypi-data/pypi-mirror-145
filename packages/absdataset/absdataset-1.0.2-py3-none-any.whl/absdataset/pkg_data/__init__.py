import os as __os
try:
    import pandas as __pd
except:
    raise SystemExit("No package found")

__here = __os.path.abspath(__os.path.dirname(__file__))

GGPLAY = __pd.read_csv(f"{__here}\googleplaystore.csv")
HEARTDATA = __pd.read_csv(f"{__here}\heart_2020_cleaned.csv")