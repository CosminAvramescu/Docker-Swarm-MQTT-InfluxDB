import paho.mqtt.client as mqtt
from json import dumps
import random
from datetime import datetime

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", port=1883)
    client.loop_start()

    n = 20
    while n > 0:
        data = {
            "BAT": random.randint(0, 100),
            "HUMID": random.randint(0, 100),
            "TEMP": random.randint(-20, 40)
        }
        
        if n%4 == 0:
            data['timestamp']=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data['status']="ok"

        station = random.choice(["station1", "station2", "station3"])
        client.publish("UPB/" + station, dumps(data))
        
        print(f"Data published on station {station}:")
        print(data)

        n -= 1
  
    client.disconnect()
    client.loop_stop()
    