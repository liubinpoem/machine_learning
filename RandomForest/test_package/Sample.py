# -*- coding:utf-8 -*-

# 作者: Gael Varoquaux <gael dot varoquaux at normalesup dot org>
# 协议: BSD 3 clause

# Python标准科学计算包导入
import matplotlib.pyplot as plt

# 导入数据集,分类器和评估度量
from sklearn import datasets,svm, metrics

# 数字数据集
digits = datasets.load_digits()
#数据是一个8x8的数字图像,让我们先看看开头的三张图像.图像存储在数据集
#的`images`属性中,如果我们要加载图像文件的话,可以使用pylab.imread.
#注意每一张图像尺寸必须相等.这些图像各自对应的数字是多少我们是知道的
#他们存储在数据集的target属性中.

images_and_labels = list(zip(digits.images, digits.target))

for index, (image, label) in enumerate(images_and_labels[:4]):
    plt.subplot(2, 4, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Training: %i' % label)

# 在数据上应用一个分类器, 我们需要铺平图像,将数据转换成二位矩阵:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# 创建一个分类器: 一个支持向量分类器
classifier = svm.SVC(gamma=0.001)

# 我们在前半部分数据上进行学习
classifier.fit(data[:n_samples / 2], digits.target[:n_samples / 2])

# 现在预测后半部分的值:
expected = digits.target[n_samples / 2:]
predicted = classifier.predict(data[n_samples / 2:])
print("Classification report for classifier %s:\n%s\n"
      %(classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
images_and_predictions = list(zip(digits.images[n_samples / 2:], predicted))
for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    plt.subplot(2, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)
    plt.show()