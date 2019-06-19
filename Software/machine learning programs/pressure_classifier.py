import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.externals import joblib

############################################################################
input_file_train = 'pressure.csv'
train_df = pd.read_csv(input_file_train, header=0)
y_train = train_df['activity'].as_matrix()

# remove the non-numeric columns
train_df = train_df._get_numeric_data()

# put the numeric column names in a python list
train_numeric_headers = list(train_df.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
train_numeric_array = train_df.as_matrix()

x_train = train_numeric_array
dimention = y_train.shape
y_train = np.reshape(y_train, (dimention[0], 1))

# remove duplicate entries
composite = np.hstack((x_train, y_train))
newarray = [tuple(row) for row in composite]
uniques = np.unique(newarray, axis = 0)
x_train, y_train = np.hsplit(uniques, 2)
dimention = y_train.shape
y_train = np.reshape(y_train, (dimention[0], ))

############################################################################
input_file_test = 'testpressure.csv'
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
# using grid search to find most suitable kernel and it's parameters
Cs = np.logspace(-6, 3, 10)
parameters = [{'kernel': ['rbf'], 'C': Cs},
              {'kernel': ['linear'], 'C': Cs}]

svc = SVC(random_state = 12)

clf = GridSearchCV(estimator = svc, param_grid = parameters, cv = 5, n_jobs = -1)
clf.fit(x_train, y_train)

print (clf.best_params_)
print (clf.best_score_)
test_score = clf.score(x_test, y_test)
print("test_score: " + test_score)
joblib.dump(clf, 'pressure.pkl')

"""
# after using grid search
# {'C': 0.001, 'kernel': 'linear'} has 0.96 accuracy

clf = SVC(C=0.001, kernel='linear', random_state = 12)
clf.fit(x_train, y_train)

test_score = clf.score(x_test, y_test)
print(test_score)

crosstab = pd.crosstab(y_test, clf.predict(x_test),rownames=['True'], colnames=['Predicted'],margins=True)
print(crosstab)
"""
