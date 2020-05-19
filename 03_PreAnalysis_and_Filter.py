# Import the necesary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# Read the database that we created in step 02
database_path = "./Processed/push_total.csv"
push_df = pd.read_csv(database_path)

push_df[push_df['user']=='firm1']


plt.hist(push_df['r_py_actions'], bins=30,range=[0, 500])  
plt.ylabel('Frequency')
plt.xlabel('Number of Python or R push actions in one month')
#plt.show()

# See users with more than 5000 push actions
push_df[push_df['r_py_actions']> 5000]


# Group by year
pushs_agg_year = push_df.groupby(['year','user'])['r_py_actions'].agg(['sum'])
pushs_agg_year


# reset the index to have a nice dataframe
pushs_agg_year = pushs_agg_year.reset_index()


plt.hist(pushs_agg_year['sum'], bins=100,range=[0, 1000])
plt.ylabel('Frequency')
plt.xlabel('Number of Python or R push actions in one year')
#plt.show()


# Base database with all users
pushs_user = pd.DataFrame({'user' : push_df.user.unique()})
pushs_user

years = [2015,2016,2017,2018,2019]
months = [1,2,3,4,5,6,7,8,9,10,11,12]

# This iteration will spread the database to get a column for each data
for year in years:
    for month in months:

        print(year)
        print(month)
        
        pushs_agg_year_iter = push_df[(push_df['year'] == year) & (push_df['month'] == month)]

        pushs_agg_year_iter = pushs_agg_year_iter.drop(columns = ['r_actions','py_actions','time','r_py_index','year','month'])

        #pushs_agg_year_iter

        column_rename = 'actions_' + str(year) + "_" + str(month)

        pushs_agg_year_iter = pushs_agg_year_iter.rename(columns = {'r_py_actions':column_rename})

        if (year==2015) & (month == 1):
            pushs_5years = pd.merge(pushs_user,
                            pushs_agg_year_iter,
                            left_on = 'user',
                            right_on = 'user',
                            how = 'left')
        else:
            pushs_5years = pd.merge(pushs_5years,
                                    pushs_agg_year_iter,
                                    left_on = 'user',
                                    right_on = 'user',
                                    how = 'left')

print(pushs_5years)

# Count the numbers of NA i n a row and substract it by 60 (total of months)
pushs_5years['months_activity'] = 60 - pushs_5years.isnull().sum(axis=1)


# Filter the users with at least 12 months of activity
pushs_5years_filter12 = pushs_5years[pushs_5years['months_activity']>=12]

pushs_5years_filter12

users_filter12 = pushs_5years_filter12['user'].unique()

users_filter12

# Filter the users with at least 24 months of activity
pushs_5years_filter24 = pushs_5years[pushs_5years['months_activity']>=24]

pushs_5years_filter24

users_filter24 = pushs_5years_filter24['user'].unique()

users_filter24

# Filter the users with at least 30 months of activity
pushs_5years_filter30 = pushs_5years[pushs_5years['months_activity']>=30]

pushs_5years_filter30

users_filter30 = pushs_5years_filter30['user'].unique()

users_filter30

# Filter the users with at least 48 months of activity
pushs_5years_filter48 = pushs_5years[pushs_5years['months_activity']>=48]

pushs_5years_filter48

users_filter48 = pushs_5years_filter48['user'].unique()

users_filter48

# Filter the main database using the selected users
push_df_filter12 = push_df[push_df['user'].isin(users_filter12)]
push_df_filter24 = push_df[push_df['user'].isin(users_filter24)]
push_df_filter30 = push_df[push_df['user'].isin(users_filter30)]
push_df_filter48 = push_df[push_df['user'].isin(users_filter48)]



#Write them to csv
push_df_filter12.to_csv("./Processed/push_total_filter12.csv",index=False)
push_df_filter24.to_csv("./Processed/push_total_filter24.csv",index=False)
push_df_filter30.to_csv("./Processed/push_total_filter30.csv",index=False)
push_df_filter48.to_csv("./Processed/push_total_filter48.csv",index=False)

push_df_filter24

plt.hist(push_df_filter24['r_py_index'], bins=10)  
plt.ylabel('Frequency')
plt.xlabel('R-Python index')
plt.show()


plt.scatter(push_df_filter24['time'], push_df_filter24['r_py_index'])
plt.show()




# Exploratory analysis


