import os
import pandas as pd

# locMst=pd.read_csv('../data/location_mst.csv',encoding='ms949')

for year in range(2015, 2018):
    for month in range(1, 13):
        # for code, name in zip(locMst.CODE, locMst.NAME):
        target_directory = '../data/Y' + str(year) \
                           + '/M' + str(month).zfill(2)

        if not os.path.isdir(target_directory):
            os.makedirs(target_directory)

