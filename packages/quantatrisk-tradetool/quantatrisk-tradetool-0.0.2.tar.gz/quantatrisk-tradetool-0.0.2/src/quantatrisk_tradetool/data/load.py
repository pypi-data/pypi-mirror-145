
import pandas as pd
import os


def LoadSampleCryptoDaily():

    path = os.path.dirname(os.path.realpath(__file__))
    path = '\\'.join(path.split('\\')[:-2])  # -1 step back
    print(path)
    data = pd.read_csv(path + '\data\CryptoSample_daily_timeline' + '.csv', delimiter=',', header=0)
    return data
