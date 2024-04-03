# -*- coding: utf-8 -*-
"""Predictive Model Quiz1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zcn9mBllCSU_PK_ftBP2f39WP8lHIvl_
"""

import pandas as pd
import numpy as np
import random
data=pd.read_csv('/content/DSAI-LVA-DATASET for Quiz.csv')
data

education=['Masters','Bachelors','High School','School','No Education']
for index in data.index:
  data.loc[index,'ParentEducation']=random.choice(education)
data

from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder,StandardScaler
data['ParentEducationLabels']=LE.fit_transform(data['ParentEducation'])
passed=data[data['Pass']=='Yes']
LE=LabelEncoder()
SC=StandardScaler()
passed['StudyTime_Norm']=SC.fit_transform(passed[['StudyTime']])
passed['PreviousTestScore_Norm']=SC.fit_transform(passed[['PreviousTestScore']])
passed

KM=KMeans(n_clusters=2)
KM.fit_predict(passed[['StudyTime','PreviousTestScore','ParentEducationLabels']])
passed['cluster']=KM.labels_
passed

data['cluster']=[2]*len(data.index)
new_data=pd.concat([data[data['Pass']=='No'],passed],axis=0,ignore_index=True)
new_data
data.drop('cluster',axis=1,inplace=True)
new_data.drop(['StudyTime_Norm','PreviousTestScore_Norm'],axis=1,inplace=True)
new_data.info()

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

var_model=[]
var_model.append(['XGBoost',XGBClassifier()])
var_model.append(['Random Forest',RandomForestClassifier()])
var_model.append(['Decision Tree',DecisionTreeClassifier()])
X=new_data.drop('cluster',axis=1)
y=new_data['cluster']
xtrain,xtest,ytrain,ytest=train_test_split(X,y,test_size=0.3,random_state=42)
xtrain.join(ytrain).to_csv('/content/train.csv')
xtest.join(ytest).to_csv('/content/test.csv')

from sklearn.metrics import accuracy_score,classification_report
train_data=pd.read_csv('/content/train.csv')
test_data=pd.read_csv('/content/test.csv')
for name, model in var_model:
    model.fit(train_data[['StudyTime','PreviousTestScore','ParentEducationLabels']], train_data['cluster'])
    y_pred = model.predict(test_data[['StudyTime','PreviousTestScore','ParentEducationLabels']])
    vAR_model_predictions = [round(value) for value in y_pred]
##
## The accuracy and runtime of all the models should be compared
##
    accuracy = accuracy_score(test_data.iloc[:,-1],vAR_model_predictions)
    print("Model Prediction Accuracy: %.2f%%" % (accuracy * 100.0),name)
    print("Model Report:\n")
    print(classification_report(test_data.iloc[:,-1],vAR_model_predictions))
    print("\n")