__version__ = '0.0.0'
import pandas as pd
import os

from os import environ, listdir, makedirs
from os.path import dirname, expanduser, isdir, join, splitext


def helloworld():
    print('\n\nHello! \n This is quantatrisk_tradetool 0.0.0 python package.\n')


def helloworld2():
    print('hello2')


def LoadSampleCryptoDaily():
    path = os.path.dirname(os.path.realpath(__file__))
    path = '\\'.join(path.split('\\')[:-1])  # -1 step back
    print(path)
    data = pd.read_csv(path + '\data\CryptoSample_daily_timeline' + '.csv', delimiter=',', header=0)
    return data
