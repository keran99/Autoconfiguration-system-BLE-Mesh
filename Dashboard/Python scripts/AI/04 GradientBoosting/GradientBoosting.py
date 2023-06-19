## Imports
"""

import xgboost as xgb
from sklearn.preprocessing import StandardScaler
import pandas as pd
from joblib import dump, load
import itertools
import csv

"""## Functions and variables"""

def conversionMs(x):
    return round(x / 2000000, 3)

DelayValues = [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15]
PDRValues = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

DeviceID = [3]

TTLValues = [2,3,4,5]
TransmissionPowerValues = [1,3,6]
TransmissionNumberValues = [1,3,5]
IntervalTimeValues = [1,2,3,4,5]

TTLValueSet = [2,3,4,5]
TPValueSet = [1,3,6]
TNValueSet = [1,3,5]
TIValueSet = [1,2,3,4,5]

"""## Dataset"""

# Caricare i dati di esempio
data_performance = pd.read_csv("parameters_performance.csv")
data_pdr =  pd.read_csv("parameters_pdr.csv")
data_performance['Delay'] = data_performance['Delay'].apply(conversionMs)
data_pdr['PDR'] = data_pdr['PDRReceived'] / data_pdr['PDRSend']
dataset = pd.merge(data_performance, data_pdr, on=['TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime', 'DeviceID'])

"""## Gradient Boosting model creation

### Gradient Boosting model creation - predictor of 5 variables

#### Delay - NodeID
"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'DeviceID']
target_features = ['TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/01 Boosting-Delay.joblib')

"""#### PDR - NodeID"""

# Seleziona le feature di input e il target
input_features = ['PDR', 'DeviceID']
target_features = ['TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/02 Boosting-PDR.joblib')

"""### Gradient Boosting model creation - predictor of 4 variables"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'PDR', 'DeviceID']
target_features = ['TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/03 Boosting.joblib')

"""### Gradient Boosting model creation - predictor of 3 variables

