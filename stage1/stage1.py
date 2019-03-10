import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from feature_extraction import extract_features, get_feature_names
from text_processing import get_instances

TRAIN_DOCS_DIR = './documents/set_I'
TEST_DOCS_DIR = './documents/set_J'

instances = []
for i in range(200):
    text_file = os.path.join(TRAIN_DOCS_DIR, f'{i}.txt')

    if not os.path.isfile(text_file):
        continue

    with open(text_file) as f:
        text = f.read()

    instances += get_instances(text, i)

feature_names = get_feature_names()

with Pool() as p:
    features = p.map(extract_features, instances)

data = pd.DataFrame(features, columns=feature_names)

numeric_features = data.dtypes[data.dtypes == int].keys().values.tolist()
boolean_features = data.dtypes[data.dtypes == bool].keys().values.tolist()[:-1]
categorical_features = data.dtypes[data.dtypes == object].keys().values.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', StandardScaler(), numeric_features)],
    remainder='passthrough')

D_train = preprocessor.fit_transform(data)

X_train = D_train[:, :-1].toarray()
y_train = D_train[:, -1].astype(int).toarray().flatten()

classifiers = [DecisionTreeClassifier(random_state=0),
               RandomForestClassifier(random_state=0),
               SVC(kernel="linear", random_state=0),
               RidgeClassifier(random_state=0),
               LogisticRegression(solver='lbfgs', tol=1e-3, max_iter=400, random_state=0),
               SGDClassifier(loss="log", random_state=0),
               MLPClassifier(early_stopping=True, random_state=0),
               AdaBoostClassifier(random_state=0),
               KNeighborsClassifier(3)]

cv_scores = pd.DataFrame(columns=['Classifier', 'Precision', 'Recall', 'F1'])
for i, clf in enumerate(classifiers):
    s = cross_validate(clf, X_train, y_train, scoring=['recall', 'precision', 'f1'], cv=3, return_train_score=False)
    cv_scores.loc[i] = [clf.__class__.__name__,
                        s['test_precision'].mean(),
                        s['test_recall'].mean(),
                        s['test_f1'].mean()]

clf = MLPClassifier(early_stopping=True, random_state=0)
clf.fit(X_train, y_train)

instances_ = []

for i in range(200, 300):
    text_file = os.path.join(TEST_DOCS_DIR, f'{i}.txt')

    if not os.path.isfile(text_file):
        continue

    with open(text_file) as f:
        text = f.read()

    instances_ += get_instances(text, i)

with Pool() as p:
    features_ = p.map(extract_features, instances_)

data_ = pd.DataFrame(features_, columns=feature_names)

D_test = preprocessor.transform(data_)

X_test = D_test[:, :-1].toarray()
y_test = D_test[:, -1].astype(int).toarray().flatten()

y_test_predicted = clf.predict(X_test)

print(f'precision: {precision_score(y_test, y_test_predicted)}')
print(f'recall: {recall_score(y_test, y_test_predicted)}')
print(f'f1: {f1_score(y_test, y_test_predicted)}')
