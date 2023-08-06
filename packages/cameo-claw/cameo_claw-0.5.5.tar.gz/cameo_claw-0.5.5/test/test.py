from cameo_claw import it_distinct, it_download, it_group, it_filter
import time
from cameo_claw.log import log


def get_lst_url():
    lst_device_id = [
        "11144353041",
        "11135655524",
        "11146220817",
        "11134915729",
        "11144949700",
        "11145345031",
        "11144535597",
        "11150348864",
        "11152332479",
        "11137445267",
        "11142706581",
        "11139427726",
        "11132757143",
        "11143315941",
        "11145428733",
        "11138263064",
        "11149040829",
        "11135424517",
        "11147350591",
        "11132265371",
        "11136533184",
        "11141843507",
        "11136480034",
        "11149117865",
        "11148832575",
        "11133512028",
        "11143988456",
        "11143119216",
        "11134364858",
        "11143240238",
        "11132477607",
        "11146482455",
        "11131367272",
        "11151053715",
        "11138740618",
        "11143570743",
        "11132083287",
        "11135577162",
        "11144277295",
        "11134472620",
        "11151283365",
        "11147041406",
        "11131824250",
        "11136322895",
        "11149357462",
        "11131209112",
        "11139221095",
        "11148103547",
        "11145230386",
        "11132685693",
    ]
    lst_url = []
    for device_id in lst_device_id:
        for i in range(1, 32):
            day = f'2022-03-{i:02}'
            url = f'https://iot.epa.gov.tw/fapi_open/topic-device-daily/topic_save.industry.rawdata.material/device_{device_id}/device_{device_id}_daily_{day}.csv.gz'
            lst_url.append(url)
    return lst_url


# def test_filter():
#     lst_select_column = ['createTime', 'deviceId', 'lat', 'localTime', 'lon', 'sensorId', 'value']
#     lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
#     filter_column = 'sensorId'
#     filter_value = 'pm2_5'
#     target_directory = './data/parquet/'
#     multiprocessing_download_to_parquet(
#         get_lst_url(),
#         lst_select_column,
#         lst_distinct_column,
#         filter_column,
#         filter_value,
#         target_directory)

def test_it_download():
    target_directory = './data/topic_download/'
    int_total = len(get_lst_url())
    for int_progress, done_url in it_download(get_lst_url(), target_directory):
        print(f'int_progress/int_total = {int_progress}/{int_total}')
        print(f'done url: {done_url}')


def test_it_distinct():
    target_directory = './data/topic_distinct/'
    int_total = len(get_lst_url())
    lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
    for int_progress, done_url in it_distinct(get_lst_url(), target_directory, lst_distinct_column):
        print(f'int_progress/int_total = {int_progress}/{int_total}')
        print(f'done url: {done_url}')


def test_it_group():
    target_directory = './data/topic_group/'
    int_total = len(get_lst_url())
    lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
    lst_group_by_column = ['deviceId', 'sensorId']
    for int_progress, done_url in it_group(get_lst_url(), target_directory, lst_distinct_column, lst_group_by_column):
        print(f'int_progress/int_total = {int_progress}/{int_total}')
        print(f'done url: {done_url}')


def test_it_filter():
    target_directory = './data/topic_filter/'
    int_total = len(get_lst_url())
    lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
    lst_column_match = [['sensorId', 'pm2_5'], ['sensorId', 'voc']]
    sort_column = 'localTime'
    for int_progress, done_url in it_filter(
            get_lst_url(), target_directory, lst_distinct_column,
            lst_column_match, sort_column):
        print(f'int_progress/int_total = {int_progress}/{int_total}')
        print(f'done url: {done_url}')


if __name__ == '__main__':
    # t = time.time()
    # test_it_download()
    # log(f'test_it_download:{time.time() - t}')
    #

    # t = time.time()
    # test_it_distinct()
    # log(f'test_it_distinct:{time.time() - t}')

    # t = time.time()
    # test_it_group()
    # log(f'test_it_group:{time.time() - t}')

    t = time.time()
    test_it_filter()
    log(f'test_it_filter:{time.time() - t}')

# sh/go.sh
