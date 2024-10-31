# %%
from metpy.calc import mixing_ratio_from_relative_humidity, specific_humidity_from_mixing_ratio
from metpy.units import units
from geopy.distance import geodesic
from glob import glob
import numpy as np
import pandas as pd
import xarray as xr
import hvplot.xarray
import holoviews as hv
#import panel as pn

hvplot.extension('bokeh', comms='vscode')

# %%
d = '/mnt/disk2/data/hysplit/backTrajectories/'
dstr = '2024'
fns = sorted(glob(d + 'DYE-2_' + dstr + '*.trj'))

time       = []
lat_median = []
alt_min    = []
dTheta     = []
q_mean     = []
dq         = []

for fn in fns:
    dstr = fn.split('/')[-1]
    time.append(pd.Timestamp(dstr[6:10]+'-'+dstr[10:12]+'-'+dstr[12:14]+' '+dstr[14:16]))
    df = pd.read_csv(fn, 
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
                            'solar flux'
                            ]
                    )

    height = df.altitude[0:19]     # ending altitudes
    lat_median.append(df.groupby('trajectory')['latitude'].median().values)
    alt_min.append(df.groupby('trajectory')['altitude'].min().values)
    dTheta_min = (df.groupby('trajectory')['potential temperature'].min().values - df['potential temperature'][0:19]).values
    dTheta_max = (df.groupby('trajectory')['potential temperature'].max().values - df['potential temperature'][0:19]).values
    dTheta.append([np.array(max(values, key=abs)) for values in zip(dTheta_min, dTheta_max)])
    w = mixing_ratio_from_relative_humidity(df['pressure'].values*units.hPa, df['air temperature'].values*units.K, df['relative humidity'].values/100.).to('g/kg')
    df['specific humidity'] = specific_humidity_from_mixing_ratio(w)
    dq_min = (df.groupby('trajectory')['specific humidity'].min().values - df['specific humidity'][0:19]).values
    dq_max = (df.groupby('trajectory')['specific humidity'].max().values - df['specific humidity'][0:19]).values
    dq.append([np.array(max(values, key=abs)) for values in zip(dq_min, dq_max)])
    q_mean.append(df.groupby('trajectory')['specific humidity'].mean().values)

lat_median = np.array(lat_median)
height = height.values
ds = xr.Dataset(data_vars={'lat_median': (['time', 'height'], lat_median),
                           'alt_min':    (['time', 'height'], alt_min),
                           'dTheta':     (['time', 'height'], dTheta),
                           'q_mean':     (['time', 'height'], q_mean),
                           'dq':         (['time', 'height'], dq),
                           }, 
                coords={'time': ('time', time), 
                        'height': ('height', height)})

p_lat_median = ds.lat_median.hvplot(x='time', y='height', cmap='viridis_r', ylim=(0,10000), clim=(45,85), clabel='Median Latitude', height=300, responsive=True).opts(title='HYSPLIT-5 Back Trajectories for DYE-2, Greenland 2024')
p_alt_min    = ds.alt_min.hvplot(x='time', y='height', cmap='viridis_r', ylim=(0,10000), clim=(0,10000), clabel='Minimum Altitude', height=300, responsive=True)
p_dTheta     = ds.dTheta.hvplot(x='time', y='height', cmap='RdBu_r', ylim=(0,10000), clim=(-30,30), clabel='d(Potential Temperature)', height=300, responsive=True)
p_q_mean     = ds.q_mean.hvplot(x='time', y='height', cmap='Blues', ylim=(0,10000), clabel='Specific Humidity, q (g/kg)', height=300, responsive=True)
p_dq         = ds.dq.hvplot(x='time', y='height', cmap='RdBu', ylim=(0,10000), clim=(-10,10), clabel='Change in specific humidity, dq (g/kg)', height=300, responsive=True)

plots = hv.Layout([p_lat_median, p_alt_min, p_dTheta, p_q_mean, p_dq]).cols(1)
hvplot.save(plots, 'docs/index.html')

#TAB = pn.Column(pn.pane.Markdown('# HYSPLIT-5 Back Trajectories for DYE-2, Greenland 2024'), p_lat_median, p_alt_min, p_dTheta, p_q_mean, p_dq)
#pn.Row(TAB, sizing_mode='stretch_width', width_policy='max').servable()

# %%
