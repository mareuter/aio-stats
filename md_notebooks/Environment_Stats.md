---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import calendar
import pathlib

from IPython.display import Markdown as md
import plotly.graph_objects as go

import aio_stats
import aio_stats.plotting as asp
```

```python editable=true slideshow={"slide_type": ""} tags=["parameters"]
location = "office"
year = 2024
month = 9
```

```python
data_path = f"~/Documents/SensorData/{location}"
temp_data_path = f"{data_path}/temperature/{year}/{month:02}"
rh_data_path = f"{data_path}/relative-humidity/{year}/{month:02}"
```

```python
m = calendar.Month(month)
```

```python
temp_data = aio_stats.DataReader(pathlib.Path(temp_data_path))
rh_data = aio_stats.DataReader(pathlib.Path(rh_data_path))

temp_data.read_month()
rh_data.read_month()

temp_df = temp_data.table.to_pandas()
rh_df = rh_data.table.to_pandas()
```

```python
layout = dict(height=500, width=700)
```

```python
md(f"# <center>{location.title()} Environment for {m.name.title()} {year}</center>")
```

```python
fig1 = go.Figure(layout=layout)
asp.make_stats_trend("Temp", fig1, temp_df)
```

```python
fig2 = go.Figure(layout=layout)
asp.make_min_max_dist("Temp", fig2, temp_df)
```

```python
fig3 = go.Figure(layout=layout)
asp.make_stats_trend("RH", fig3, rh_df)
```

```python
fig4 = go.Figure(layout=layout)
asp.make_min_max_dist("RH", fig4, rh_df)
```

```python

```
