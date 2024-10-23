import pandas as pd


def df_info(df, include=False, samples=1):
    """
    Function takes a dataframe and returns potentially relevant information about it (including a sample)
    include=bool, default to False. To add the results from a describe method, pass True to the argument.
    samples=int, default to 1. Shows 1 sample by default, but can be modified to include more samples if desired.
    """
    # create the df_inf dataframe
    df_inf = pd.DataFrame(index=df.columns,
                          data={
                              'nunique': df.nunique(), 'dtypes': df.dtypes, 'isnull': df.isnull().sum()
                          })
    # append samples based on input
    if samples >= 1:
        df_inf = df_inf.merge(df.sample(
            samples).iloc[0:samples].T, how='left', left_index=True, right_index=True)
        # append describe results if option selected
    if include == True:
        return df_inf.merge(df.describe(include='all').T, how='left', left_index=True, right_index=True)
    elif include == False:
        return df_inf
    else:
        print('Value passed to "include" argument is invalid.')


def print_libs():
    """
    Function that prints all libraries used up to present. Takes no arguments and returns none.
    """
    libraries = [
        'import itertools -> iterations',
        'import time -> time and date work',
        'from tqdm import tqdm -> progress bars on for loops'
        'import pandas as pd -> large scale database work',
        'import numpy as np -> advanced numerical work',
        'import matplotlib.pyplot as plt -> plotting work',
        'import seaborn as sns -> advanced and intuitive plotting',
        'from scipy import stats -> statistical work',
        'from pydataset import data -> list of datasets',
        'import os -> operating system work',
        'import warnings -> getting rid of pesky warnings',
        'from sklearn import metrics -> model metrics',
        'from sklearn.impute import SimpleImputer -> dynamic value filling',
        'from sklearn.model_selection import train_test_split -> splitting datasets',
        'from sklearn.tree import DecisionTreeClassifier, plot_tree -> DT modeling',
        'from sklearn.neighbors import KNeighborsClassifier -> KNN modeling',
        'from sklearn.ensemble import RandomForestClassifier -> RF modeling',
        'from sklearn.linear_model import LogisticRegression -> LR modeling',
        'from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler -> scaling work'
    ]
    for library in libraries:
        print(library)


def check_file_exists(filename, query, url):
    """
    Function takes a filename, query, and url and checks if the file exists. It will load the dataset requested from either SQL or from the local file.
    """
    if os.path.exists(filename):
        print('Reading from file...')
        df = pd.read_csv(filename, index_col=0)
    else:
        print('Reading from database...')
        df = pd.read_sql(query, url)
        df.to_csv(filename)
        return df
