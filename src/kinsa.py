import re
from datetime import datetime

import pandas as pd

_date_pattern = re.compile(
    r"\[\w{3}, (\w{3}) (\d{1,2}), (\d{4})\]" # [Sat, Jan 1, 2022]
)

_record_pattern = re.compile(
    r"\s+\[(\d{1,2}:\d{2} (?:AM|PM))\] " + # [8:22 AM] 
    r"Temperature \((.+?), (.+?)\): " + # Temperature (Oral Reading, QuickCare): 
    r"(\d+?\.\d+?)°C.+?\." # 36.9°C No Fever.
)

def parse(path, timezone):
    records = []
    with open(path, encoding="utf-8") as source:
        for line in source:
            if line.strip() == "":
                month = None
                day_of_month = None
                year = None
            date_match = _date_pattern.match(line)
            if date_match:
                month = date_match.group(1)
                day_of_month = date_match.group(2)
                year = int(date_match.group(3))
                continue
            record_match = _record_pattern.match(line)
            if record_match:
                if year is None:
                    raise ValueError("Couldn't find a date before processing line <%s>" % (line))
                records.append({
                    "time": _isoformat(year, month, day_of_month, record_match.group(1), timezone),
                    "site": record_match.group(2),
                    "device": record_match.group(3),
                    "value": float(record_match.group(4))
                })
                continue
    return _df(records, timezone)

def _isoformat(year, month, day_of_month, time_of_day, timezone):
    s = "%d %s %s %s" % (year, month, day_of_month, time_of_day)
    return timezone.localize(datetime.strptime(s, "%Y %b %d %I:%M %p"))

def _df(records, timezone):
    df = pd.DataFrame(records)
    df.time = pd.to_datetime(df.time).dt.tz_convert(timezone)
    df = df.sort_values("time", ignore_index=True)
    df.reset_index()
    return df
