# %%
from glob import glob
from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
import hvplot.xarray
import cartopy.crs as ccrs

# %%
def repair_trajectory_dataframe(df, hours):
    # ....Initialize a new dataframe
    ndf = pd.DataFrame({})
    for trj_df in df.groupby('trajectory'):
        # Extract trajectory and dataframe from group
        trj = trj_df[0]
        tdf = trj_df[1]
        # ....Check if trajectory dataframe has expected hours.
        #     If not, repair
        if len(tdf) < len(hours):
            for hour in hours:
                # ....Create date and time variables
                date = pd.Timestamp(df.year.iloc[0]+2000, df.month.iloc[0], df.day.iloc[0], df.hour.iloc[0]) + pd.Timedelta(hour, 'h')
                if hour not in tdf.time.values:
                    # ....Create a new row
                    new_row = pd.DataFrame({'trajectory': trj,
                                'run': 1,
                                'year': date.year,
                                'month': date.month,
                                'day': date.day,
                                'hour': date.hour,
                                'minute': 0,
                                'seconds': 0,
                                'time': hour,
                                'latitude': np.nan,
                                'longitude': np.nan,
                                'altitude': np.nan,
                                'pressure': np.nan,
                                'potential temperature': np.nan,
                                'air temperature': np.nan,
                                'rainfall': np.nan,
                                'mix depth': np.nan,
                                'relative humidity': np.nan,
                                'terrain above msl': np.nan,
                                'solar flux': np.nan,
                                }, index=[trj])
                    tdf = pd.concat([tdf, new_row.reset_index()])
        
        # ....Concat trajectory dataframe onto new dataframe
        ndf = pd.concat([ndf, tdf.reset_index()])
        ndf.reset_index(drop=True, inplace=True)

    return ndf

# %%
# ....Initialize variables
hours = np.arange(0,-121,-1).astype(float)
variables = ['latitude', 'longitude', 'altitude', 'pressure', 'potential temperature', 'air temperature', 'rainfall', 'mix depth', 'relative humidity', 'terrain above msl', 'solar flux']
time = []
ref_time_along_trajectories = np.nan * np.ones((121,1))
vertical_level = np.nan * np.ones((19,1))
ds = xr.Dataset({}, coords={'time': time})

fns = sorted(glob('/mnt/disk2/data/hysplit/backTrajectories/DYE-2*.trj'))
for fn in fns:
    print(fn)
    df = pd.read_csv(fn, skiprows=32, delimiter=r"\s+", names=['trajectory', 'run', 'year', 'month', 'day', 'hour', 'minute', 'seconds', 'time', 'latitude', 'longitude', 'altitude', 'pressure', 'potential temperature', 'air temperature', 'rainfall', 'mix depth', 'relative humidity', 'terrain above msl', 'solar flux'])
    time = [np.array(pd.Timestamp(2000+df.year[0], df.month[0], df.day[0], df.hour[0], df.minute[0], df.seconds[0]))]
    if fn == fns[0]:
        ref_time_along_trajectories = df[df.trajectory==1]['time'].values
        vertical_level = df.altitude.values[0:19]
    # ....Deals with trajectories that have less than desired number of hours
    ndf = repair_trajectory_dataframe(df, hours)
    # ....Convert dataframe to a dataset and append
    nds = xr.Dataset({'latitude':                            (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.latitude.values.reshape(1, 19, 121)),
                      'longitude':                           (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.longitude.values.reshape(1, 19, 121)),
                      'altitude':                            (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.altitude.values.reshape(1, 19, 121)),
                      'air_pressure':                        (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.pressure.values.reshape(1, 19, 121)*100.),
                      'air_potential_temperature':           (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['potential temperature'].values.reshape(1, 19, 121)),
                      'air_temperature':                     (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['air temperature'].values.reshape(1, 19, 121)),
                      'rainfall_rate':                       (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf.rainfall.values.reshape(1, 19, 121)/3600000.),
                      'atmosphere_boundary_layer_thickness': (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['mix depth'].values.reshape(1, 19, 121)),
                      'relative_humidity':                   (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['relative humidity'].values.reshape(1, 19, 121)),
                      'ground_level_altitude':               (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['terrain above msl'].values.reshape(1, 19, 121)),
                      'downward_solar_irradiance':           (['time', 'vertical_level', 'ref_time_along_trajectories'], ndf['solar flux'].values.reshape(1, 19, 121)),
                      }, 
                    coords={
                        'ref_time_along_trajectories': ref_time_along_trajectories,
                        'vertical_level': vertical_level,
                        'time': time})
    ds = xr.concat([ds, nds], dim='time')
