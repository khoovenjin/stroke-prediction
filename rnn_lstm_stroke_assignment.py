# -*- coding: utf-8 -*-
"""RNN-LSTM Stroke Assignment.ipynb

**DATA PREPROCESSING**

Data: Kaggle = https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset?resource=download

Description: This dataset is used to predict whether a patient is likely to get stroke based on the input parameters like gender, age, various diseases, and smoking status.

Target Variable: Stroke (Binary)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Data Preprocessing
#
# Problem Statement: To predict the likeliness of a patient to encounter stroke
# with 0 being 'not likely' and 1 being 'likely'
#
# Purpose: Remove any anomalies spotted in EDA so that the data is more accurate
# to solve the problem statement
#
# Flow: EDA -> Data Preprocessing
#
# Steps Taken:
# 1) Understand and explore scope of data (use: shape for dimensions, info to check data_types,
# describe to view proportion of numerical data, unique/nunique to check unique data of classification attributes)
#
# 2) Adjust Incorrect Attribute Data Types (Optional: If needed, checked in info, unique)
# Reason to wrong data type: could be typo error, mispell, capitalization, wrong format,
# misinterpretation of attribute during data fill-ups etc.
# Steps: detect the rows involved -> replace value with attribute's mean -> re-check data_type (either replace or astype)
# 
# 3) Handle Duplication Data (Deletion, mostly CATEGORICAL/string)
# Reason to duplication: could be database or function problem, runtime issue, human mistakes (customer inputs twice)
# Steps: identify attribute data that CANNOT be duplicated (e.g: id) -> detect duplicated attribute data (column) ->
# detect duplicated records (rows) -> delete duplication (use drop w/ axis) 
#
# 4) Perform 1st EDA (visually & statistically detect & remove outliers)
# Reason to EDA: To explore patterns, find out anomalies such as outliers, and test hypothesis and early assumptions which
# further helps in understanding the data to make better future analysis
# Steps: do Descriptive Statistical Information (done w/ describe; compare std w/ mean) -> highlight attributes w/ outlier (min & max) ->
# plot boxplot, histogram, scatterplot (to verify) -> detect rows/col involved -> decision to remove or replace (use drop or replace) ->
# re-check EDA
#
# (VERY IMPORTANT: We put removing outliers before handling missing data because if we decide
# to impute missing data with mean, the imputed data is affected by the outlier's value)
# 5) Handle Missing Data (Deletion or Imputation)
# Reason to missing data: could be sensitive data, typo error etc.
# Steps: detect rows/col involved -> decision to delete or impute based on %/No. of Missing ->
# delete/impute data (use isnull/fillna/simpleimputer)
#
# 6) Perform Label Encoding (for Categorical data)
# Reason: to convert string data into numerical data so that is readable by binary machine
# Steps: detect col involved -> do label encoding (use simpleEncoder, factorize, onehotencoder)
# 
# 7) Perform Variable Assignment (x and y dataset)
# Reason: to select suitable input dataset which influences target variable dataset
# Steps: check significance of x to y (use OSL) -> remove low significance -> check correlation between attributes (use corrs, heatmap) ->
# take 1 high correlated attribute -> assign inputs to x, assign TV to y (use select, iloc) -> recheck significance (OSL)
#
# 8) Perform Class Balancing (for Categorical data)
# Steps: detect TV -> do class balancing (over-sampling or under-sampling)
#
# 9) Perform Normalization (for NN)
# Reason: to obtain mean close to 0 via scale down, so that learning rate is optimal and faster convergence
# Steps: normalize x -> check normalized_x (use normalize)
#
# 10) Perform Data Splitting (train set, test set, x, y)
# Reason: to split train and test dataset; train set use to build model with default hyperparameter algorithm;
# test set use to get predicted values to be evaluated against actual y value
# Steps: split x and y into trainx, testx, trainy, testy (define split ratio and random state)
#
# 11) Build and Train Model Solution (w/ DL algorithm selected)
# Reason: to get equation of solution to solve the problem statement
# Steps: select algorithm -> set hyperparameters -> fit and transform -> predict using testx 
#
# 12) Evaluate Result (Numerical or Categorical)
# Reason: to evaluate the 'accuracy' or how optimal or trustworthy is the model solution to solve the problem
# Steps: select score -> evaluate ypred against yactual
#
# 13) Perform Optimization and HyperParameterTuning (search for better model)
# Reason: to improve the accuracy of the model to solve the problem statement
# Steps: select suitable method -> search for optimal hyperparameters -> build the optimal model ->
# evaluate optimal result vs previous result -> Present findings via plottings
# 
# Load Dataset using pandas
data = pd.read_csv('/content/healthcare-dataset-stroke-data.csv')

# View first 5 rows
data.head()

# STEP 1 (Understand and explore scope of data)
#
# View data dimensions (row, column)

count_label = np.asarray(['No. of Records', 'No. of Columns:'])

dict = {}
for index, i in enumerate(count_label):
    dict[i] = data.shape[index]

pd.DataFrame(dict,index=["count"]).transpose()

# Understand the variables or column exist within the dataset
#
# List down all the name of the columns within the dataset
data.columns

# STEP 2 (Adjust Incorrect Attribute Data Types)
#
# Check data types
# Verdict: All attributes are in correct data type, 7 int types, 5 string
data.info()

# View Summary of Data
# Verdicts:
# 1) Correct 7 int attributes displayed
# 2) Outliers suspected (std > mean) = hypertension, heart_disease, stroke (ignore)
# 3) Outliers to consider (min, max values) = age (min = 0.08), avg_glucose_level (min = 55.12, max = 271.74), but still consider BMI (max = 97)
# 4) BMI has missing records = (5110 total - 4909: 201 missing data)
#
# Citation Acceptable Glucose Level (70-200): https://www.singlecare.com/blog/normal-blood-glucose-levels/#:~:text=A%20normal%20blood%20glucose%20level,90%20to%20110%20mg%2FdL.
# Citation Acceptable BMI Value (9-105 <- Highest BMI ever recorded): https://bmicalculator.mes.fm/bmi-chart
data.describe()

# View number of unique data in each attribute
# Verdicts:
# 1) From this, take low unique count and display unique data to validate value
dict = {}
for i in list(data.columns):
    dict[i] = data[i].value_counts().shape[0]

pd.DataFrame(dict,index=["unique count"]).transpose()

# View unique data in each attribute
# Verdicts:
# 1) Find out more about 'Other' in gender column
# 2) Find out more about 'children' in work_type column
# 3) Find out more about 'Unknown' in smoking_status column
# 4) Standardize all data to lowercase
data_select = data[['gender', 'hypertension', 'heart_disease', 'ever_married',
                   'work_type', 'Residence_type', 'smoking_status', 'stroke']]
dict = {}
for i in list(data_select.columns):
    dict[i] = ', '.join(str(x) for x in data_select[i].unique())

pd.DataFrame(dict,index=["unique value"]).transpose()

# View record having 'Other' as 'gender'
# Verdicts:
# 1) Since the count is 1, Discard this record later
display(data[data['gender'] == 'Other'])

# View record having 'children' as 'work_type'
# Verdicts:
# 1) There is 687 records having children, so it is not a mistype, Do Nothing about it
display(data[data['work_type'] == 'children'])

# Calculate percentage of record having 'Unknown' as 'smoking_status'
percentage_unknown = round(data[data['smoking_status'] == 'Unknown'].shape[0]/data.shape[0]*100, 2)
print('Percentage of data Unknown as smoking_status',
      percentage_unknown, '%')

# View record having 'Unknown' as 'smoking_status'
# Verdicts:
# 1) There is 1544 records having Unknown, which is 30.22% pretty high, 2 options:
# take it as it is or replace with mode ; CANNOT DISCARD because too many records,
# if discard, data is not accurate anymore
# Answer: Take it as it is (Do nothing)
display(data[data['smoking_status'] == 'Unknown'])

# Handle Capitalization and 1 record of 'Other' as 'gender'
# Drop data
data.drop(data.index[data['gender'] == 'Other'], inplace = True)

# Reset index of dataframe
data = data.reset_index(drop = True)
print('Unique data in gender', data['gender'].unique())
print('Total Records: ', data.shape[0])

# Change all to lowercase
data['gender'] = data['gender'].str.lower()
data['ever_married'] = data['ever_married'].str.lower()
data['work_type'] = data['work_type'].str.lower()
data['Residence_type'] = data['Residence_type'].str.lower()
data['smoking_status'] = data['smoking_status'].str.lower()

data_select = data[['gender', 'hypertension', 'heart_disease', 'ever_married',
                   'work_type', 'Residence_type', 'smoking_status', 'stroke']]
dict = {}
for i in list(data_select.columns):
    dict[i] = ', '.join(str(x) for x in data_select[i].unique())

pd.DataFrame(dict,index=["unique value"]).transpose()

# STEP 3 (Handle Duplication Data)
#
# Verdicts:
# 1) No duplicated records detected, can skip this step
# Detect duplicated records by id
print("Number of duplicated ID: ", data[data.columns[0]].duplicated().sum())

# Detect duplicated records by all attributes
print("Number of duplicated Records: ", data.duplicated().sum())

# STEP 4 (Perform 1st EDA)
# Descriptive Statistical Information is DONE ALREADY EARLIER
# ...bringing the verdict:
# 1) Outliers suspected (std > mean) = hypertension, heart_disease, stroke (ignore)
# 2) Outliers to consider (min, max values) = age (min = 0.08), avg_glucose_level
# (min = 55.12, max = 271.74), but still consider BMI (max = 97)
#
# Plot boxplot (Handling verdict 2: age, avg_glucose_level, bmi)
# ----------------------------------------------------------------
# Boxplot shows how well your data is dispersed and distributed which tells you if your
# data is symmetrical, how tightly your data is grouped, and if and how your data is skewed.
# Even they show outliers visibly that is position OUTSIDE OF MAX or MIN boundary.
# ----------------------------------------------------------------
# Verdicts:
# 1) Age against Stroke boxplot shows outliers
# 2) BMI against Stroke boxplot shows outliers (dot is spread so far away when Stroke = 0)
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18, 6) , squeeze=True) # Segment subplots arranged as 1 row and 3 columns

sns.boxplot(data=data, y=data['age'], x=data['stroke'], ax=axes[0]) # axes refers to column positioning when row is 1
sns.boxplot(data=data, y=data['bmi'], x=data['stroke'], ax=axes[1])
sns.boxplot(data=data, y=data['avg_glucose_level'], x=data['stroke'], ax=axes[2])

plt.show

# Plot histogram (Handling verdict 1: hypertension, heart_disease, and others)
# -----------------------------------------------------
# Histogram shows the frequency comparison between 2 or more types of attributes or
# data value which helps us to decide actions to take on the distribution shown,
# It shows the Relationship too between x and y
# -----------------------------------------------------
# Verdicts:
# 1) There are more people w/o stroke than w/ stroke which means the data is not
# balanced
fig, axes = plt.subplots(nrows = 3, ncols = 3, figsize = (18, 18))

fig.delaxes(ax=axes[2,1]) # to delete extra subplots located at row 2, col 1 & 2
fig.delaxes(ax=axes[2,2])

sns.countplot(x="gender", hue='stroke', data=data , ax=axes[0,0])
sns.countplot(x="hypertension", hue='stroke', data=data , ax=axes[0,1])
sns.countplot(x="heart_disease", hue='stroke', data=data , ax=axes[0,2])

sns.countplot(x="ever_married", hue='stroke', data=data , ax=axes[1,0])
sns.countplot(x="work_type", hue='stroke', data=data , ax=axes[1,1])
sns.countplot(x="Residence_type", hue='stroke', data=data , ax=axes[1,2])

sns.countplot(x="smoking_status", hue='stroke', data=data , ax=axes[2,0])

plt.show()

# Plot scatterplot (Handling verdict 2: age, avg_glucose_level, bmi)
# ----------------------------------------------------
# Scatterplot reveals outliers which are spread far away from the mean
# ----------------------------------------------------
# Verdicts:
# 1) To confirm verdicts in boxplot, BMI and age have outliers.
# However, these are against stroke. We must confirm individually w/o stroke.
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18, 6) , squeeze=True)

sns.scatterplot(data=data, x=data['stroke'], y=data['age'], ax=axes[0])
sns.scatterplot(data=data, x=data['stroke'], y=data['bmi'], ax=axes[1] )
sns.scatterplot(data=data, x=data['stroke'], y=data['avg_glucose_level'], ax=axes[2])

plt.show

# To Re-Confirm outliers in age and BMI
# Plot Individual Boxplot
# Verdicts:
# 1) Age shows NO outliers, while BMI still shows outliers of value > 70.
# Therefore, conduct outliers removal on BMI respectively
fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (10, 6) , squeeze=True)

sns.boxplot(data=data, y=data['age'], ax=axes[0])
sns.boxplot(data=data, y=data['bmi'], ax=axes[1])

plt.show

# Display rows with 'bmi' > 70
# Verdicts:
# 1) It shows 4 records of outliers which is VERY SMALL to 5109 total records,
# therefore not an issue to discard these outliers
display(data[data['bmi'] > 70])

# Discard outliers
data.drop(data.index[data['bmi'] > 70], inplace = True)

# Reset index of data
data = data.reset_index(drop = True)

# Checking outliers after handling outliers
# OUTLIERS ARE GONE!!!
plt.figure(figsize = (4,5)) # set figure size

sns.boxplot(data=data, y=data['bmi'])

plt.show

# STEP 5 (Handle missing data)
#
# Check missing value
# Verdicts:
# 1) Yes, we were right, there are 201 missing data in 'bmi'
print(data.isnull().sum())

# Check percentage of missing data
# Verdicts:
# 1) Since 3.94% is very little, imputing it with mean shouldn't be
# much of hassle and it wont affect much to the overall data
print('Percentage of missing data: ', round(data['bmi'].isnull().sum()/data.shape[0]*100, 2), '%')

# Impute missing data with mean
# MISSING DATA IS GONE!!!
data["bmi"] = data["bmi"].fillna(data["bmi"].mean())
print(data.isnull().sum())

# STEP 6 (Perform Label Encoding)
# 
# Factorize Categorical Data to Numerical
data_select = data.select_dtypes(include='object')
for i in list(data_select.columns):
    data[i] = pd.factorize(data[i])[0]

data.head()

# Check encoding by viewing unique values
# LABEL ENCODING SUCCEEDED!!!
dict = {}
for i in list(data_select.columns):
    dict[i] = ', '.join(str(x) for x in data[i].unique())

pd.DataFrame(dict,index=["unique value"]).transpose()

# STEP 7 (Perform Variable Assignment)
#
# Dropping column that is not revelant which in this case, id column is not required as it is just the number of the record.
data = data.drop(['id'], axis = 1)

data

# As the Target Variable (TV) is stroke, the value for this column will be saved in Y, while the others will be saved in X as Input Variable (IV)
# Checking the correlation of the v

x = data.iloc[:, 0:9] # Input Variable
y = data.iloc[:, 10] # Target Variable

print (x)
print (y)

# Checking the correlation of between all the variables within the dataset, but more importantly is to understand the correlation between the target variable and the input variable.
#
# High correlation instance variable can be choosen as the main variable to be used for prediction
# If there are any variable that has high correlation between each other (> 0.8), it should be drop to pervent wrong prediction.
data.corr()

# Heatmap is created to understand the correlation between the variable more easily.
#
# Since there are no variables that contain correlation over 0.8, no column will be dropped. 
# Based on the heatmap, the three variable that is most correlated to the target variable (stroke) are
# age, (hypertension, heart_disease, avg_glucose_level) = same value
plt.figure(figsize = (15, 15))
sns.heatmap(data.corr(), annot = True)

# Performing OLS Regression Result to check whether the IV and TV is related and suitable to be used as the input variable
#
# Adding constant into the existing x (input variable) for OLS Regression 
# Import statsmodel.api for OLS Regression
import statsmodels.api as sm
X = sm.add_constant(x)
est = sm.OLS(y, X).fit()
print (est.summary())

# Based on the OLS Regression result, we can determine that there are some input variable is not significant towards the target values 
# since the P value for the input variable is greater than the significant value (0.05)
# Input variable that is higher than the significant value include gender, work_type and Residence_type
# Therefore, these three column will be dropped from x

x.drop(columns = ['gender', 'work_type', 'Residence_type'], axis = 1, inplace = True)

# the Input value will be tested in the OLS Regression Test again to check whether the IV and TV is suitable
X = sm.add_constant(x)
est = sm.OLS(y, X).fit()
print (est.summary())

# STEP 8 (Perform Class Balancing)
#
# Class Balancing is done on the Target Variable if the target variable is not balanced.
# Countplot is used to show the number of class amount in the stroke column.
sns.countplot(x = y)

# Based on graph, the number of patient that had stroke is significantly lower then the number of patient that does not have stroke.
# This means that the class for Target Variable to be extremely unbalanced
# Two methods to treat imbalanced class, Under or Over Sampling. 
# Oversampling is done to prevent data lost as the differences of the 0 and 1 is too much
# under sampling means that huge amount of data will be deleted
#
# Oversampling is done using SMOTE

from imblearn.over_sampling import SMOTE
x_b, y_b = SMOTE().fit_resample(x, y)
print(y_b.value_counts())
sns.countplot(x = y_b)

# STEP 9 (Perform Normalization)
#
# Normalization is done with the help of sklearn

from sklearn.preprocessing import normalize

x_n = normalize(x_b)
x_n

# STEP 10 (Perform Data Splitting)
#
# Splitting the data into test and training data in the ratio of 2:8
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_n, y_b, test_size = 0.2, random_state = 2)

print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

# The data is split into 80% for training test and 20% for testing test
# Train data -> 7769
# Test data -> 1943

# STEP 11 (Build and Train Model Solution)
#
# Re-shape x_train and x_test data into 7769 samples of 1 row record with 6 columns
x_n_column = x_n.shape[1]
x_train= np.array(x_train).reshape(len(x_train), 1, x_n_column)
x_test= np.array(x_test).reshape(len(x_test), 1, x_n_column)
print(x_train.shape, x_test.shape)

# Set Class Weights using y_train Key-to-Value pair in an Array Dictionary
# 
# Parameter settings:
# 1) class_weight set as 'balanced' to be given by n_samples / (n_classes * np.bincount(y))
# 2) classes set as 'np.unique(y_train)' to define an array of unique classes occuring in data
# 3) y set as 'y_train' to defined an array of original class labels per sample
#
from sklearn.utils import class_weight

class_weights = class_weight.compute_class_weight(class_weight = 'balanced',
                                                  classes = np.unique(y_train), y = y_train)
class_weights = {0: class_weights[0], 1: class_weights[1]}
class_weights

# Select algorithm (as RNN-LSTM), Set default hyperparameters
#
# Model Details:
# 1) Type: Recurrent Neutral-Network (RNN)
# 2) Derivative: Long-Short Term Memory (LSTM)
# 
# Default Model Building Parameters:
# 1) No. of LSTM Layers: 3
# 2) No. of LSTM Units: 50
# 3) Dropout Value: 0.2 (Optimal between 0.0 - 0.5; if > 0.6 is unacceptable)
# - Purpose: To prevent overfitting and underfitting of the model, thus produce smoother result
# 4) No. of Dense Unit: 1
# 5) Dense Activation Function: Sigmoid (Because TV is binary classification)
# 6) Loss Function: Binary Cross Entropy (Because TV is binary classification) 
# 7) Optimizer: Adam (widely accepted default optimizer)
# 8) Metrics: Accuracy (Because TV is binary classification)
#
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

model = Sequential()
model.add(LSTM(units = 50, return_sequences=True, input_shape=(1, x_train.shape[2])))
model.add(Dropout(0.2))

model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))

model.add(LSTM(units = 50))
model.add(Dropout(0.2))

model.add(Dense(units = 1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

# Fit and Transform
#
# Default Model Building Parameters:
# 9) No. of Epochs: 100 (Set at moderate-high which is widely accepted as default no. of epochs)
# 10) Batch Size: 32 (Set on moderate-low to improve learning process and save time)
# 11) Class Weight Model: set as class_weights dictionary by y_train
history = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=100, batch_size=32, class_weight=class_weights)

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Test'], loc = 'upper left')
plt.show()

# Predict x_test
#
predictions= model.predict(x_test)
predictions

# View sum value of predictions and data type
#
sum(predictions)

# Segment prediction value (more than 0.5 is True, less than 0.5 is False)
# 
# Verdicts:
# 1) Based on a Sigmoid Graph, the output value MUST be BINARY (True or False; 0 or 1),
# thus to solve the float predicted values, any output > 0.5 is taken as True, and otherwise.
#
y_pred = (predictions > 0.5)

y_pred

# STEP 11: (Evaluate Result)
# Evaluate Model by Accuracy, Precision, Recall and F1 Score
#
# Verdicts:
# 1) 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
print('Accuracy of MLP Classifier: ', accuracy_score(y_test, y_pred))
print('Precision of MLP Classifier: ', precision_score(y_test, y_pred, average = 'binary'))
print('Recall of MLP Classifier: ', recall_score(y_test, y_pred, average = 'binary'))
print('F1 Score of MLP Classifier: ', f1_score(y_test, y_pred, average = 'binary'))

# View Confusion Matrix
#
from sklearn.metrics import confusion_matrix, classification_report
confusion_matrix(y_test, y_pred)

# View Classification Report
#
print(classification_report(y_test, y_pred))

# Plot ROC-AUC Diagram
import sklearn.metrics as metrics
FP, TP, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(FP, TP)

import matplotlib.pyplot as plt
plt.subplots(1, figsize = (7,7))
plt.title('ROC')
plt.plot(FP, TP, label = 'DNN_AUC = %0.2f' % roc_auc)
plt.plot([0,1], ls = '--')
plt.xlabel('True Positive')
plt.ylabel('False Positive')
plt.legend()

# STEP 13 (Perform Optimization and HyperParameterTuning)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
import tensorflow as tf

!pip install -q -U keras-tuner

import keras_tuner as kt
from kerastuner.tuners import RandomSearch

def model_builder(hp):
  model = Sequential()
  model.add(LSTM(hp.Int('input_unit',min_value=32,max_value=512,step=32),
                 return_sequences=True, input_shape=(1, x_train.shape[2])))
  model.add(Dropout(hp.Float('Dropout_initial',min_value=0.0,max_value=0.5,step=0.1)))

# No of Layers
  for i in range(hp.Int('No of Layers', 1, 3)):

    # No of Neurons
    hp_units = hp.Int('Units_'+str(i), min_value=32, max_value=512, step=32)
    model.add(LSTM(units = hp_units, return_sequences=True))

    # Dropout Value
    hp_dropout = hp.Float('Dropout_rate', min_value=0.0, max_value=0.5, step=0.1)
    model.add(Dropout(hp_dropout))

  model.add(LSTM(hp.Int('output_unit',min_value=32,max_value=512,step=32)))
  model.add(Dropout(hp.Float('Dropout_exit',min_value=0.0,max_value=0.5,step=0.1)))

  model.add(Dense(units = 1,
                  activation=hp.Choice('dense_activation',values=['relu', 'sigmoid'],default='sigmoid')))
  
  hp_optimizer = hp.Choice('Optmizer', ['sgd', 'adam', 'rmsprop'])
  model.compile(optimizer=hp_optimizer, loss='binary_crossentropy', metrics = ['accuracy'])

  return model

tuner = RandomSearch(model_builder, objective = 'val_accuracy', max_trials = 5, executions_per_trial = 3,
                        directory = 'Tuning_RNN_LSTM', project_name = 'Stroke Prediction', overwrite = True)

tuner.search(
    x=x_train,
    y=y_train,
    epochs=50,
    batch_size=32,
    validation_data=(x_test,y_test)
)

best_model = tuner.get_best_models(num_models=1)[0]

best_model.summary()

best_hp = tuner.get_best_hyperparameters(num_trials=1)[0]

best_hp.values

optimized_model = tuner.hypermodel.build(best_hp)

pip install scikeras[tensorflow]

# Find Best Batch Size and Epochs
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import RandomizedSearchCV

def build_model_RandomizedSearch():
  model_gs = Sequential()
  model_gs.add(LSTM(units = 64, return_sequences=True, input_shape=(1, x_train.shape[2])))
  model_gs.add(Dropout(0.2))

  model_gs.add(LSTM(units = 416, return_sequences = True))
  model_gs.add(Dropout(0.1))

  model_gs.add(LSTM(units = 416, return_sequences = True))
  model_gs.add(Dropout(0.1))

  model_gs.add(LSTM(units = 64))
  model_gs.add(Dropout(0.0))

  model_gs.add(Dense(units = 1, activation='sigmoid'))

  model_gs.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

  model_gs.summary()
  return model_gs

model_kc = KerasClassifier(model = build_model_RandomizedSearch, verbose = 2)

batch_size = [32,64,128]
epochs = [150,200,250]
param_random = {'batch_size': batch_size, 'epochs': epochs}

RNN_LSTM_random = RandomizedSearchCV(model_kc, param_random, cv = 5, n_jobs = -1, verbose = 1)
RNN_LSTM_random = RNN_LSTM_random.fit(x_train, y_train)

print('Best Model Fitting Parameters: ', RNN_LSTM_random.best_params_)
print('Best Score: ', RNN_LSTM_random.best_score_)

# Build Best Model
#
model_optimized = Sequential()
model_optimized.add(LSTM(units = 64, return_sequences=True, input_shape=(1, x_train.shape[2])))
model_optimized.add(Dropout(0.2))

model_optimized.add(LSTM(units = 416, return_sequences = True))
model_optimized.add(Dropout(0.1))

model_optimized.add(LSTM(units = 416, return_sequences = True))
model_optimized.add(Dropout(0.1))

model_optimized.add(LSTM(units = 64))
model_optimized.add(Dropout(0.0))

model_optimized.add(Dense(units = 1, activation='sigmoid'))

model_optimized.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model_optimized.summary()

# Train Best Tuned Model
#
history_optimized = model_optimized.fit(x_train, y_train, validation_data = (x_test, y_test),
                                        epochs=250, batch_size=32, class_weight=class_weights)

plt.plot(history_optimized.history['accuracy'])
plt.plot(history_optimized.history['val_accuracy'])
plt.title('Optimized Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Test'], loc = 'upper left')
plt.show()

# Predict x_test
#
predictions_optimized= model_optimized.predict(x_test)
predictions_optimized

y_pred_optimized = (predictions_optimized > 0.5)

y_pred_optimized

print('Accuracy of MLP Classifier: ', accuracy_score(y_test, y_pred_optimized))
print('Precision of MLP Classifier: ', precision_score(y_test, y_pred_optimized, average = 'binary'))
print('Recall of MLP Classifier: ', recall_score(y_test, y_pred_optimized, average = 'binary'))
print('F1 Score of MLP Classifier: ', f1_score(y_test, y_pred_optimized, average = 'binary'))

confusion_matrix(y_test, y_pred_optimized)

print(classification_report(y_test, y_pred_optimized))

# Plot ROC-AUC Diagram
import sklearn.metrics as metrics
FP, TP, threshold = metrics.roc_curve(y_test, y_pred_optimized)
roc_auc = metrics.auc(FP, TP)

import matplotlib.pyplot as plt
plt.subplots(1, figsize = (7,7))
plt.title('ROC')
plt.plot(FP, TP, label = 'DNN_AUC = %0.2f' % roc_auc)
plt.plot([0,1], ls = '--')
plt.xlabel('True Positive')
plt.ylabel('False Positive')
plt.legend()
