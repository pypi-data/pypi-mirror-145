from cameo_claw import multiprocessing_download_to_parquet

multiprocessing_download_to_parquet([
    'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-30.csv',
    'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-31.csv'
])
