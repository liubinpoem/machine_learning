#coding=utf-8

import pandas as pd
import matplotlib.pyplot as pyt
import numpy as np

#pandas and numpy is suitable for processing batch numbers and make some steps easy to be realized
#no need to set all procedures into numpy and pandas
#read data files in
movies=pd.read_csv('data/movies.csv')
ratings=pd.read_csv('data/ratings.csv')

#construct rating matrix
matrix=ratings.iloc[:,0:3]
print matrix