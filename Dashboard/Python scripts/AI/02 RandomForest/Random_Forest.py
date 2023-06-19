## Imports

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from joblib import dump, load
import itertools

"""## Functions"""

def conversionMs(x):
    return round(x / 2000000, 3)

#DelayValues = [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5]
#PDRValues = [0.7, 0.8, 0.9, 1]

DelayValues = [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15]
PDRValues = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

IDNodos = [3]

TTLValues = [2,3,4,5]
TransmissionPowerValues = [1,3,6]
TransmissionNumberValues = [1,3,5]
IntervalTimeValues = [1,2,3,4,5]

"""## Dataset"""

# Caricare i dati di esempio
data_performance = pd.read_csv("parameters_performance.csv")
data_pdr =  pd.read_csv("parameters_pdr.csv")
data_performance['Delay'] = data_performance['Delay'].apply(conversionMs)
data_pdr['PDR'] = data_pdr['PDRReceived'] / data_pdr['PDRSend']
dataset = pd.merge(data_performance, data_pdr, on=['TTL', 'TransmissionPower', 'TransmissionsNumber', 'IntervalTime', 'DeviceID'])

"""## Random Forest model creation

### Random Forest model creation - Predictor of 5 variables

#### Delay - DeviceID
"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "DeviceID"]
output_cols = ["TTL", "TransmissionPower", "TransmissionsNumber", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/01 RandomForest-Delay.joblib')

"""#### PDR - DeviceID"""

