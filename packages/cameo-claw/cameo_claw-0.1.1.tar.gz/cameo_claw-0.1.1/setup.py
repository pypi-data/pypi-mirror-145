from setuptools import setup

setup(
    name='cameo_claw',
    version='0.1.1',
    description='multiprocessing download files'
                '2022-04-02 v0.1.1 default processes 25'
                '2022-04-02 v0.1.0 initial',
    url='https://github.com/bohachu/cameo_claw',
    author='Bowen Chiu',
    author_email='bohachu@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_claw'],
    install_requires=[
        'fastapi',
        'psutil'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
