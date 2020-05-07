import os

import pandas as pd

# for root, dirs, files in os.walk("../data/"):
#     for filename in files:
#         os.rename('../data/' + filename, '../data/' + filename.split()[-1])

data = []

for root, dirs, files in os.walk("../data/"):
    for file in files:
        data.append(file.replace('.csv', ''))

stocks = pd.DataFrame(data=data)
stocks.columns = ['stock']
stocks.to_csv('../stock.csv', header=True)