# selezionare le colonne di input e di output
input_cols = ["PDR", "DeviceID"]
output_cols = ["TTL", "TransmissionPower", "TransmissionsNumber", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/02 RandomForest-PDR.joblib')

"""### Random Forest model creation - Predictor of 4 variables"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID"]
output_cols = ["TTL", "TransmissionPower", "TransmissionsNumber", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/03 RandomForest.joblib')

"""### Random Forest model cration - Predictor of 3 variables

#### Delay - PDR - DeviceID - TTL
"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL"]
output_cols = ["TransmissionPower", "TransmissionsNumber", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/04 RandomForest-TTL.joblib')

"""#### Delay - PDR - DeviceID - TransmissionPower"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TransmissionPower"]
output_cols = ["TTL", "TransmissionsNumber", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/05 RandomForest-TransmissionPower.joblib')

"""#### Delay - PDR - TransmissionsNumber"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TransmissionsNumber"]
output_cols = ["TTL", "TransmissionPower", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/06 RandomForest-TransmissionsNumber.joblib')

"""#### Delay - PDR - DeviceID - IntervalTime"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "IntervalTime"]
output_cols = ["TTL", "TransmissionPower", "TransmissionsNumber"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/07 RandomForest-IntervalTime.joblib')

"""### Random Forest model creation - Predictor of 2 variables

#### Delay - PDR - DeviceID- TTL - TransmissionPower
"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionPower"]
output_cols = ["TransmissionsNumber", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/08 RandomForest-TTL-TransmissionPower.joblib')

"""#### Delay - PDR - DeviceID - TTL - TransmissionsNumber"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionsNumber"]
output_cols = ["TransmissionPower", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/09 RandomForest-TTL-TransmissionsNumber.joblib')

"""#### Delay - PDR - DeviceID - TTL - IntervalTime"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL", "IntervalTime"]
output_cols = ["TransmissionPower", "TransmissionsNumber"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/10 RandomForest-TTL-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TransmissionPower - TransmissionsNumber"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TransmissionPower", "TransmissionsNumber"]
output_cols = ["TTL", "IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/11 RandomForest-TransmissionPower-TransmissionsNumber.joblib')

"""#### Delay - PDR - TransmissionPower - IntervalTimea"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TransmissionPower", "IntervalTime"]
output_cols = ["TTL",  "TransmissionsNumber"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/12 RandomForest-TransmissionPower-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TransmissionsNumber - IntervalTime"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TransmissionsNumber", "IntervalTime"]
output_cols = ["TTL", "TransmissionPower"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/13 RandomForest-TransmissionsNumber-IntervalTime.joblib')

"""### Random Forest model creation - Predictor of 1 variable

#### Delay - PDR - DeviceID - TTL - TransmissionPower - TransmissionsNumber
"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionPower", "TransmissionsNumber"]
output_cols = ["IntervalTime"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/14 RandomForest-TTL-TransmissionPower-TransmissionsNumber.joblib')

"""#### Delay - PDR - DeviceID - TTL - TransmissionPower - IntervalTime"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionPower", "IntervalTime"]
output_cols = ["TransmissionsNumber"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/15 RandomForest-TTL-TransmissionPower-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TTL - TransmissionsNumber - IntervalTime"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TTL", "TransmissionsNumber", "IntervalTime"]
output_cols = ["TransmissionPower"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/16 RandomForest-TTL-TransmissionsNumber-IntervalTime.joblib')

"""#### Delay - PDR - DeviceID - TransmissionPower - TransmissionsNumber - IntervalTime"""

# selezionare le colonne di input e di output
input_cols = ["Delay", "PDR", "DeviceID", "TransmissionPower", "TransmissionsNumber", "IntervalTime"]
output_cols = ["TTL"]

# dividi le colonne di input e di output
X = dataset[input_cols]
y = dataset[output_cols]

# applicare la Standard Scaler alle colonne di input
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# creare il modello di Decision Tree e addestrarlo
model = RandomForestClassifier(random_state=0)
model.fit(X_scaled, y)

# Salva il modello su file
dump(model, 'Models/17 RandomForest-TransmissionPower-TransmissionsNumber-IntervalTime.joblib')

"""## Prediction

### Prediction of 5 variables

#### Delay - DeviceID
"""

# Carica il modello addestrato
clf = load('Models/01 RandomForest-Delay.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, IDNodos))

output = []
for combination in combinations:
  DelayValue = combination[0]
  IDNodo = combination[1]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, IDNodo]])

  row = []
  row.append(DelayValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(prediction[0][2])
  row.append(prediction[0][3])
  output.append(row)

#print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/01 RandomForest-Delay.csv', index=False)

"""#### PDR - NodeID"""

# Carica il modello addestrato
clf = load('Models/02 RandomForest-PDR.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(PDRValues, IDNodos))

output = []
for combination in combinations:
  PDRValue = combination[0]
  IDNodo = combination[1]

  # Esegui la predizione
  prediction = clf.predict([[PDRValue, IDNodo]])

  row = []
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(prediction[0][2])
  row.append(prediction[0][3])
  output.append(row)

#print(output)
dataframeOutput = pd.DataFrame(output)
header = ['PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/02 RandomForest-PDR.csv', index=False)

"""### Prediction of 4 variables"""

# Carica il modello addestrato
clf = load('Models/03 RandomForest.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(prediction[0][2])
  row.append(prediction[0][3])
  output.append(row)

#print(output)
dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/03 RandomForest.csv', index=False)

"""### Prediction of 3 variables

#### Prediction of 3 variables - TTL
"""

# Carica il modello addestrato
clf = load('Models/04 RandomForest-TTL.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(prediction[0][2])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/04 RandomForest-TTL.csv', index=False)

"""#### Prediction of 3 variables - TransmissionPower"""

# Carica il modello addestrato
clf = load('Models/05 RandomForest-TransmissionPower.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TransmissionPowerValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TransmissionPowerValue = combination[3]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TransmissionPowerValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(TransmissionPowerValue)
  row.append(prediction[0][1])
  row.append(prediction[0][2])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/05 RandomForest-TransmissionPower.csv', index=False)

"""#### Prediction of 3 variables - TransmissionsNumber"""

# Carica il modello addestrato
clf = load('Models/06 RandomForest-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TransmissionNumberValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TransmissionsNumberValue = combination[3]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TransmissionsNumberValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(TransmissionsNumberValue)
  row.append(prediction[0][2])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/06 RandomForest-TransmissionsNumber.csv', index=False)

"""#### Prediction of 3 variables - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/07 RandomForest-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  IntervalTimeValue = combination[3]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, IntervalTimeValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(prediction[0][2])
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/07 RandomForest-IntervalTime.csv', index=False)

"""### Preditcion of 2 variables

#### Delay - PDR - DeviceID - TTL - TransmissionPower
"""

# Carica il modello addestrato
clf = load('Models/08 RandomForest-TTL-TransmissionPower.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues,TransmissionPowerValues ))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]
  TransmissionPowerValue = combination[4]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue, TransmissionPowerValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(TransmissionPowerValue)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/08 RandomForest-TTL-TransmissionPower.csv', index=False)

"""#### Delay - PDR - DeviceID- TTL - TransmissionsNumber"""

# Carica il modello addestrato
clf = load('Models/09 RandomForest-TTL-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues,TransmissionNumberValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]
  TransmissionsNumberValue = combination[4]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue, TransmissionsNumberValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(prediction[0][0])
  row.append(TransmissionsNumberValue)
  row.append(prediction[0][1])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/09 RandomForest-TTL-TransmissionsNumber.csv', index=False)

"""#### Delay - PDR - DeviceID - TTL - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/10 RandomForest-TTL-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues,IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]
  IntervalTimeValue = combination[4]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue, IntervalTimeValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/10 RandomForest-TTL-IntervalTime.csv', index=False)

"""#### Delay - PDR - DeviceID - TransmissionPower - TransmissionsNumber"""

# Carica il modello addestrato
clf = load('Models/11 RandomForest-TransmissionPower-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TransmissionPowerValues,TransmissionNumberValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TransmissionPowerValue = combination[3]
  TransimissionNumberValue = combination[4]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TransmissionPowerValue, TransimissionNumberValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(TransmissionPowerValue)
  row.append(TransimissionNumberValue)
  row.append(prediction[0][1])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/11 RandomForest-TransmissionPower-TransmissionsNumber.csv', index=False)

"""#### Delay - PDR - TransmissionPower - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/12 RandomForest-TransmissionPower-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TransmissionPowerValues,IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TransmissionPowerValue = combination[3]
  IntervalTimeValue = combination[4]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TransmissionPowerValue, IntervalTimeValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(TransmissionPowerValue)
  row.append(prediction[0][1])
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/12 RandomForest-TransmissionPower-IntervalTime.csv', index=False)

"""#### Delay - PDR - DeviceID - TransmissionsNumber - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/13 RandomForest-TransmissionsNumber-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TransmissionNumberValues,IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TransimissionNumberValue = combination[3]
  IntervalTimeValue = combination[4]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TransimissionNumberValue, IntervalTimeValue]])

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0][0])
  row.append(prediction[0][1])
  row.append(TransimissionNumberValue)
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/13 RandomForest-TransmissionsNumber-IntervalTime.csv', index=False)

"""### Preditcion of 1 variables

#### Delay - PDR - DeviceID - TTL - TransmissionPower - TransmissionsNumber
"""

# Carica il modello addestrato
clf = load('Models/14 RandomForest-TTL-TransmissionPower-TransmissionsNumber.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues, TransmissionPowerValues, TransmissionNumberValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]
  TransmissionPowerValue = combination[4]
  TransimissionNumberValue = combination[5]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue, TransmissionPowerValue, TransimissionNumberValue]])
  print(str(prediction))

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(TransmissionPowerValue)
  row.append(TransimissionNumberValue)
  row.append(prediction[0])
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/14 RandomForest-TransmissionsNumber-IntervalTime.csv', index=False)

"""#### Delay - PDR - DeviceID - TTL - TransmissionPower - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/15 RandomForest-TTL-TransmissionPower-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues, TransmissionPowerValues, IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]
  TransmissionPowerValue = combination[4]
  IntervalTimeValue = combination[5]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue, TransmissionPowerValue, IntervalTimeValue]])
  print(str(prediction))

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(TransmissionPowerValue)
  row.append(prediction[0])
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/15 RandomForest-TTL-TransmissionPower-IntervalTime.csv', index=False)

"""#### Delay - PDR - DeviceID - TTL - TransmissionsNumber - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/16 RandomForest-TTL-TransmissionsNumber-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TTLValues, TransmissionNumberValues, IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TTLValue = combination[3]
  TransimissionNumberValue = combination[4]
  IntervalTimeValue = combination[5]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TTLValue, TransimissionNumberValue, IntervalTimeValue]])
  print(str(prediction))

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(TTLValue)
  row.append(prediction[0])
  row.append(TransimissionNumberValue)
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/16 RandomForest-TTL-TransmissionsNumber-IntervalTime.csv', index=False)

