import os;from pathlib import Path
rootPath = Path(os.path.dirname(__file__)).parent
import sys;sys.path.append(os.path.relpath(rootPath, os.path.dirname(__file__)))
import pandas as pd

def colReader():
    df = pd.read_csv(f'{rootPath}/data/nav.csv')
    c = 0
    for col in df.columns:
        print(c, col)
        c += 1

colReader()