# 필요 라이브러리 import
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets

# 기본적인 SVM 모델적합
# iris 학습용 데이터 사용

iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target

C = 1                         # SVM의 regularization parameter
clf. svm.SVC(kernel = "linear", C=C)
clf.fit(X,y)

# confusion matrix를 통한 정확도 확인

from sklearn.metrics import confusion_matrix    # confusion_matrix라이브러리
y_pred = clf.predict(X)                         # 학습데이터 분류예측
confusion_matrix(y, y_pred)                     # 정확성검정

# LinearSVM 활용
clf = svm.LinearSVC(C=C, max_iter = 10000)              # 학습 반복횟수 10000
clf.fit(X,y)
y_pred = clf.predict(X)
confusion_matrix(y, y_pred)

# rbf 활용

clf = svm.SVC(kernel = 'rbf', gamma = 0.7, C=C, max_iter = 10000)
#gamma는 sigma^2에 해당하는 scale parameter
#학습 반복횟수 10000

clf.fit(X,y)
y_pred = clf.predict(X)
confusion_matrix(y, y_pred)

# polynomial 활용

clf = svm.SVC(kernel = 'poly', degree = 3, gamma = 'auto', C=C, max_iter = 10000)
#3차항으로 설정, degree = 3
#gamma는 sigma^2에 해당하는 scale parameter
#학습 반복횟수 10000

clf.fit(X,y)
y_pred = clf.predict(X)
confusion_matrix(y, y_pred)


# 함수 정의
def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy


def plot_contours(ax, clf, xx, yy, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out
# 데이터 로드하기
iris = datasets.load_iris()

X = iris.data[:, :2]
y = iris.target
# 모델 정의&피팅
C = 1.0 #regularization parameter
models = (svm.SVC(kernel='linear', C=C),
          svm.LinearSVC(C=C, max_iter=10000),
          svm.SVC(kernel='rbf', gamma=0.7, C=C),
          svm.SVC(kernel='poly', degree=3, gamma='auto', C=C))
models = (clf.fit(X, y) for clf in models)

# plot title 형성
titles = ('SVC with linear kernel',
          'LinearSVC (linear kernel)',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 3) kernel')

# plot 그리기

fig, sub = plt.subplots(2, 2)
plt.subplots_adjust(wspace=0.4, hspace=0.4)

X0, X1 = X[:, 0], X[:, 1]
xx, yy = make_meshgrid(X0, X1)

for clf, title, ax in zip(models, titles, sub.flatten()):
    plot_contours(ax, clf, xx, yy,
                  cmap=plt.cm.coolwarm, alpha=0.8)
    ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xlabel('Sepal length')
    ax.set_ylabel('Sepal width')
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title(title)

plt.show()