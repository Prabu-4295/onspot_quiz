# -*- coding: utf-8 -*-
"""On_spot_lab1_4295_prabu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vfwCwE5johGYsG-yaQ3EKVu-6BbYF_aj
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


data = pd.read_csv('/content/drive/MyDrive/DSAI-LVA-DATASET for Quiz.csv')


label_encoder = LabelEncoder()
data['ParentEducation'] = label_encoder.fit_transform(data['ParentEducation'])
data['Pass'] = label_encoder.fit_transform(data['Pass'])

X = data.drop('Pass', axis=1)
y = data['Pass']

scaler = StandardScaler()
X[['StudyTime', 'PreviousTestScore']] = scaler.fit_transform(X[['StudyTime', 'PreviousTestScore']])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


X_train.to_csv('/content/train_data.csv', index=False)
X_test.to_csv('/content/test_data.csv', index=False)


def determine_performance(probabilities):
    if probabilities[0] >= 0.5:
        return 'Fail'
    elif probabilities[1] >= 0.5:
        return 'Pass with Low Grade'
    else:
        return 'Pass with High Grade'


clf_dt = DecisionTreeClassifier()
clf_dt.fit(X_train, y_train)
y_pred_prob_dt = clf_dt.predict_proba(X)


clf_rf = RandomForestClassifier()
clf_rf.fit(X_train, y_train)
y_pred_prob_rf = clf_rf.predict_proba(X)

clf_xgb = XGBClassifier()
clf_xgb.fit(X_train, y_train)
y_pred_prob_xgb = clf_xgb.predict_proba(X)


performance_categories_dt = [determine_performance(probs) for probs in y_pred_prob_dt]
performance_categories_rf = [determine_performance(probs) for probs in y_pred_prob_rf]
performance_categories_xgb = [determine_performance(probs) for probs in y_pred_prob_xgb]


data['DT_Performance'] = performance_categories_dt
data['RF_Performance'] = performance_categories_rf
data['XGB_Performance'] = performance_categories_xgb


data.to_csv('/content/Performance.csv', index=False)