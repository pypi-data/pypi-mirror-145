from setuptools import setup

setup(
    name='cameo_claw',
    version='0.4.0',
    description='multiprocessing download files'
                '2022-04-03 v0.4.0 add parameters'
                '2022-04-03 v0.3.0 independent test'
                '2022-04-02 v0.2.0 multiprocessing, download select to parquet'
                '  . polars select and to parquet'
                '  . 51.8s, ADSL, total 44MB parquets, convert to 1533 .parquet files'
                '  . from 453MB .csv.gz, from 2.6GB .csv'
                '2022-04-02 v0.1.1 default processes 25'
                '2022-04-02 v0.1.0 initial',
    url='https://github.com/bohachu/cameo_claw',
    author='Bowen Chiu',
    author_email='bohachu@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_claw'],
    install_requires=[
        'requests',
        'polars',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
