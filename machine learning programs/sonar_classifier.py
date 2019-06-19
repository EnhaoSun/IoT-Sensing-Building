import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.externals import joblib

############################################################################
input_file_train = 'sonar_train.csv'
train_df = pd.read_csv(input_file_train, header=0)
y_train = train_df['activity'].as_matrix()

# remove the non-numeric columns
train_df = train_df._get_numeric_data()

# put the numeric column names in a python list
train_numeric_headers = list(train_df.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
train_numeric_array = train_df.as_matrix()

x_train = train_numeric_array
############################################################################
input_file_test = 'sonar_test.csv'
test_df = pd.read_csv(input_file_test, header=0)
y_test = test_df['activity'].as_matrix()

# remove the non-numeric columns
test_df = test_df._get_numeric_data()

# put the numeric column names in a python list
test_numeric_headers = list(test_df.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
test_numeric_array = test_df.as_matrix()
x_test = test_numeric_array

############################################################################

"""
Cs = np.logspace(-6, 3, 10)
parameters = [{'kernel': ['rbf'], 'C': Cs},
              {'kernel': ['linear'], 'C': Cs}]

svc = SVC(random_state = 12)

clf = GridSearchCV(estimator = svc, param_grid = parameters, cv = 5, n_jobs = -1)
clf.fit(x_train, y_train)

print (clf.best_params_)
print (clf.best_score_)
test_score = clf.score(x_test, y_test)
print(test_score)
#joblib.dump(clf, 'sonar.pkl')
"""
# after using grid search
# {'C': 0.001, 'kernel': 'linear'} has 0.96 accuracy

clf = SVC(C=0.001, kernel='linear', random_state = 12)
clf.fit(x_train, y_train)
test_score = clf.score(x_test, y_test)
print(test_score)
joblib.dump(clf, 'sonar.pkl')


crosstab = pd.crosstab(y_test, clf.predict(x_test),rownames=['True'], colnames=['Predicted'],margins=True)
print(crosstab)
