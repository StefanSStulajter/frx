import os
import pandas as pd
import plotly as py
import plotly.graph_objs as pygo
import plotly.tools as pyt

print(os.getcwd())

dateTimeFormat = "%d.%m.%Y %H:%M:%S.%f"
unit = "(hour)"

df = pd.read_csv("resources/data/frx/test.csv")

# TODO: To be removed
# Dropping most of the values (for performance purposes)
df = df[0:100]

df.columns = ["date", "open", "high", "low", "close", "volume"]
df.date = pd.to_datetime(df.date, format=dateTimeFormat)

# Setting "date" as the index
df = df.set_index(df.date)
# Dropping original "date" column (since now it's index)
df = df[["open", "high", "low", "close", "volume"]]
# Dropping duplicate values (downtimes)
df = df.drop_duplicates(keep=False)

# Adding additional analytics columns
movingAverage30 = df.close.rolling(center=False, window=30).mean()

# Plotting
# Traces
traceOhlc = pygo.Ohlc(x=df.index, open=df.open, high=df.high, low=df.low, close=df.close, name="OHLC")
traceMean = pygo.Scatter(x=df.index, y=movingAverage30, name="Rolling mean 30 %s" % unit)
traceVolume = pygo.Bar(x=df.index, y=df.volume, name="Volume")

# Figure
fig = pyt.make_subplots(rows=2, cols=1, shared_xaxes=True)
fig.append_trace(traceOhlc, 1, 1)
fig.append_trace(traceMean, 1, 1)
fig.append_trace(traceVolume, 2, 1)

# Plot
py.offline.plot(fig, filename="test.html")