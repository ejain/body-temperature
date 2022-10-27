import pandas as pd

def read_travel(path, timezone):
    df = pd.read_csv(path,
        usecols=["begin", "end"],
        index_col=False
    )
    df.begin = pd.to_datetime(df.begin, utc=False).dt.tz_localize(timezone)
    df.end = pd.to_datetime(df.end, utc=False).dt.tz_localize(timezone)
    return df
