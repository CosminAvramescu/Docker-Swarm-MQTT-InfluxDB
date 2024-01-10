from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import logging
from datetime import datetime
from json import loads

database = InfluxDBClient(host="influx_db", port=8086)
database_availables = database.get_list_database()
if {"name": "iot_db"} not in database_availables:
    database.create_database("iot_db")

database.switch_database("iot_db")

def on_connect(client, args, flags, rc):
    logging.info("MQTT connection completed!")
    mqtt_cl.subscribe("#")

def on_message(client, args, msg):
    logging.info(f"Received a message by topic [{msg.topic}]")
    
    location, station = msg.topic.split("/")
    data = loads(msg.payload)
    
    try:
        if "timestamp" not in data:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"Data timestamp is NOW")
        else:
            timestamp = str(datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S"))
            logging.info(f"Data timestamp is: {timestamp}")
        
        data_to_send = []
        for key, value in data.items():
            if type(value) == float or type(value) == int:
                data_to_send.append({
                    "measurement": f"{location}.{station}.{key}",
                    "tags": {
                        "location": location,
                        "station": station,
                        "sensor": key
                    },
                    "fields": {
                        "value": float(value)
                    },                    
                    "timestamp": timestamp
                })
                
                logging.info(f"{location}.{station}.{key} {value}")
                
        if data_to_send:
            database.write_points(data_to_send)
    except Exception as e:
        logging.error(f"Error in function on_message: {e}")
        
if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    
    mqtt_cl = mqtt.Client()
    mqtt_cl.on_connect = on_connect
    mqtt_cl.on_message = on_message
    try:
        mqtt_cl.connect(host="mqtt_broker", port=1883)
        mqtt_cl.loop_forever()
    except Exception as e:
        logging.error(f"Error in function __main__: {e}")
        mqtt_cl.disconnect()
        mqtt_cl.loop_stop()
        exit(1)