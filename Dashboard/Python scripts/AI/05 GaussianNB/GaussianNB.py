from sklearn.naive_bayes import GaussianNB
import pandas as pd
from joblib import dump, load
import itertools
import csv

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

data_performance = pd.read_csv("parameters_performance.csv")
data_pdr =  pd.read_csv("parameters_pdr.csv")
data_performance['Delay'] = data_performance['Delay'].apply(conversionMs)
data_pdr['PDR'] = data_pdr['PDRReceived'] / data_pdr['PDRSend']
dataset = pd.merge(data_performance, data_pdr, on=['TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime', 'DeviceID'])

# Seleziona le feature di input e il target
input_features = ['Delay', 'DeviceID']
target_features = ['TTL']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/01 NaiveBayes-Delay-Step1.joblib')

# Seleziona le feature di input e il target
input_features = ['Delay', 'DeviceID', 'TTL']
target_features = ['TransmissionPower']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/01 NaiveBayes-Delay-Step2.joblib')

# Seleziona le feature di input e il target
input_features = ['Delay', 'DeviceID', 'TTL', 'TransmissionPower']
target_features = ['TransmissionsNumber']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/01 NaiveBayes-Delay-Step3.joblib')

# Seleziona le feature di input e il target
input_features = ['Delay', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber']
target_features = ['IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/01 NaiveBayes-Delay-Step4.joblib')

# Carica il modello addestrato
clf1 = load('Models/01 NaiveBayes-Delay-Step1.joblib')
clf2 = load('Models/01 NaiveBayes-Delay-Step2.joblib')
clf3 = load('Models/01 NaiveBayes-Delay-Step3.joblib')
clf4 = load('Models/01 NaiveBayes-Delay-Step4.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, DeviceID))
dataframeInput = pd.DataFrame(combinations)
header = ['Delay', 'DeviceID']
dataframeInput.columns = header

prediction = clf1.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    output.append(row)

dataframeOutputStep1 = pd.DataFrame(output)
header = ['Delay', 'DeviceID', 'TTL']
dataframeOutputStep1.columns = header

prediction = clf2.predict(dataframeOutputStep1)
output = []
for index, inputRow in dataframeOutputStep1.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    output.append(row)


dataframeOutputStep2 = pd.DataFrame(output)
header = ['Delay', 'DeviceID', 'TTL', 'TransmissionPower']
dataframeOutputStep2.columns = header

prediction = clf3.predict(dataframeOutputStep2)
output = []
for index, inputRow in dataframeOutputStep2.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    output.append(row)

dataframeOutputStep3 = pd.DataFrame(output)
header = ['Delay', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber']
dataframeOutputStep3.columns = header

prediction = clf4.predict(dataframeOutputStep3)
output = []
for index, inputRow in dataframeOutputStep3.iterrows():
    row = []
    DelayValue = float(inputRow['Delay'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber = int(inputRow['TransmissionsNumber'])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

dataframeOutputStep4 = pd.DataFrame(output)
header = ['Delay', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime']
dataframeOutputStep4.columns = header

print(dataframeOutputStep4)

dataframeOutputStep4.to_csv('Results/01 GaussinNB-Delay.csv', index=False)

"""## PDR"""

# Seleziona le feature di input e il target
input_features = ['PDR', 'DeviceID']
target_features = ['TTL']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/02 NaiveBayes-PDR-Step1.joblib')



# Seleziona le feature di input e il target
input_features = ['PDR', 'DeviceID', 'TTL']
target_features = ['TransmissionPower']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/02 NaiveBayes-PDR-Step2.joblib')



# Seleziona le feature di input e il target
input_features = ['PDR', 'DeviceID', 'TTL', 'TransmissionPower']
target_features = ['TransmissionsNumber']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/02 NaiveBayes-PDR-Step3.joblib')



# Seleziona le feature di input e il target
input_features = ['PDR', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber']
target_features = ['IntervalTime']

# Crea il dataset di training e testing con tutte le feature
X = dataset[input_features]
y = dataset[target_features]

# Crea il modello per la previsione di tutti i target
model = GaussianNB()
model.fit(X, y)

dump(model, 'Models/02 NaiveBayes-PDR-Step4.joblib')



# Carica il modello addestrato
clf1 = load('Models/02 NaiveBayes-PDR-Step1.joblib')
clf2 = load('Models/02 NaiveBayes-PDR-Step2.joblib')
clf3 = load('Models/02 NaiveBayes-PDR-Step3.joblib')
clf4 = load('Models/02 NaiveBayes-PDR-Step4.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(PDRValues, DeviceID))
dataframeInput = pd.DataFrame(combinations)
header = ['PDR', 'DeviceID']
dataframeInput.columns = header

prediction = clf1.predict(dataframeInput)
output = []
for index, inputRow in dataframeInput.iterrows():
    row = []
    DelayValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = min(TTLValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    output.append(row)

dataframeOutputStep1 = pd.DataFrame(output)
header = ['PDR', 'DeviceID', 'TTL']
dataframeOutputStep1.columns = header

prediction = clf2.predict(dataframeOutputStep1)
output = []
for index, inputRow in dataframeOutputStep1.iterrows():
    row = []
    DelayValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower =  min(TPValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    output.append(row)


dataframeOutputStep2 = pd.DataFrame(output)
header = ['PDR', 'DeviceID', 'TTL', 'TransmissionPower']
dataframeOutputStep2.columns = header

prediction = clf3.predict(dataframeOutputStep2)
output = []
for index, inputRow in dataframeOutputStep2.iterrows():
    row = []
    DelayValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber =  min(TNValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    output.append(row)

dataframeOutputStep3 = pd.DataFrame(output)
header = ['PDR', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber']
dataframeOutputStep3.columns = header

prediction = clf4.predict(dataframeOutputStep3)
output = []
for index, inputRow in dataframeOutputStep3.iterrows():
    row = []
    DelayValue = float(inputRow['PDR'])
    IDNodo = int(inputRow['DeviceID'])
    TTL = int(inputRow['TTL'])
    TransmissionPower = int(inputRow['TransmissionPower'])
    TransmissionsNumber = int(inputRow['TransmissionsNumber'])
    IntervalTime = min(TIValueSet, key=lambda x: abs(x - prediction[index]))
    row.append(DelayValue)
    row.append(IDNodo)
    row.append(TTL)
    row.append(TransmissionPower)
    row.append(TransmissionsNumber)
    row.append(IntervalTime)
    output.append(row)

dataframeOutputStep4 = pd.DataFrame(output)
header = ['PDR', 'DeviceID', 'TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime']
dataframeOutputStep4.columns = header

print(dataframeOutputStep4)

dataframeOutputStep4.to_csv('Results/01 GaussinNB-PDR.csv', index=False)

'''
!zip -r ModelsGaussianNB.zip Models
!zip -r ResultsGaussianNB.zip Results
'''