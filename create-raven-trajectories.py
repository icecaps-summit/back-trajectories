# %%
import sys
import pandas as pd
import numpy as np

# ....Import hysplit
sys.path.append('/home/vonw/work/software/backTrajectories/')
import hysplit

def download_GFS_data(date):
    # ....Retrieve GFS data for given date
    dates = pd.date_range(date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d'), freq='D')
    dataSource = 'GFS'
    hy = hysplit.HYSPLIT(dates,dataSource)
    hy.retrieveGFSdataFromNOAA()
    return

def generate_back_trajectories(date):
    # ....Create hysplit back trajectories for yesterday
    times = pd.date_range(date.strftime('%Y-%m-%d')+' 00:00', date.strftime('%Y-%m-%d')+' 23:00', freq='1h')
    dataSource = 'GFS'
    length = 120
    lat    = +66.5
    lon    = -46.3
    alts   = np.arange(100, 10000, 500)
    descriptor = 'Raven_'
    hy = hysplit.HYSPLIT(times,dataSource,length,lat,lon,alts,descriptor)
    hy.runBackTrajectory()
    return

# %%
date = pd.Timestamp.now()
datem1 = (date - pd.Timedelta('1 days'))

download_GFS_data(date)
generate_back_trajectories(datem1)

