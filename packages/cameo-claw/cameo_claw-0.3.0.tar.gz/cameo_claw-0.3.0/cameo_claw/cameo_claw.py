import requests
from multiprocessing import Pool
from pathlib import Path
import os
import polars as pl


def download_to_parquet(
        url,
        lst_select_column=['createTime', 'deviceId', 'lat', 'localTime', 'lon', 'sensorId', 'value'],
        lst_distinct_column=['deviceId', 'localTime', 'sensorId'],
        filter_column='sensorId',
        filter_value='pm2_5',
        target_directory='./data/parquet/'):
    Path(target_directory).mkdir(parents=True, exist_ok=True)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        bytes1 = r.raw.read()
        if len(bytes1) > 180:
            df = pl.read_csv(bytes1)
            df = df.distinct(subset=lst_distinct_column)
            df = df.select([pl.col(lst_select_column).filter(pl.col(filter_column) == filter_value)])
            filename = os.path.basename(url)
            filename = filename[:filename.find('.')]
            path = target_directory + filename + '.parquet'
            df.write_parquet(path)
            print('Output:', path)


def multiprocessing_download_to_parquet(lst_url, n_process=25):
    with Pool(n_process) as p:
        p.map(download_to_parquet, lst_url)
