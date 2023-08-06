try:
    import pandas as __pd
except:
    raise SystemExit("No package found")


GGPLAY = __pd.read_csv("googleplaystore.csv")
HEARTDATA = __pd.read_csv("heart_2020_cleaned.csv")