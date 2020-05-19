# Import the necesary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# Read the database that we created in step 01
#database_path = "./Processed/pulls_total_closed_merged.csv"
#database_path = "./Processed/pulls_total_opened.csv"
database_path = "./Processed/pulls_total.csv"
#database_path = "./Processed/pulls_total_opened_closed.csv"


pulls_df = pd.read_csv(database_path)

pulls_df


plt.hist(pulls_df['r_py_actions'], bins=30,range=[0, 30])  
plt.ylabel('Frequency')
plt.xlabel('Number of Python or R pull requests in one month')
#plt.show()


# Group by year
pulls_agg_year = pulls_df.groupby(['year','user'])['r_py_actions'].agg(['sum'])
pulls_agg_year


# reset the index to have a nice dataframe
pulls_agg_year = pulls_agg_year.reset_index()


plt.hist(pulls_agg_year['sum'], bins=100,range=[0, 100])
plt.ylabel('Frequency')
plt.xlabel('Number of Python or R pull requests in one year')
#plt.show()


# Base database with all users
pulls_user = pd.DataFrame({'user' : pulls_df.user.unique()})
pulls_user.columns


years = [2015,2016,2017,2018,2019]

# This iteration will stread the database to
for year in years:

    pulls_agg_year_iter = pulls_agg_year[pulls_agg_year.year==year]

    print(pulls_agg_year_iter)

    pulls_agg_year_iter = pulls_agg_year_iter.drop(columns = ['year'])

    column_rename = 'actions_' + str(year)

    pulls_agg_year_iter = pulls_agg_year_iter.rename(columns = {'sum':column_rename})

    if year==2015:
        pulls_5years = pd.merge(pulls_user,
                        pulls_agg_year_iter,
                        left_on = 'user',
                        right_on = 'user',
                        how = 'left')
    else:
        pulls_5years = pd.merge(pulls_5years,
                                pulls_agg_year_iter,
                                left_on = 'user',
                                right_on = 'user',
                                how = 'left')

print(pulls_5years)


# Filter the users with at least 10 pull requests in each year
pulls_5years_filter10 = pulls_5years[(pulls_5years['actions_2015'] > 1) &
                            (pulls_5years['actions_2016'] > 1) &
                            (pulls_5years['actions_2017'] > 1) &
                            (pulls_5years['actions_2018'] > 1) &
                            (pulls_5years['actions_2019'] > 1)]


pulls_5years_filter10['user']




# Exploratory analysis


