import sys
import time
import adafruit_dht
import requests
import math
import random

pin = 17
sensor = adafruit_dht.DHT11(pin)
TOKEN = "BBFF-MwQ4pYB0m7dCfn8WB6QCf22X8j0QIl"  # Put your TOKEN here
DEVICE_LABEL = "sensor-temp-humidity"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here

def build_payload(variable_1, variable_2):
    payload = {VARIABLE_LABEL_1: variable_1,
               VARIABLE_LABEL_2: variable_2}
    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

    
    
def main():
    
        try:
            # Obtiene la humedad y la temperatura desde el sensor
            humedad = sensor.humidity
            temperatura = sensor.temperature

            # Imprime en la consola las variables temperatura y humedad con un decimal
            print('Temperatura={0:0.1f} C  Humedad={1:0.1f}%'.format(temperatura, humedad))
            payload = build_payload(temperatura, humedad)

            print("[INFO] Attemping to send data")
            post_request(payload)
            print("[INFO] finished")

        # Se ejecuta en caso de que falle alguna instruccion dentro del try
        except RuntimeError as error:
            # Imprime en pantalla el error
            print(error.args[0])
    


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)



