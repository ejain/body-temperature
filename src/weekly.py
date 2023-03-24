import altair as alt

def plot(df, df_t):
    df = _first_of_day(df)
    df = _resample_weekly(df)
    return _plot(df, df_t)

def _first_of_day(df):
    return df.resample("D", on="time").agg("first").dropna().reset_index(drop=False)

def _resample_weekly(df):
    return df.set_index("time").value.resample("W-MON", label='left', closed='left').agg(["median", "min", "max"]).dropna().reset_index()

def _plot(df, df_t):
    scale_y = alt.Scale(domain=[36, 38])
    points = alt.Chart(df).mark_line(opacity=1.0, interpolate="monotone").encode(
        x=alt.X("time:T", axis=alt.Axis(grid=False, title=None)),
        y=alt.Y("median:Q", axis=alt.Axis(grid=True, title="temperature (°C)"), scale=scale_y),
        tooltip=["time:T", "median:Q", "min:Q", "max:Q"]
    ).properties(
        width=600,
        height=200
    )
    diff = points.mark_area(opacity=0.2, interpolate="monotone").encode(
        alt.Y("min:Q"),
        alt.Y2("max:Q")
    )
    travel_chart = alt.Chart(df_t).mark_rect(opacity=0.2, color="orange").encode(
        x="begin:T",
        x2="end:T",
        tooltip=["begin:T", "end:T"]
    )
    return points + diff + travel_chart
