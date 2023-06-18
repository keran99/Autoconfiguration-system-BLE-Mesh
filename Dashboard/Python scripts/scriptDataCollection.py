import mysql.connector
from paho.mqtt import client as mqtt_client
import itertools


mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

broker = ''
port = 1883
topic = "/sendPerformnce"
topic2 = '/sendPDR'
topic3 = '/getNewParameters'
client_id = 'pythonScript'
username = ''
password = ''


TTLValue = [2,3,4,5]
TransmissionPower = [1,3,6]
TransmissionsNumber = [1,3,5]
IntervalTime= [1,2,3,4,5]
Combinations = []
index = 0
count = 0

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, setTopic, value):
    result = client.publish(setTopic, value)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print("Send")
    else:
        print("Failed")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        global count
        global index

        if msg.topic == "/sendPerformnce":
            print("SEND PERFORMANCE")
            Performances = msg.payload.decode().split("-")
            nodeID = int(Performances[0])
            TTLResidue = int(Performances[1])
            Delay = int(Performances[2])

            mycursor = mydb.cursor()
            sql = "INSERT INTO parameters_performance (DeviceID, TTL, TransmissionPower, TransmissionsNumber, IntervalTime, TTLResidue, Delay) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nodeID, Combinations[index][0], Combinations[index][1], Combinations[index][2], Combinations[index][3],TTLResidue,Delay)
            mycursor.execute(sql, val)
            mydb.commit()
        
        elif msg.topic == "/sendPDR":
            print("SEND PDR")
            print(msg.payload.decode())
            PDRVal = msg.payload.decode().split("-")
            PDRSend = int(PDRVal[0])
            PDRReceived = int(PDRVal[1])
            print(PDRSend)
            print(PDRReceived)
            mycursor = mydb.cursor()
            sql = "INSERT INTO parameters_pdr (TTL, TransmissionPower, TransmissionsNumber, IntervalTime, PDRSend, PDRReceived) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Combinations[index][0], Combinations[index][1], Combinations[index][2], Combinations[index][3], PDRSend, PDRReceived)
            mycursor.execute(sql, val)
            mydb.commit()
        
        elif msg.topic == "/getNewParameters":
            try:
                index += 1
                print(index)
                CombinazioneInvio = str(Combinations[index][0]) + ":" + str(Combinations[index][1]) + ":" +  str(Combinations[index][2]) + ":" + str(Combinations[index][3])
                publish(client, "/setAllParameters",CombinazioneInvio)
            except:
                print("FINITO")

    client.subscribe(topic)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.on_message = on_message

def run():
    result = list(itertools.product(TTLValue, TransmissionPower, TransmissionsNumber, IntervalTime))
    for element in result:
        Combinations.append(element)
    print(len(Combinations))

    client = connect_mqtt()
    subscribe(client)

    CombinazioneInvio = str(Combinations[index][0]) + ":" + str(Combinations[index][1]) + ":" +  str(Combinations[index][2]) + ":" + str(Combinations[index][3])
    publish(client, "/setAllParameters",CombinazioneInvio)

    client.loop_forever()    
   

if __name__ == '__main__':
    run()
