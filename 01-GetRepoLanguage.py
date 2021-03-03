# Import the necesary libraries
import numpy as np
import pandas as pd

years = ["2015","2016","2017","2018","2019"]

months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

time = 0

for year in years:
    for month in months:

        # Go one time step further
        time = time + 1

        #print(time)

        # Assing year and month
        print(year)
        print(month)

        # Define the math of the csv file and read it
        database_path = "./Databases/pulls_month/github_user_pull_count_{year}{month}.csv".format(year = year,month = month)
        pulls_df = pd.read_csv(database_path)

        #pulls_df

        pulls_df_unfiltered = pulls_df
        pulls_df_unfiltered = pulls_df_unfiltered.drop(columns = ['user','action','merged','number_actions'])

        ## Filter the Users with activities in R of Python
        pulls_df = pulls_df[pulls_df.language.isin(['"R"','"Python"'])]

        # Drop unused columns
        pulls_df = pulls_df.drop(columns = ['user','action','merged','number_actions'])

        ## I will make a dataframe with the unique values
        pulls_df = pulls_df.drop_duplicates()

        if time == 1:
            pulls_total = pulls_df
        else:
            pulls_total = pulls_total.append(pulls_df)
            pulls_total = pulls_total.drop_duplicates()

        if time == 1:
            pulls_total_unfiltered = pulls_df_unfiltered
        else:
            pulls_total_unfiltered = pulls_total_unfiltered.append(pulls_df_unfiltered)
            pulls_total_unfiltered = pulls_total_unfiltered.drop_duplicates()


print(pulls_total)

pulls_total = pulls_total.drop_duplicates(subset=['repo_name'], keep=False)

pulls_total.to_csv("./Processed/repos_R_Python.csv",index=False)



print(pulls_total_unfiltered)
pulls_total_unfiltered.to_csv("./Processed/repos_total.csv",index=False)








#pulls_df = pd.read_csv(database_path)


