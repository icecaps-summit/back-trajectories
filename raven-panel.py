# %%
import numpy as np
import xarray as xr
import hvplot.xarray
import datetime as dt
import panel as pn
pn.extension()

# %%
raven_back_trajectories = xr.open_dataset('/mnt/disk2/data/hysplit/backTrajectories/raven_back_trajectories.nc')

# %%
def trajectory_plot(variable='latitude', time=dt.datetime(2024, 5, 15, 0), level=100):
    return raven_back_trajectories.sel(time=time, vertical_level=level, method='nearest')[variable].hvplot()

# %%
variables = [variable for variable in raven_back_trajectories.variables][0:11]
variable_widget = pn.widgets.Select(name='Trajectory Variable', options=variables)
#time_widget = pn.widgets.DatetimePicker(name='Date of Trajectories', value=dt.datetime(2024, 5, 15), start=dt.datetime(2024, 5, 15), end = dt.datetime.today() - dt.timedelta(days=1))
#time_widget = pn.widgets.DateSlider(name='Date of Trajectories', value=dt.datetime(2024, 5, 15, 0), start=dt.datetime(2024, 5, 15, 0), end = dt.datetime.today() - dt.timedelta(days=1))
time_widget = pn.widgets.DiscreteSlider(name='Date of Trajectories', options=list(raven_back_trajectories.time.values), value=raven_back_trajectories.time[0].values, bar_color='green')
level_widget = pn.widgets.IntSlider(name='Vertical Level of Trajectory (m)', start=100, end=9100, value=100, step=500, bar_color='green')

# %%
plot = pn.bind(trajectory_plot, variable=variable_widget, time=time_widget, level=level_widget)
widgets = pn.Column(variable_widget, time_widget, level_widget)
pn.Column(widgets, plot).show()

