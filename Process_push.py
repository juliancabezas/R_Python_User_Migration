# Import the necesary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json




# Read the database that we created in step 01
#database_path = "./Processed/pulls_total_closed_merged.csv"
#database_path = "./Processed/pulls_total_opened.csv"
database_path = "./Databases_commits/github_repo_commits_20150901.csv"

#database_path = "./Processed/pulls_total_opened_closed.csv"


pulls_df = pd.read_csv(database_path)


for i in range(0,len(pulls_df.index)):

    print(i)

    payload = json.loads(pulls_df['payload'][i])
    repo = pulls_df['repo_name'][i]

    for j in range(0,len(payload['commits'])):

        print(j)

        email = payload['commits'][j]['author']['email']
        #print(email)

        if j == 0:
            row = [[repo,email]]
            df_commits = pd.DataFrame(row, columns = ['repo_name', 'user'])
        else:
            row = [[repo,email]]
            new_row = pd.DataFrame(row, columns = ['repo_name', 'user'])
            df_commits = df_commits.append(new_row)
    
    if i == 0:
        df_full = df_commits
    else:
        df_full = df_full.append(df_commits)

df_full


# Exploratory analysis


