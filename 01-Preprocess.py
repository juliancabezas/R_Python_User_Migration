# Import the necesarry libraries
import numpy as np
import pandas as pd

years = ["2015","2016","2017","2018","2019"]

months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

year = years[0]
month = months[0]

print(year)
print(month)

database_path = "./Databases/pulls_month/github_user_pull_count_{year}{month}.csv".format(year = year,month = month)

pulls_df = pd.read_csv(database_path)

pulls_df = pulls.df[(pulls_df.merged==True) & (pulls_df.merged==True)]

print(pulls_df.user)




pulls_df = pd.read_csv(database_path)


