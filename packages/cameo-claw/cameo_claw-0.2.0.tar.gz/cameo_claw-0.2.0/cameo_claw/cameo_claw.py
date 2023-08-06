import cameo_fastapi
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from multiprocessing import Pool
import psutil
from pathlib import Path
import os
import duckdb
import polars as pl

router = APIRouter()


class ItemLstUrl(BaseModel):
    lst_url: list = []
    target_directory: str = './data/download/'


def download(url, target_directory='./data/download/'):
    Path(target_directory).mkdir(parents=True, exist_ok=True)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        bytes1 = r.raw.read()
        if len(bytes1) > 256:
            filename = os.path.basename(url)
            with open(target_directory + filename, 'wb') as f:
                f.write(bytes1)
                print('filename', filename, round(len(bytes1) / 1024 / 1024, 2), 'MB')
            print('ram', round(psutil.virtual_memory().available / 1024 / 1024 / 1024, 2), 'GB')


def download_select_to_parquet(
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
        if len(bytes1) > 256:
            df = pl.read_csv(bytes1)
            df = df.distinct(subset=lst_distinct_column)
            df = df.select([pl.col(lst_select_column).filter(pl.col(filter_column) == filter_value)])
            filename = os.path.basename(url)
            path = target_directory + filename[:-7] + '.parquet'
            df.write_parquet(path)
            print('cameo_claw.py:', path)


def distinct_duckdb(source_directory='./data/download/*.csv.gz', target_path='./data/distinct/output.csv.gz'):
    print('ram', round(psutil.virtual_memory().available / 1024 / 1024 / 1024, 2), 'GB')
    print('distinct')
    source_directory = './data/download/*.csv'
    target_path = './data/distinct/all.csv'
    Path(os.path.dirname(target_path)).mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(database=':memory:')
    # createTime,deviceId,lat,localTime,lon,sensorId,value
    con.execute(
        f'''COPY (SELECT DISTINCT deviceId,lat,"localTime",lon,sensorId,value FROM '{source_directory}' WHERE sensorId='pm2_5' ORDER BY "localTime") TO '{target_path}' (FORMAT 'csv');''')
    print('ram', round(psutil.virtual_memory().available / 1024 / 1024 / 1024, 2), 'GB')


def multiprocessing_f(f, lst_url, n_process=25):
    with Pool(n_process) as p:
        p.map(f, lst_url)


def multiprocessing_download(lst_url):
    multiprocessing_f(download, lst_url)


def multiprocessing_download_select(lst_url):
    multiprocessing_f(download_select_to_parquet, lst_url)


@router.post('/api/cameo_claw/api_multiprocessing_download/',
             description='Multiprocessing download files',
             response_description='lst_output_path')
def api_multiprocessing_download(item_lst_url: ItemLstUrl):
    return multiprocessing_download(item_lst_url.lst_url, item_lst_url.target_directory)


app = cameo_fastapi.init()
app.include_router(router)


def run():
    cameo_fastapi.run('cameo_claw:app')