ds['time'] = np.array([t.values for t in ds.time])

# %% - Add attributes to variables
ds['latitude'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'degrees_north',
                        'standard_name': 'latitude',
                        'long_name': 'latitude along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['longitude'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'degrees_east',
                        'standard_name': 'longitude',
                        'long_name': 'longitude along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['altitude'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'm',
                        'standard_name': 'altitude',
                        'long_name': 'altitude along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['air_pressure'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'Pa',
                        'standard_name': 'air pressure',
                        'long_name': 'air pressure along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['air_temperature'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'K',
                        'standard_name': 'air temperature',
                        'long_name': 'air temperature along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['air_potential_temperature'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'K',
                        'standard_name': 'air potential temperature',
                        'long_name': 'air potential temperature along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['relative_humidity'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': '1',
                        'standard_name': 'relative humidity',
                        'long_name': 'relative humidity along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['rainfall_rate'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'm s-1',
                        'standard_name': 'rainfall rate',
                        'long_name': 'rainfall rate along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['atmosphere_boundary_layer_thickness'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'm',
                        'standard_name': 'atmosphere boundary layer thickness (mix depth)',
                        'long_name': 'atmosphere boundary layer thickness (mix depth) along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['ground_level_altitude'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'm',
                        'standard_name': 'ground level altitude (terrain height) above mean sea level',
                        'long_name': 'ground level altitude (terrain height) above mean sea level along backward trajectories',
                        'other': 'HYSPLIT5 model output'}
ds['downward_solar_irradiance'].attrs = {'type': 'float32',
                        'dimension': 'time, vertical_level, ref_time_along trajectories',
                        'units': 'W m-2',
                        'standard_name': 'downward solar irradiance (solar flux)',
                        'long_name': 'downward solar irradiance (solar flux) along backward trajectories',
                        'other': 'HYSPLIT5 model output'}

# %% - Add global attributes
ds.attrs = {'Conventions': 'CF-1.8',
            'source': 'NOAA Global Forecast System (GFS) (0.25 degree, sigma-pressure hybrid) Model',
            'creator_name': 'Von P. Walden',
            'creator_email': 'v.walden@wsu.edu',
            'creator_url': 'https://orcid.org/0000-0003-3857-4416',
            'institution': 'Washington State University',
            'processing_software': 'Python scripts at https://github.com/icecaps-summit/back-trajectories',
            'sampling_interval': '5-day (120-hour) backward trajectories initialized every 1 hour',
            'product_version': 'v01',
            'last_revised_date': '2024-10-31T14:30:00',
            'project': 'ICECAPS - Integrated Characterization of Energy, Clouds, Atmospheric state and Precipitation at Summit',
            'project_principal_investigator': 'Von P. Walden',
            'project_principal_investigator_email': 'v.walden@wsu.edu',
            'project_principal_investigator_url': 'https://orcid.org/0000-0003-3857-4416',
            'title': 'Meteorological data along 5-day backward trajectories for DYE-2, Greenland',
            'feature_type': 'backward trajectory time series',
            'time_coverage_start': '2024-05-15T00:00:00',
            'time_coverage_end': '2024-08-10T23:00:00',
            'geospatial_bounds': '89.999N, -180.000W, 23.916N, 179.999E',
            'trajectory_initial_altitude': 'Trajectories simulated at 19 different vertical altitude levels above ground (100 to 9100 m, every 500 m)',
            'keywords': 'Greenland, DYE-2 site, atmosphere, backward trajectories',
            'history': 'This dataset consists of 2112 5-day backward trajectories initialized every 1h (00 to 23 UTC) from DYE-2, Greenland (66.48 N, 46.28 W) during the ICECAPS-MELT field campaign of summer 2024.  Trajectories have an hourly temporal resolution (121 hourly time steps) and are initialized from 19 different vertical starting levels. These levels are every 500 m between 100 and 9100 m. The backward trajectory variables have dimensions of (time,vertical_level,ref_time_along_trajectories) and are calculated using HYSPLIT v5 using NOAA Global Forecast System (0.25 degree, sigma-level hybrid) Model output.',
            'comment': 'Data was simulated using HYSPLIT v5 by Von P. Walden (v.walden@wsu.edu). See https://github.com/icecaps-summit/back-trajectories for more details.'
            }

# %%
ds.to_netcdf('/mnt/disk2/data/hysplit/backTrajectories/dye2_back_trajectories.nc')

# %%
ds.to_zarr('/mnt/disk2/data/hysplit/backTrajectories/dye2_back_trajectories')

# %%
