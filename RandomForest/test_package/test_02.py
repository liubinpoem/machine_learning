#coding=utf-8

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyt
from sklearn import metrics

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)

#用numpy生成(0,1)之间的随机数,<=0.75的作为训练样本
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

#形成一个category类型
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
#print df['species']

#返回最前面的n行df.head(n)
#df.head()

#将训练数据和测试数据分开
train, test = df[df['is_train']==True], df[df['is_train']==False]

#得到列名称,也是分类特征
features = df.columns[:4]

#定义随机森林模型
clf = RandomForestClassifier(n_jobs=2)

#将species这个列的数据转换成数字枚举类型,返回结果为y
y, _ = pd.factorize(train['species'])
#print y

#训练模型,训练数据,训练分类
#print train[features]
clf.fit(train[features], y)

#进行预测
result=clf.predict(test[features])
test_y,_=pd.factorize(test['species'])
print pd.factorize(test['species'])

#计算预测准确率
print metrics.accuracy_score(test_y,result)

preds = iris.target_names[clf.predict(test[features])]

#行列交叉验证预测结果,对于多分类(非2分类)的预测问题,可采用这样的方式
print pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])

