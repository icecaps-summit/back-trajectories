# %%
import xarray as xr
import datetime as dt
import panel as pn
pn.extension()

# %%
raven_back_trajectories = xr.open_dataset('/mnt/disk2/data/hysplit/backTrajectories/raven_back_trajectories.nc')

# %%
def trajectory_plot(raven_back_trajectories):
    trj_plot = 
    return trj_plot
# %%
trajectories = pn.widgets.IntRangeSlider(
    name='Vertical Level of Trajectory (m)',
    start=100, 
    end=9100, 
    value=(100, 100), 
    step=500,
    bar_color='green')

trajectories

# %%
trj_time = pn.widgets.DatetimePicker(
    name='Date of Trajectories', 
    value=dt.datetime(2024, 5, 15),
    start=dt.datetime(2024, 5, 15),
    end = dt.datetime.today() - dt.timedelta(days=1)
)

pn.Column(trj_time)

# %%
import panel.widgets as pnw

# %%
trj_time  = pnw.IntSlider(name='time', start=0, end=len(raven_back_trajectories.time)-1)
trj_level = pnw.IntSlider(name='level', start=0, end=len(raven_back_trajectories.vertical_level)-1)

variables = ['altitude', 'pressure', 'potential temperature', 'air temperature', 'rainfall', 'mix depth', 'relative humidity', 'terrain above msl', 'solar flux']
variable  = variables[3]
raven_back_trajectories[variable].interactive(width=800).isel(time=trj_time, vertical_level=trj_level).hvplot(ylim=[220, 300])

# %%
x='longitude', y='latitude', geo=True, coastlines=True, xlim=[-90,0], ylim=[45,90])

# %%
colorScaleVariable = 'altitude'
plot = raven_back_trajectories.sel(time='2024-05-15 00:00', method='nearest').hvplot.points(x='longitude', y='latitude', 
                    geo=True, 
                    c=raven_back_trajectories[colorScaleVariable], 
                    clabel=colorScaleVariable,
                    cmap='viridis', 
                    tiles='StamenTerrain', 
                    title='Back Trajectories for Raven 2024:' + colorScaleVariable)
# %%
