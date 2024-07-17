# %%
from datetime import datetime
import pandas as pd
import xarray as xr
import hvplot.xarray
import cartopy.crs as ccrs

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
