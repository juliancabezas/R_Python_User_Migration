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
        #year = 2017
        #month = 10

        print(year)
        print(month)

        # Define the math of the csv file and read it
        database_path = "./Databases/pulls_month/github_user_pull_count_{year}{month}.csv".format(year = year,month = month)
        pulls_df = pd.read_csv(database_path)


        # Filter to get the merged pull requests
        #pulls_df = pulls_df[(pulls_df.merged==True) & (pulls_df.action=='"closed"')]
        #pulls_df = pulls_df[(pulls_df.action =='"opened"')]
        #pulls_df = pulls_df[(pulls_df.action =='"opened"') | ((pulls_df.merged==True) & (pulls_df.action=='"closed"'))]

        ## Filter the Users with activities in R of Python
        pulls_df = pulls_df[pulls_df.language.isin(['"R"','"Python"'])]
        # Drop unused columns
        pulls_df = pulls_df.drop(columns = ['repo_name','action','merged'])

        ## I will make a dataframe with the unique values of the users
        pulls_user = pd.DataFrame({'user' : pulls_df.user.unique()})

        ## Pulls in the R language
        pulls_df_r = pulls_df[pulls_df.language == '"R"']

        # Rename the column of actions to represent the R actions
        pulls_df_r = pulls_df_r.rename(columns = {'number_actions':'r_actions'})

        # Drop unused column
        pulls_df_r = pulls_df_r.drop(columns = ['language'])

        ## Pulls in the Python language
        pulls_df_py = pulls_df[pulls_df.language == '"Python"']

        # Rename the column of actgions to represent the R actions
        pulls_df_py = pulls_df_py.rename(columns = {'number_actions':'py_actions'})

        # Drop unused column
        pulls_df_py = pulls_df_py.drop(columns = ['language'])

        # Merge the dataframes together
        pulls_merged = pd.merge(pulls_user,
                                pulls_df_r,
                                left_on = 'user',
                                right_on = 'user',
                                how = 'left')

        pulls_merged = pd.merge(pulls_merged,
                                pulls_df_py,
                                left_on = 'user',
                                right_on = 'user',
                                how = 'left')

        ## If the r actions or python action colums are NaN put a zero 
        pulls_merged['r_actions'] = np.where(np.isnan(pulls_merged['r_actions']), 0, pulls_merged['r_actions'])
        pulls_merged['py_actions'] = np.where(np.isnan(pulls_merged['py_actions']), 0, pulls_merged['py_actions'])

        pulls_merged['year'] = year
        pulls_merged['month'] = month
        pulls_merged['time'] = time

        if time == 1:
            pulls_total = pulls_merged
        else:
            pulls_total = pulls_total.append(pulls_merged)


#print(pulls_total)

pulls_total['r_py_actions'] = pulls_total['r_actions'] + pulls_total['py_actions']

#pulls_total.to_csv("./Processed/pulls_total_closed_merged.csv",index=False)

#pulls_total.to_csv("./Processed/pulls_total_opened.csv",index=False)

pulls_total.to_csv("./Processed/pulls_total.csv",index=False)








#pulls_df = pd.read_csv(database_path)


