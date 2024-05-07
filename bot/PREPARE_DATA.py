import os;from pathlib import Path
rootPath = Path(os.path.dirname(__file__)).parent
import sys;sys.path.append(os.path.relpath(rootPath, os.path.dirname(__file__)))
import pandas as pd

df = pd.read_csv(f'{rootPath}/data/nav.csv')
strategies = df['code'].unique()
print(strategies)
for strategy in strategies:
    navs = df[df['code'] == strategy]
    navs.to_parquet(f'{rootPath}/data/navs/{strategy}.parquet')