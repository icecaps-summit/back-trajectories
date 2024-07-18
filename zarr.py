# %%
from glob import glob
from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
import hvplot.xarray
import cartopy.crs as ccrs

# %%
fns = sorted(glob('/mnt/disk2/data/hysplit/backTrajectories/Raven*.trj'))

# %%
# ....Initialize variables
variables = ['latitude', 'longitude', 'altitude', 'pressure', 'potential temperature', 'air temperature', 'relative humidity', 'mix depth', 'terrain above msl', 'solar flux']
time = []
ref_time_along_trajectories = np.nan * np.ones((121,1))
vertical_level = np.nan * np.ones((19,1))
latitude = np.nan * np.ones((121,19))
longitude = np.nan * np.ones((121,19))
altitude = np.nan * np.ones((121,19))
pressure = np.nan * np.ones((121,19))
potential_temperature = np.nan * np.ones((121,19))
air_temperature = np.nan * np.ones((121,19))
relative_humidity = np.nan * np.ones((121,19))
mix_depth = np.nan * np.ones((121,19))
terrain_above_msl = np.nan * np.ones((121,19))
solar_flux = np.nan * np.ones((121,19))

for fn in fns[0:2]:
    df = pd.read_csv(fn, skiprows=32, delimiter=r"\s+", names=['trajectory', 'run', 'year', 'month', 'day', 'hour', 'minute', 'seconds', 'time', 'latitude', 'longitude', 'altitude', 'pressure', 'potential temperature', 'air temperature', 'rainfall', 'mix depth', 'relative humidity', 'terrain above msl', 'solar flux'])
    time.append(np.array([pd.Timestamp(2000+df.year[0], df.month[0], df.day[0], df.hour[0], df.minute[0], df.seconds[0])]))
    if fn == fns[0]:
        ref_time_along_trajectories = df[df.trajectory==1]['time'].values
        vertical_level = df.altitude.values[0:19]
    # ....Deals with trajectories that have less than desired number of hours
    for group in df.groupby('trajectory'):
        latitude[group[0]-1] = group[1].latitude.values

# %%
df = pd.read_csv('/mnt/disk2/data/hysplit/backTrajectories/Raven_2024051500.trj', 
                     skiprows=32, 
                     delimiter=r"\s+", 
                     names=['trajectory', 
                            'run', 
                            'year', 
                            'month', 
                            'day', 
                            'hour', 
                            'minute', 
                            'seconds', 
                            'time', 
                            'latitude', 
                            'longitude', 
                            'altitude', 
                            'pressure', 
                            'potential temperature', 
                            'air temperature', 
                            'rainfall', 
                            'mix depth', 
                            'relative humidity', 
                            'terrain above msl', 
                            'solar flux'])

# %%
df.hvplot.points('longitude', 
                 'latitude', 
                 projection=ccrs.NorthPolarStereo(), 
                 coastline=True,
                 c=df['pressure'], 
                 cmap='viridis', 
                 )
# %%
reference_time = np.array([pd.Timestamp(2000+df.year[0], df.month[0], df.day[0], df.hour[0], df.minute[0], df.seconds[0])])
ref_time_along_trajectories = df[df.trajectory==1]['time'].values
vertical_level = df.altitude.values[0:19]
vars = ['latitude', 
        'longitude',
        'altitude',
        'pressure',
        'potential temperature',
        'air temperature',
        'rainfall',
        'mix depth',
        'terrain above msl',
        'solar flux'
        ]

# %%
ds = xr.Dataset({'latitude': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df.latitude.values.reshape(1, 121, 19)),
                 'longitude': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df.longitude.values.reshape(1, 121, 19)),
                 'altitude': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df.altitude.values.reshape(1, 121, 19)),
                 'pressure': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df.pressure.values.reshape(1, 121, 19)),
                 'potential temperature': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df['potential temperature'].values.reshape(1, 121, 19)),
                 'air temperature': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df['air temperature'].values.reshape(1, 121, 19)),
                 'rainfall': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df.rainfall.values.reshape(1, 121, 19)),
                 'mix depth': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df['mix depth'].values.reshape(1, 121, 19)),
                 'terrain above msl': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df['terrain above msl'].values.reshape(1, 121, 19)),
                 'solar flux': (['reference_time', 'ref_time_along_trajectories', 'vertical_level'], df['solar flux'].values.reshape(1, 121, 19)),
                 }, 
                coords={
                          'ref_time_along_trajectories': ref_time_along_trajectories,
                          'vertical_level': vertical_level,
                          'reference_time': reference_time})


# %%
