import paho.mqtt.publish as publish
import time
import random
import threading


MSG_ID_TOWER1 = 2290
MSG_ID_TOWER2 = 573
MSG_ID_TOWER3 = 1026
MSG_ID_SHIP = 856

def generate_data(msg_id, ship_id, nama_kapal, latitude, longitude, yaw, pitch, roll,rssi):
    if rssi !=0:
        message = f"msg_id={msg_id}&ship_id={ship_id}&nama_kapal={nama_kapal}&latitude={latitude}&longitude={longitude}&yaw={yaw}&pitch={pitch}&roll={roll}&rssi={rssi}"
    else:
        message = f"msg_id={msg_id}&ship_id={ship_id}&nama_kapal={nama_kapal}&latitude={latitude}&longitude={longitude}&yaw={yaw}&pitch={pitch}&roll={roll}"
    return message

def random_sleep(min_seconds, max_seconds):
    sleep_duration = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_duration)

def publish_mqtt(message):
    publish.single("/ppns/monitor_kapal", message, hostname="188.166.242.227")

def generate_imu():
    pitch = round(random.uniform(-3,3),2)
    roll = round(random.uniform(-3,3),2)
    yaw = round(random.uniform(-3,3),2)
    return pitch, roll, yaw

def generate_rssi_greater():
    rssi = random.randint(-105,-95)
    return rssi

def generate_rssi_less():
    rssi = random.randint(-120,-106)
    return rssi

def generate_rssi():
    rssi = random.randint(-120,-100)
    return rssi

def generate_longlat(tower):
    if tower == 2:
        latitude = random.uniform(-7.2786519, -7.2788519)
        longitude = random.uniform(112.7934876, 112.7938876)
        return latitude, longitude
    elif tower == 3:
        latitude = random.uniform(-7.278951,-7.2792019)
        longitude = random.uniform(112.7934876, 112.7938876)
        return latitude, longitude

def thread_tower1():
    global MSG_ID_TOWER1
    while True:
        pitch, roll, yaw = generate_imu()
        message = generate_data(MSG_ID_TOWER1, 1, "Kapal%201", 0.00, 0.00, pitch,roll,yaw, 0)       
        MSG_ID_TOWER1 += 1 
        publish_mqtt(message)
        random_sleep(1,3)


def thread_tower2(rssi_state):
    global MSG_ID_TOWER2
    while True:
        if rssi_state == 1:
            rssi = generate_rssi_greater()
        else:
            rssi = generate_rssi_less()
        pitch, roll, yaw = generate_imu()
        message = generate_data(MSG_ID_TOWER2, 2, "Kapal%202", 0.00, 0.00, pitch,roll,yaw, rssi)       
        MSG_ID_TOWER2 += 1 
        publish_mqtt(message)
        random_sleep(1,3)

def thread_tower3(rssi_state):
    global MSG_ID_TOWER3
    while True:
        if rssi_state == 1:
            rssi = generate_rssi_greater()
        else:
            rssi = generate_rssi_less()
        pitch, roll, yaw = generate_imu()
        message = generate_data(MSG_ID_TOWER3, 3, "Kapal%203", 0.00, 0.00, pitch,roll,yaw, rssi)       
        MSG_ID_TOWER3 += 1 
        publish_mqtt(message)
        random_sleep(1,3)

def thread_ship(tower):
    global MSG_ID_SHIP
    while True:
        latitude, longitude = generate_longlat(tower)
        pitch, roll, yaw = generate_imu()
        rssi = generate_rssi()
        message = generate_data(MSG_ID_SHIP, 4, "Kapal%204", latitude, longitude, pitch,roll,yaw, rssi)       
        MSG_ID_SHIP += 1 
        publish_mqtt(message)
        random_sleep(1,3)

if __name__ == "__main__":
    condition = 3 # 2 or 3
    tower1_thread = threading.Thread(target=thread_tower1)
    if condition == 2:
        tower2_thread = threading.Thread(target=thread_tower2, args=(1,))
        tower3_thread = threading.Thread(target=thread_tower3, args=(0,))
        ship_thread = threading.Thread(target=thread_ship, args=(2,))
    elif condition == 3:
        tower2_thread = threading.Thread(target=thread_tower2, args=(0,))
        tower3_thread = threading.Thread(target=thread_tower3, args=(1,))
        ship_thread = threading.Thread(target=thread_ship, args=(3,))
    tower1_thread.start()
    tower2_thread.start()
    tower3_thread.start()
    ship_thread.start()