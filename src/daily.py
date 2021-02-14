import altair as alt

def plot(df, window=7):
    df = _first_of_day(df)
    df = _with_rolling_median(df, window)
    return _plot(df)

def _first_of_day(df):
    return df.resample("D", on="time").agg("first").dropna().reset_index(drop=True)

def _with_rolling_median(df, window):
    return df.assign(value_median=df["value"].rolling(window).median())

def _plot(df):
    scale_y = alt.Scale(domain=[36, 38])
    points = alt.Chart(df).mark_point(opacity=1.0, filled=True, size=50).encode(
        x=alt.X("time:T", axis=alt.Axis(grid=False, title=None)),
        y=alt.Y("value:Q", axis=alt.Axis(grid=True, title="temperature (°C)"), scale=scale_y),
        tooltip=["monthdate(time)", "hoursminutes(time)", "value"]
    ).properties(
        width=600,
        height=200
    )
    diff = points.mark_bar(opacity=0.4).encode(
        alt.Y("value:Q"),
        alt.Y2("value_median:Q")
    ).transform_filter(
        alt.datum.value_median > 0
    )
    return points + diff
