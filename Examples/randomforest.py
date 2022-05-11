import pandas as pd
# import numpy as np
# from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report
# from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

dataset=pd.read_csv('mushrooms.csv')
dataset


#독버섯 유무 class를 Y값으로 두고 그것에 영향을 끼치는 요인 X를 본다

x=dataset.drop('class',axis=1) #타겟 제거
y=dataset['class']

#문자를 숫자로

x= pd.get_dummies(x, columns=x.columns)
x.head()





X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)


sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)


model=RandomForestClassifier(n_estimators=50, criterion='entropy',random_state=42)
model.fit(X_train, y_train)


RandomForestClassifier(criterion='entropy',n_estimators=50,random_state=42)


x=dataset.drop('class',axis=1) #타겟을 제거
n_dataset=dataset.shape[1] #데이터 갯수

# plt.barh(range(n_dataset-1),model.feature_importances_,align='center')
# plt.yticks(np.arange(n_dataset-1),x.columns)
# plt.ylim(-1,n_dataset)
# plt.show()

#정확도
pred=model.predict(X_test)
score=accuracy_score(y_test,pred)
score

print('정답률:',score)
print('리포트:',classification_report(y_test, pred))