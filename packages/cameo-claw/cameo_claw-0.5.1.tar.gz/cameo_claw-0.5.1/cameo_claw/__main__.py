import sys
import yaml
from cameo_claw import it_distinct, it_download, it_group

help_message = '''
🐲 001 Install cameo_claw package
python3 -m pip install cameo_claw

🍇 002 Multiprocessing download, distinct rows, group by columns:
python3 -m cameo_claw '
function: it_group
lst_url:
  - https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-30.csv
  - https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-31.csv
target_directory: ./data/topic_group/
lst_distinct_column:
  - deviceId
  - localTime
  - sensorId
lst_group_by_column:
  - deviceId
  - sensorId'

🐍 003 cameo_claw coding with python
from cameo_claw import it_group
lst_url=[
'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-30.csv',
'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-31.csv']
int_total=len(lst_url)
target_directory = './data/topic_group/'
lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
lst_group_by_column = ['deviceId', 'sensorId']
for int_progress, done_url in it_group(lst_url, target_directory, lst_distinct_column, lst_group_by_column):
    print(f'int_progress/int_total = {int_progress}/{int_total}')
    print(f'done url: {done_url}')
    
'''


def show_help():
    if len(sys.argv) == 1:
        print(help_message)
    if len(sys.argv) == 2:
        d = yaml.safe_load(sys.argv[1])
        if d['function'] == 'it_download':
            for int_progress, url in it_download(d['lst_url'], d['target_directory']):
                print(f'''{int_progress}/{len(d['lst_url'])}''', url)
        if d['function'] == 'it_distinct':
            for int_progress, url in it_distinct(d['lst_url'], d['target_directory'], d['lst_distinct_column']):
                print(f'''{int_progress}/{len(d['lst_url'])}''', url)
        if d['function'] == 'it_group':
            for int_progress, url in it_group(d['lst_url'], d['target_directory'], d['lst_distinct_column'],
                                              d['lst_group_by_column']):
                print(f'''{int_progress}/{len(d['lst_url'])}''', url)


if __name__ == '__main__':
    show_help()
