print(__doc__)

# Author: LiuBin
# License: BSD Style.

import numpy as np
import pandas as pd

np.random.seed(0)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import f1_score,roc_curve,accuracy_score
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

X, y = datasets.make_classification(n_samples=10000, 
                                    n_features=20,
                                    n_informative=5, 
                                    n_redundant=2,
                                    n_classes=5)

train_samples=800;
X_train = X[:train_samples]
X_test = X[train_samples:]
y_train = y[:train_samples]
y_test = y[train_samples:]


