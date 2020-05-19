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
x
model = sm.OLS(y, x)
results = model.fit()

#print(results.summary())
print(results.params['time'])

print(results.pvalues.loc['time'])

dir(model)

# I am going to make a for loop to get the resutls of each regression

users_list = []
slopes_list = []
p_values_list = []

i = 0

for i in range(0,len(users)):

    # Subset of the dataframe
    push_df_user = push_df[push_df['user'] == users[i]]

    users_list[i] = push_df_user['user']
    slopes_list[i] = results.params['time']
    p_values_list[i] = results.pvalues.loc['time']
























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


