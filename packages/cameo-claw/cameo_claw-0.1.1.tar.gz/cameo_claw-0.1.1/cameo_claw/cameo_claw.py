import cameo_fastapi
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from multiprocessing import Pool
import psutil
from pathlib import Path
import os

router = APIRouter()


class ItemLstUrl(BaseModel):
    lst_url: list = []
    target_directory: str = './data/download/'


def download(str_url, target_directory='./data/download/'):
    Path(target_directory).mkdir(parents=True, exist_ok=True)
    r = requests.get(str_url, stream=True)
    if r.status_code == 200:
        content = r.raw.read()
        if len(content) > 256:
            filename = os.path.basename(str_url)
            with open(target_directory + filename, 'wb') as f:
                f.write(content)
                print('filename', filename, round(len(content) / 1024 / 1024, 2), 'MB')
            print('ram', round(psutil.virtual_memory().available / 1024 / 1024 / 1024, 2), 'GB')


def multiprocessing_download(lst_url, n_process=25):
    lst_output_path = []
    with Pool(n_process) as p:
        p.map(download, lst_url)
    return lst_output_path


@router.post('/api/cameo_claw/api_multiprocessing_download/',
             description='Multiprocessing download files',
             response_description='lst_output_path')
def api_multiprocessing_download(item_lst_url: ItemLstUrl):
    return multiprocessing_download(item_lst_url.lst_url, item_lst_url.target_directory)


app = cameo_fastapi.init()
app.include_router(router)


def run():
    cameo_fastapi.run('cameo_claw:app')
