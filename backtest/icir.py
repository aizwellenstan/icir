import os;from pathlib import Path
rootPath = Path(os.path.dirname(__file__)).parent
import sys;sys.path.append(os.path.relpath(rootPath, os.path.dirname(__file__)))
import numpy as np
import pandas as pd
from modules.icir import GetICIR, DumpICIRData
from datetime import datetime

def getCodeList():
    import os
    directory = f'{rootPath}/data/navs'
    files = os.listdir(directory)
    file_names_without_extension = [os.path.splitext(file)[0] for file in files]
    print(file_names_without_extension)
    return file_names_without_extension

def is_float(var):
    return isinstance(var, float)

def main(update=False):
    todayStr = datetime.today().strftime('%Y-%m-%d')
    cachePath = f"{rootPath}/cache/{todayStr}.parquet"
    if update:
        dataDict = {}
        for symbol in getCodeList():
            chart = pd.read_parquet(f'{rootPath}/data/navs/{symbol}.parquet').to_numpy()
            if len(chart) < 1: continue
            dataDict[symbol] = chart

        factorList = []
        for symbol, npArr in dataDict.items():
            for i in range(1, len(npArr)):
                if not is_float(npArr[i-1][57]): continue
                factorList.append([datetime.strptime(npArr[i][1], '%Y-%m-%d %H:%M:%S'),symbol,npArr[i][4],npArr[i-1][57]])

        df = pd.DataFrame(factorList, columns=['date','symbol', 'close', 'factor'])
        df.to_csv('factor.csv')
        df.to_parquet(cachePath)
    else:
        factorList = pd.read_parquet(cachePath).values.tolist()

    quantiles = 10
    periods = [1, 5, 10, 20]
    factor_bins_returns, ic_summary = GetICIR(factorList, quantiles=quantiles, periods=periods)

    """
    quantiles 1.0 must < 0
    quantiles 2.o must > 0
    """
    # print(factor_bins_returns, ic_summary)

    folder = f'{rootPath}/results'
    DumpICIRData(factor_bins_returns, ic_summary, 
        f"{folder}/1_diff_{quantiles}_icir_rtn.json", 
        f"{folder}/1_diff_{quantiles}_icir_stats.json")

if __name__ == '__main__':
    main(True)
    # main(False)