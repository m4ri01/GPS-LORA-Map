import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.map_data.routers import router as map_data_router
from fastapi.staticfiles import StaticFiles
from src.map_data.models import data_lora
from src.database import db
from fastapi.templating import Jinja2Templates
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import asyncio
import json
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.mount("/templates", StaticFiles(directory="src/templates"), name="templates")

templates = Jinja2Templates(directory="src/templates")

MQTT_BROKER_HOST = "188.166.242.227"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "/ppns/monitor_kapal"

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        payload_split = payload.split("&")
        # print(payload_split)
        dict_send = {}
        for p in payload_split:
            p = p.replace('"',"")
            data_split = p.split("=")
            if data_split[0] == "latitude" or data_split[0] == "longitude" or data_split[0] == "yaw" or data_split[0] == "pitch" or data_split[0] == "roll":
                dict_send[data_split[0]] = float(data_split[1]) 
            elif data_split[0] == "rssi":
                dict_send[data_split[0].upper()] = int(data_split[1])

            else:
                dict_send[data_split[0]] = data_split[1]
            if data_split[0] == "ship_id" and data_split[1] == "1":
                # print("a")
                dict_send["RSSI"] = 0

        # print(dict_send)  
        # result = requests.post("http://localhost:5555/list",json=dict_send)
        # print(result.status_code)
        # publish.single("map_realtime", json.dumps(dict_send), hostname=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT)
    except Exception as e:
        print("error {}".format(e))

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

async def connect_mqtt():
    await asyncio.sleep(1)  # Wait for 1 second to allow FastAPI to start properly
    mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    mqtt_client.subscribe(MQTT_TOPIC)
    mqtt_client.loop_start()

def disconnect_mqtt():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

@app.on_event("startup")
async def startup():
    await db.connect()
    await connect_mqtt()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    disconnect_mqtt()

@app.get("/")
async def redirect():
    response = RedirectResponse(url='/list/map')
    return response

app.include_router(map_data_router)

if __name__ == "__main__":
    uvicorn.run("main:app",port=5555,log_level="info",reload=True,host="0.0.0.0")