#### Delay - PDR - DeviceID - TTL
"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'PDR', 'DeviceID', 'TTL']
target_features = ['TransmissionPower', 'TransmissionsNumber', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/04 Boosting - TTL.joblib')

"""#### Delay - PDR - DeviceID - TransmissionPower"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'PDR', 'DeviceID', 'TransmissionPower']
target_features = ['TTL', 'TransmissionsNumber', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/05 Boosting - TransmissionPower.joblib')

"""#### Delay - PDR - Delay - TransmissionsNumber"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'PDR', 'DeviceID', 'TransmissionsNumber']
target_features = ['TTL', 'TransmissionPower', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/06 Boosting - TransmissionsNumber.joblib')

"""#### Delay - PDR - DeviceID - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'PDR', 'DeviceID', 'IntervalTime']
target_features = ['TTL', 'TransmissionPower', 'TransmissionsNumber']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/07 Boosting - IntervalTime.joblib')

"""### Decision Tree model creation - Predictor of 2 variables

#### Delay - PDR - DeviceID - TTL - TransmissionPower
"""

# Seleziona le feature di input e il target
input_features = ['Delay', 'PDR', 'DeviceID', 'TTL', 'TransmissionPower']
target_features = ['TransmissionsNumber', 'IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/08 Boosting-TTL-TransmissionPower.joblib')

"""#### Delay - PDR - DeviceID - TTL - TransmissionsNumber"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionsNumber"]
target_features = ["TransmissionPower", "IntervalTime"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/09 Boosting-TTL-TransmissionsNumber.joblib')

"""#### Delay - PDR - DeviceID - TTL - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TTL", "IntervalTime"]
target_features = ["TransmissionPower", "TransmissionsNumber"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/10 Boosting-TTL-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TransmissionPower - TransmissionsNumber"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TransmissionPower", "TransmissionsNumber"]
target_features = ["TTL", "IntervalTime"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/11 Boosting-TransmissionPower-TransmissionsNumber.joblib')

"""#### Delay - PDR - TransmissionPower - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TransmissionPower", "IntervalTime"]
target_features = ["TTL", "TransmissionsNumber"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/12 Boosting-TransmissionPower-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TransmissionsNumber - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TransmissionsNumber", "IntervalTime"]
target_features = ["TTL", "TransmissionPower"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/13 Boosting-TransmissionsNumber-IntervalTime.joblib')

"""### Decision Tree Model Creation - Predictor of 1 variable

#### Delay - PDR - DeviceID - TTL - TransmissionPower - TransmissionsNumber
"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionPower", "TransmissionsNumber"]
target_features = ["IntervalTime"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/14 Boosting-TTL-TransmissionPower-TransmissionsNumber.joblib')

"""#### Delay - PDR - DeviceID - TTL - TransmissionPower - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionPower", "IntervalTime"]
target_features = ["TransmissionsNumber"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/15 Boosting-TTL-TransmissionPower-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TTL - TransmissionsNumber - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionsNumber", "IntervalTime"]
target_features = ["TransmissionPower"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/16 Boosting-TTL-TransmissionsNumber-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TransmissionPower - TransmissionsNumber - IntervalTime"""

# Seleziona le feature di input e il target
input_features = ["Delay", "PDR", "DeviceID", "TransmissionPower", "TransmissionsNumber", "IntervalTime"]
target_features = ["TTL"]

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = xgb.XGBRegressor()
model.fit(X, y)

dump(model, 'Models/17 Boosting-TransmissionPower-TransmissionsNumber-IntervalTime.joblib')

"""## Prediction

### Prediction of 5 variables

#### Prediction of 5 variables - Delay
"""

# Carica il modello addestrato
clf = load('Models/01 Boosting-Delay.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, DeviceID))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'DeviceID']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    # print(f"Index: {index}")
    # print(f"Delay: {row['Delay']}")
    # print(f"DeviceID: {row['DeviceID']}")
    # print()
    row = []
    DelayValue = float(inputRow['Delay'])
    IDNodo = int(inputRow['DeviceID'])
    # TTL = round(prediction[i][0])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    # TransmissionPower = round(prediction[i][1])
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][1]))
    # TransmissionsNumber = round(prediction[i][2])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][2]))
    # IntervalTime = round(prediction[i][3])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][3]))

    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/01 Boosting-Delay.csv', index=False)

"""#### Prediction of 5 variables - PDR"""

# Carica il modello addestrato
clf = load('Models/02 Boosting-PDR.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(PDRValues, DeviceID))
dataframeInput = pd.DataFrame(combinations)
header = ['PDR', 'DeviceID']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    PDRValue = inputRow['PDR']
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][1]))
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][2]))
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][3]))

    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/02 Boosting-PDR.csv', index=False)

"""### Predictior of 4 variables"""

# Carica il modello addestrato
clf = load('Models/03 Boosting.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][1]))
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][2]))
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][3]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/03 Boosting.csv', index=False)

"""### Predictor of 3 variables

#### Prediction of 3 variables - TTL
"""

# Carica il modello addestrato
clf = load('Models/04 Boosting - TTL.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][1]))
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][2]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/04 Boosting-TTL.csv', index=False)

"""#### Prediction of 3 variables - TransmissionPower"""

# Carica il modello addestrato
clf = load('Models/05 Boosting - TransmissionPower.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TransmissionPowerValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TransmissionPower']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  int(inputRow['TransmissionPower'])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][1]))
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][2]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/05 Boosting-TransmissionPower.csv', index=False)

"""#### Prediction of 3 variables - TransmissionsNumber"""

# Carica il modello addestrato
clf = load('Models/06 Boosting - TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TransmissionNumberValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TransmissionsNumber']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionsNumber =  int(inputRow['TransmissionsNumber'])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][2]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/06 Boosting-TransmissionsNumber.csv', index=False)

"""#### Prediction of 3 variables - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/07 Boosting - IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][2]))
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/07 Boosting-IntervalTime.csv', index=False)

"""### Prediction of 2 variables

