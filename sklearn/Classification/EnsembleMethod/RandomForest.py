print(__doc__)

# Author: LiuBin
# License: BSD Style.

import numpy as np
import pandas as pd

np.random.seed(0)
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score,accuracy_score

X, y = datasets.make_classification(n_samples=10000, n_features=20,n_informative=2, n_redundant=2)

train_samples=8000;
X_train = X[:train_samples]
X_test = X[train_samples:]
y_train = y[:train_samples]
y_test = y[train_samples:]

#print X_train.shape[0],X_train.shape[1]
esitmator_acc=pd.DataFrame(np.random.randn(30,5))

#grid search of parameters
for n in range(20,50):
    for m in range(5,20):
        rfc=RandomForestClassifier(n_estimators=n,max_depth=m,bootstrap=True)
        rfc.fit(X_train,y_train)
        pred=rfc.predict(X_test)
        result=accuracy_score(y_true=y_test,y_pred=pred)
        print "n_estimators:",n,"max_depth:",m," accuracy:",result
        esitmator_acc[n,m]=result

print esitmator_acc

figure=plt.figure()
ax=figure.gca(projection='3d')

estimator=np.linspace(20,50,30)
max_depth=np.linspace(5,20,15)
ax.scatter(esitmator_acc)

plt.show()


