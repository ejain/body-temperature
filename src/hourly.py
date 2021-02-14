import altair as alt

def plot(df):
    scale_y = alt.Scale(domain=[36, 38])
    points = alt.Chart().mark_point(opacity=0.4, filled=True, size=50).encode(
        x=alt.X("hours(time):T", axis=alt.Axis(grid=False, title="hour of day")),
        y=alt.Y("value:Q", axis=alt.Axis(grid=True, title="temperature (°C)"), scale=scale_y),
        tooltip=["monthdate(time)", "hours(time)", "value"]
    ).properties(
        width=600,
        height=200
    )
    medians = alt.Chart().mark_tick(opacity=1.0, thickness=2).encode(
        x=alt.X("hours(time):T", axis=alt.Axis(grid=False, title="hour of day")),
        y=alt.Y("median(value):Q", axis=alt.Axis(grid=True, title="temperature (°C)"), scale=scale_y)
    )
    return alt.layer(points, medians, data=df)