#### Predictior of 2 variables - TTL - TransmissionPower
"""

# Carica il modello addestrato
clf = load('Models/08 Boosting-TTL-TransmissionPower.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues, TransmissionPowerValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL', 'TransmissionPower']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower =  int(inputRow['TransmissionPower'])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][0]))
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][1]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/08 Boosting-TTL-TransmissionPower.csv', index=False)

"""#### Prediction of 2 variables - TTL - TransmissionsNumber"""

# Carica il modello addestrato
clf = load('Models/09 Boosting-TTL-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues, TransmissionNumberValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL', 'TransmissionsNumber']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionsNumber =  int(inputRow['TransmissionsNumber'])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][1]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/09 Boosting-TTL-TransmissionsNumber.csv', index=False)

"""#### Predictior of 2 variables - TTL - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/10 Boosting-TTL-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][1]))
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/10 Boosting-TTL-IntervalTime.csv', index=False)

"""#### Predictor of 2 variables - TransmissionPower - TransmissionsNumber"""

# Carica il modello addestrato
clf = load('Models/11 Boosting-TransmissionPower-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TransmissionPowerValues, TransmissionNumberValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TransmissionPower', 'TransmissionsNumber']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  int(inputRow['TransmissionPower'])
    TransmissionsNumber =  int(inputRow['TransmissionsNumber'])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index][1]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/11 Boosting-TransmissionPower-TransmissionsNumber.csv', index=False)

"""#### Predictor of 2 variables - TransmissionPower - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/12 Boosting-TransmissionPower-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TransmissionPowerValues, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TransmissionPower', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower =  int(inputRow['TransmissionPower'])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index][1]))
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/12 Boosting-TransmissionPower-IntervalTime.csv', index=False)

"""#### Predictor of 2 variables - TransmissionsNumber - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/13 Boosting-TransmissionsNumber-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TransmissionNumberValues, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TransmissionsNumber', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index][0]))
    TransmissionPower = min(TPValueSet, key=lambda x: abs(x - prediction[index][1]))
    TransmissionsNumber =   int(inputRow['TransmissionsNumber'])
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/13 Boosting-TransmissionsNumber-IntervalTime.csv', index=False)

"""### Prediction of 1 variable

#### Prediction of 1 variable - TTL - TransmissionPower - TransmissionsNumber
"""

# Carica il modello addestrato
clf = load('Models/14 Boosting-TTL-TransmissionPower-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues, TransmissionPowerValues, TransmissionNumberValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber =   int(inputRow['TransmissionsNumber'])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index]))

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/14 Boosting-TTL-TransmissionPower-TransmissionsNumber.csv', index=False)

"""#### Prediction of 1 variable - TTL - TransmissionPower - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/15 Boosting-TTL-TransmissionPower-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues, TransmissionPowerValues, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL', 'TransmissionPower', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index]))
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/15 Boosting-TTL-TransmissionPower-IntervalTime.csv', index=False)

"""#### Prediction of 1 variable - TTL - TransmissionsNumber - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/16 Boosting-TTL-TransmissionsNumber-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TTLValues, TransmissionNumberValues, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TTL', 'TransmissionsNumber', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = min(TPValueSet, key=lambda x: abs(x - prediction[index]))
    TransmissionsNumber = int(inputRow['TransmissionsNumber'])
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/16 Boosting-TTL-TransmissionsNumber-IntervalTime.csv', index=False)

"""#### Prediction of 1 variable - TransmissionPower - TransmissionsNumber - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/17 Boosting-TransmissionPower-TransmissionsNumber-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, DeviceID, TransmissionPowerValues, TransmissionNumberValues, IntervalTimeValues))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'PDR', 'DeviceID', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime']
dataframeInput.columns = header

prediction = clf.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    PDRValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index]))
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber = int(inputRow['TransmissionsNumber'])
    IntervalTime = int(inputRow['IntervalTime'])

    row.append(DelayValue)
    row.append(PDRValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

# print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/17 Boosting-TransmissionPower-TransmissionsNumber-IntervalTime.csv', index=False)

"""## Comandi
!zip -r ModelsBoosting.zip Models
!zip -r ResultsBoosting.zip Results
"""