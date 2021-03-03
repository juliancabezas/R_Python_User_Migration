# Import the necesary libraries
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

import statsmodels.api as sm


# Read the database that we created in step 02
database_path = "./Processed/push_total_filter30.csv"
push_df = pd.read_csv(database_path)
push_df


# Create new column with the first 3 years
push_df['years_group'] = np.where(push_df['year'].isin([2015,2016,2017]), '2015-2016-2017', '2018-2019') 

push_df

# push_df[push_df['time']==60]

# # Seaborn graphs
# x = push_df['time']
# y = push_df['r_py_index']

# sns.distplot(push_df['r_py_index'], bins = 10,kde=False, rug=False)
# plt.show()

# sns.jointplot(x='time', y='r_py_index', data=push_df)

# sns.jointplot(x='time', y='r_py_index', data=push_df,kind = "kde")

# plt.show()

# sns.jointplot(x='r_actions', y='py_actions', data=push_df)

# sns.jointplot(x='time', y='r_py_index', data=push_df,kind = "kde")

# plt.show()


# Get the linear regressions of each user

# Linear regression of all the data

x = push_df['time']
y = push_df['r_py_index']
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())

print(results.params)
results.pvalues.loc['time']

print()

dir(model)

# Linear regression of single user

# Get a list of all users
users = push_df['user'].unique()
len(users)


# push_df_user = push_df[push_df['user'] == users[3444]] # Example R user
push_df_user = push_df[push_df['user'] == users[3443]] # Example python user

push_df_user

x = push_df_user['time']
y = push_df_user['r_py_index']
x = sm.add_constant(x) # Add constact to consider intercept
model = sm.OLS(y, x)
results = model.fit()

#print(results.summary())
print(results.params['time'])

print(results.pvalues.loc['time'])

dir(model)

# I am going to make a for loop to get the resutls of each regression
len(users)
users_list = []
slopes_list = []
p_values_list = []
means_list_first3years = []
means_list_last2years = []
means_list_full = []
counts_list_first3years = []
counts_list_last2years = []
counts_list_full = []

i =1

for i in range(0,len(users)):

    if i % 100 == 0:
        print(str(round(i/len(users)*100,2)) + "%")

    # Subset of the dataframe
    push_df_user = push_df[push_df['user'] == users[i]]
    # Append the user name
    users_list.append(push_df_user['user'].unique()[0])

    if push_df_user['r_py_index'].nunique() != 1:
        x = push_df_user['time']
        y = push_df_user['r_py_index']
        x = sm.add_constant(x) # Add constact to consider intercept
        model = sm.OLS(y, x)
        results = model.fit()
        slopes_list.append(results.params['time'])
        p_values_list.append(results.pvalues.loc['time'])
    else:
        slopes_list.append(np.nan)
        p_values_list.append(np.nan)


    # Get the mean of the complete series
    means_list_full.append(push_df_user['r_py_index'].mean())  
    counts_list_full.append(len(push_df_user['r_py_index']))

    # Get the mean of the index in the first 3 years
    means = push_df_user[['years_group','r_py_index']].groupby('years_group').mean().reset_index()
    means_list_first3years.append(means[means['years_group'] == '2015-2016-2017']['r_py_index'].values.tolist()[0])

    if len(means[means['years_group'] == '2018-2019']['r_py_index']) != 0:
        means_list_last2years.append(means[means['years_group'] == '2018-2019']['r_py_index'].values.tolist()[0])
    else:
        means_list_last2years.append(0)
    

    # Get the number of data points in the first 3 years
    counts = push_df_user[['years_group','r_py_index']].groupby('years_group').agg('count').reset_index()
    counts_list_first3years.append(counts[counts['years_group'] == '2015-2016-2017']['r_py_index'].values.tolist()[0])

    if len(counts[counts['years_group'] == '2018-2019']['r_py_index']) != 0:
        counts_list_last2years.append(counts[counts['years_group'] == '2018-2019']['r_py_index'].values.tolist()[0])
    else:
        counts_list_last2years.append(0)


users_list
slopes_list
p_values_list

def mean(lst): 
    return sum(lst) / len(lst) 

len(users_list)
len(slopes_list)
len(p_values_list)
len(means_list_first3years)
len(means_list_last2years)
len(means_list_full)
len(counts_list_first3years)
len(counts_list_last2years)
len(counts_list_full)

# Create Dictionary of lists
dic_lists = {'user': users_list,'slope':slopes_list,'p_value':p_values_list,'mean_2015_2017': means_list_first3years,
            'count_2015_2017':counts_list_first3years,'mean_2018_2019':means_list_last2years,'count_2018_2019':counts_list_last2years,
            'mean':means_list_full,'count':counts_list_full}

results_index = pd.DataFrame(dic_lists)

# Write to csv
results_index.to_csv("./Results/Results_index_filter30_v3.csv",index=False)

results_index[results_index['p_value'] <= 0.05]
results_index[(results_index['p_value'] <= 0.05) & (results_index['slope'] < 0)]

# Complete adoption of python
push_df_user = push_df[push_df['user'] == 'chrisluedtke']
push_df_user
x = push_df_user['time']
y = push_df_user['r_py_index']
x = sm.add_constant(x) # Add constact to consider intercept
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())




push_df_user

p_values_list[4]
users_list[4]
push_df_user = push_df[push_df['user'] == users[4]]
push_df_user

results.summary

results.params

results.pvalues.loc['time']


results.pvalues

x
y
results.predict()








# The model seems to be wrong
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
y = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.99]
x = sm.add_constant(x) # Add constact to consider intercept
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())






















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


