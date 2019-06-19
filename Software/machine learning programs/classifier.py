import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn import tree
import graphviz
from sklearn.externals import joblib

def transform_sonar(var):
    #OPEN: 0, SEMI: 0.5, PASS: 0.75, CLOSED: 1
    if var == "OPEN":
        return 0
    elif var == "SEMI":
        return 0.5
    elif var == "PASS":
        return 0.75
    elif var == "CLOSED":
        return 1
    else:
        return 2

def transform_pressure(var):
    #SITTING:0, STAND:1
    if var == "SITTING":
        return 0
    elif var == "STAND":
        return 1
    else:
        return 2

def transform_door(var):
    #OPEN:0, CLOSE:1
    if var == "NONE":
        return 0
    elif var == "OPEN":
        return 1
    elif var == "CLOSE":
        return 2
    else:
        return 3

def transform_window(var):
    #OPENED:0, CLOSED:1,
    #OPEN: 2, CLOSE: 3
    if var == "OPENED":
        return 0
    elif var == "CLOSE":
        return 1
    elif var == "OPEN":
        return 2
    elif var == "CLOSE":
        return 3
    else:
        return 4


def transform_mobile(var):
    #STATIC: 0, SIT_MOVE:1
    #SIT_TO_STAND: 2, WALKING:3, HAND_MOBILE:4
    if var == "STATIC":
        return 0
    elif var == "SIT_MOVE":
        return 1
    elif var == "SIT_TO_STAND":
        return 2
    elif var == "WALKING":
        return 3
    elif var == "HAND_MOBILE":
        return 4
    else:
        return 5

############################################################################
input_file_train = 'Sensor.csv'
train_df = pd.read_csv(input_file_train, header=0)
y_train = train_df['activity'].as_matrix()

# remove the non-numeric columns
train_df = train_df._get_numeric_data()

# put the numeric column names in a python list
train_numeric_headers = list(train_df.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
train_numeric_array = train_df.as_matrix()

x_train = train_numeric_array

a = np.hsplit(x_train, np.arange(1,16,1))
#lux: 0, tem_in: 1, tem_win: 2, sonar_in: 3, sonar_out: 4, move: 5, p: 6, adxyz: 7,8,9, awxyz: 10,11,12, mobile: 13, 14, 15
lux = a[0]
temp_in = a[1]
temp_win = a[2]
sonar = np.hstack((a[3], a[4]))
move = a[5]
pressure = a[6]
adxyz = np.hstack((a[7], a[8], a[9]))
awxyz = np.hstack((a[10], a[11], a[12]))
mobile = np.hstack((a[13], a[14], a[15]))

clf_sonar = joblib.load('sonar.pkl')
clf_pressure = joblib.load('pressure.pkl')
clf_door = joblib.load('doorACC.pkl')
clf_window = joblib.load('windowACC.pkl')
clf_mobile = joblib.load('mobileACC.pkl')

#predict single data entry: np.reshape(data[0], (1, -1))
input_sonar = np.reshape(clf_sonar.predict(sonar), (-1,1))
input_pressure = np.reshape(clf_pressure.predict(pressure), (-1,1))
input_door = np.reshape(clf_door.predict(adxyz), (-1,1))
input_window = np.reshape(clf_window.predict(awxyz), (-1,1))
input_mobile = np.reshape(clf_mobile.predict(mobile), (-1,1))

for i in range(0, input_sonar.shape[0]):
    input_sonar[i] = transform_sonar(input_sonar[i])
    input_pressure[i] = transform_pressure(input_pressure[i])
    input_door[i] = transform_door(input_door[i])
    input_window[i] = transform_window(input_window[i])
    input_mobile[i] = transform_mobile(input_mobile[i])

train_x = np.hstack((move,input_sonar, input_pressure, input_door, input_window, input_mobile))

feature = ['movement','sonar', 'pressure', 'door', 'window', 'mobile']
target_name = ['SITTING', 'SIT_MOVE', 'WALKING', 'CLOSEDOOR', 'OPEN_WIN', 'STAND', 'HAND_MOBILE','OPENDOOR']
############################################################################
## compare temperature in and out
###############
clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_x, y_train)
dot_data = tree.export_graphviz(clf, out_file=None, feature_names = feature, class_names = target_name, filled=True, rounded = True, special_characters = True)
graph = graphviz.Source(dot_data)
graph.render("sensor1.gv", view=True)
print(graph)

############################################################################
