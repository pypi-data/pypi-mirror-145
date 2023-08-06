from setuptools import setup
import pathlib
from datetime import datetime as dt


def gen_version() -> str:
    return dt.now().strftime('%Y.%#m.%#d.%#H.%#M.%#S.%f')


setup(
    name='TelethonFakeTLS',
    packages=['TelethonFakeTLS'],
    version=gen_version(),
    license='MIT',
    description='MTProxy FakeTLS Support For Telethon !',
    long_description=pathlib.Path('README.rst').read_text(encoding='UTF-8'),
    author='Ro0tz5',
    author_email='Ro0tz5c@Gmail.Com',
    url='https://github.com/Ro0tz5/telethon-faketls',
    download_url='https://github.com/Ro0tz5/telethon-faketls/archive/refs/heads/master.zip',
    keywords=['Telethon', 'FakeTLS', 'MTProxy', 'EE'],
    install_requires=[
        'Telethon',
        'cryptography',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    package_data={'TelethonFakeTLS': ['*']}
)
