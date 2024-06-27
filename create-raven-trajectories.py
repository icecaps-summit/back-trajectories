# %%
import sys
import pandas as pd
import numpy as np
from multiprocessing import Pool

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

def generate_back_trajectories(times):
    # ....Create hysplit back trajectories for particular time 
    dataSource = 'GFS'
    length = 120    # 120 hours = 5 days
    lat    = +66.5
    lon    = -46.3
    alts   = np.arange(100, 10000, 500)
    descriptor = 'Raven_'
    hy = hysplit.HYSPLIT(times,dataSource,length,lat,lon,alts,descriptor)
    hy.runBackTrajectory()
    return

# %%
today     = pd.Timestamp.now()
yesterday = today - pd.Timedelta('1 days')
times = pd.date_range(yesterday.strftime('%Y-%m-%d')+' 00:00', yesterday.strftime('%Y-%m-%d')+' 23:00', freq='1h')

download_GFS_data(today)
generate_back_trajectories(times)