"""#### Delay - PDR - DeviceID - TransmissionPower - TransmissionsNumber - IntervalTime"""

# Carica il modello addestrato
clf = load('Models/17 RandomForest-TransmissionPower-TransmissionsNumber-IntervalTime.joblib')

# Combinazione di tutti i parametri
combinations = list(itertools.product(DelayValues, PDRValues, IDNodos, TransmissionPowerValues, TransmissionNumberValues, IntervalTimeValues))

output = []
for combination in combinations:
  DelayValue = combination[0]
  PDRValue = combination[1]
  IDNodo = combination[2]
  TransmissionPowerValue = combination[3]
  TransimissionNumberValue = combination[4]
  IntervalTimeValue = combination[5]

  # Esegui la predizione
  prediction = clf.predict([[DelayValue, PDRValue, IDNodo, TransmissionPowerValue, TransimissionNumberValue, IntervalTimeValue]])
  print(str(prediction))

  row = []
  row.append(DelayValue)
  row.append(PDRValue)
  row.append(IDNodo)
  row.append(prediction[0])
  row.append(TransmissionPowerValue)
  row.append(TransimissionNumberValue)
  row.append(IntervalTimeValue)
  output.append(row)

dataframeOutput = pd.DataFrame(output)
header = ['Delay (ms)', 'PDR', 'NodeId', 'TTL', 'Potenza di trasmissione', 'Numero di trasmissioni', 'Intervallo tra le trasmissioni']
dataframeOutput.columns = header

# Esportare in un file CSV
dataframeOutput.to_csv('Results/17 RandomForest-TransmissionPower-TransmissionsNumber-IntervalTime.csv', index=False)

"""## Comandi
!zip -r Models.zip Models
!zip -r ResultsRandomForest.zip Results
"""