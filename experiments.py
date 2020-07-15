import altair as alt
import pandas as pd

def plot(df, experiments, timezone):
    df = _extract(df, experiments, timezone)
    return _plot(df)

def _extract(df, experiments, timezone):
    data = []
    for experiment in experiments:
        begin, end, label = experiment
        begin = pd.to_datetime(begin).tz_localize(timezone)
        end = pd.to_datetime(end).tz_localize(timezone)
        for i, row in df[df.time.between(begin, end)].iterrows():
            data.append({
                "label" : label,
                "time" : (row.time - begin).total_seconds() // 60,
                "value" : row.value,
                "begin" : begin,
                "end" : end
            })
    return pd.DataFrame(data)

def _plot(df):
    scale_x = alt.Scale(domain=[0, 60])
    scale_y = alt.Scale(domain=[34, 41])
    chart = alt.Chart().encode(
        y=alt.Y("value:Q", axis=alt.Axis(grid=True, title="temperature (°C)"), scale=scale_y)
    ).properties(
        height=200
    )
    base = chart.encode(
        x=alt.X("time:Q", axis=alt.Axis(grid=True, title="time (minutes)"), scale=scale_x),
        color=alt.Color("begin:O", legend=None, scale=alt.Scale(range=["steelblue"])),
        tooltip=["time:Q", "value:Q", "label:O", "begin:O", "end:O"]
    )
    points = base.mark_point(opacity=1.0, filled=True, size=10).encode()
    lines = base.mark_line(interpolate="monotone", clip=True, opacity=0.4, strokeWidth=3).encode()
    return alt.layer(lines, points, data=df)

