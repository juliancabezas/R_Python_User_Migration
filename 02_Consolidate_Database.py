# Import the necesary libraries
import numpy as np
import pandas as pd


# Load the repositories database
repos_r_py = pd.read_csv("./Processed/repos_R_Python.csv")

repos_r_py

repos_r_py['language'].unique()

len(repos_r_py['repo_name'].unique())

# Create arrays of years and months in out database
years = ["2015","2016","2017","2018","2019"]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

time = 0

year = '2015'
month = '01'

for year in years:
    for month in months:

        # Go one time step further
        time = time + 1

        #print(time)

        print(year)
        print(month)

        # Define the math of the csv file and read it
        database_path = "./Databases_push/github_user_push_{year}{month}.csv".format(year = year,month = month)
        push_df = pd.read_csv(database_path)

        push_df = pd.merge(push_df,
                        repos_r_py,
                        left_on = 'repo_name',
                        right_on = 'repo_name',
                        how = 'left')

        # Filter to get the merged pull requests

        ## Filter the Users with activities in R of Python
        push_df = push_df[push_df.language.isin(['"R"','"Python"'])]

        # Drop unused columns
        push_df = push_df.drop(columns = ['repo_name'])

        ## I will make a dataframe with the unique values of the users
        push_user = pd.DataFrame({'user' : push_df.user.unique()})

        ## push in the R language
        push_df_r = push_df[push_df.language == '"R"']

        # Group the actions in hte different R repos
        push_df_r = push_df_r.groupby(['user'])['number_actions'].agg(['sum']).reset_index()

        # Rename the column of actions to represent the R actions
        push_df_r = push_df_r.rename(columns = {'sum':'r_actions'})

        ## push in the Python language
        push_df_py = push_df[push_df.language == '"Python"']

        # Group the actions in hte different Python repos
        push_df_py = push_df_py.groupby(['user'])['number_actions'].agg(['sum']).reset_index()

        # Rename the column of actgions to represent the R actions
        push_df_py = push_df_py.rename(columns = {'sum':'py_actions'})

        # Merge the dataframes together
        push_merged = pd.merge(push_user,
                                push_df_r,
                                left_on = 'user',
                                right_on = 'user',
                                how = 'left')

        push_merged = pd.merge(push_merged,
                                push_df_py,
                                left_on = 'user',
                                right_on = 'user',
                                how = 'left')

        ## If the r actions or python action colums are NaN put a zero 
        push_merged['r_actions'] = np.where(np.isnan(push_merged['r_actions']), 0, push_merged['r_actions'])
        push_merged['py_actions'] = np.where(np.isnan(push_merged['py_actions']), 0, push_merged['py_actions'])

        push_merged['year'] = year
        push_merged['month'] = month
        push_merged['time'] = time

        if time == 1:
            push_total = push_merged
        else:
            push_total = push_total.append(push_merged)
        
        print("Ready!")


push_total['r_py_actions'] = push_total['r_actions'] + push_total['py_actions']

push_total['r_py_index'] = push_total['r_actions'] / (push_total['py_actions'] + push_total['r_actions'])

print(push_total)

push_total[push_total['user']=='firm1']

#push_total.to_csv("./Processed/push_total_closed_merged.csv",index=False)

#push_total.to_csv("./Processed/push_total_opened.csv",index=False)

push_total.to_csv("./Processed/push_total.csv",index=False)

