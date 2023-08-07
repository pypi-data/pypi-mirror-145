from cameo_claw import it_distinct, it_download, it_group, it_filter
import time
from cameo_claw.log import log


def get_lst_url_taipei_100():
    lst_device_id = [
        "10180507985",
        "10183804818",
        "10180935138",
        "10182362729",
        "10186915768",
        "10182765572",
        "10183643733",
        "10187817545",
        "10180711468",
        "10181888891",
        "10184237251",
        "10200376949",
        "10187714974",
        "10188959173",
        "10181133624",
        "10189875513",
        "10184780057",
        "10187536226",
        "10188542674",
        "10187616860",
        "10190212306",
        "10200485379",
        "10184404771",
        "10188107333",
        "10186524358",
        "10187942042",
        "10183163884",
        "10180654119",
        "10185092420",
        "10187452115",
        "10190000864",
        "10190479538",
        "10185579073",
        "10181983795",
        "10188844366",
        "10189360662",
        "10182995926",
        "10181055695",
        "10189089883",
        "10181464107",
        "10184979038",
        "10181258942",
        "10184871059",
        "10185137651",
        "10182074994",
        "10190374312",
        "10186752944",
        "10189461434",
        "10184589018",
        "10181395211",
        "10186372622",
        "10186223376",
        "10182118699",
        "10190513901",
        "10185716972",
        "10189779191",
        "10188219952",
        "10185390063",
        "10181621345",
        "10182567005",
        "10186123517",
        "10188652949",
        "10184615499",
        "10189289540",
        "10182827296",
        "10185414614",
        "10184032107",
        "10185295344",
        "10182603505",
        "10186080368",
        "10187340888",
        "10186497242",
        "10187268812",
        "10183739942",
        "10188795449",
        "10183269165",
        "10183435474",
        "10180884769",
        "10188098571",
        "10183378041",
        "10185861505",
        "10183938343",
        "10185920135",
        "10181700710",
        "10188450871",
        "10186643177",
        "10184128532",
        "10190122978",
        "10188364226",
        "10184373796",
        "10186871514",
        "10181510720",
        "10183091769",
        "10187195615",
        "10182493773",
        "10187012610",
        "10182273531",
        "10183554350",
        "10185613026",
        "10189170767",
    ]
    return get_lst_url_by_date(lst_device_id)


def get_lst_url_50():
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
    return get_lst_url_by_date(lst_device_id)


def get_lst_url_by_date(lst_device_id):
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
    int_total = len(get_lst_url_50())
    for int_progress, done_url in it_download(get_lst_url_50(), target_directory):
        print_progress(done_url, int_progress, int_total)


def test_it_distinct():
    target_directory = './data/topic_distinct/'
    int_total = len(get_lst_url_50())
    lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
    for int_progress, done_url in it_distinct(get_lst_url_50(), target_directory, lst_distinct_column):
        print_progress(done_url, int_progress, int_total)


def print_progress(done_url, int_progress, int_total):
    print(f'int_progress/int_total = {int_progress}/{int_total}')
    print(f'done url: {done_url}')


def test_it_group():
    target_directory = './data/topic_group/'
    int_total = len(get_lst_url_50())
    lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
    lst_group_by_column = ['deviceId', 'sensorId']
    for int_progress, done_url in it_group(get_lst_url_50(), target_directory, lst_distinct_column,
                                           lst_group_by_column):
        print_progress(done_url, int_progress, int_total)


def test_it_filter():
    target_directory = './data/topic_filter/'
    int_total = len(get_lst_url_taipei_100())
    lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
    lst_column_match = [['sensorId', 'pm2_5'], ]
    sort_column = 'localTime'
    for int_progress, done_url in it_filter(
            get_lst_url_taipei_100(), target_directory, lst_distinct_column,
            lst_column_match, sort_column):
        pass
        # print_progress(done_url, int_progress, int_total)


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
