from pydantic import BaseModel

class MapDataIn(BaseModel):
    msg_id: str
    ship_id: str
    nama_kapal: str
    latitude: float
    longitude: float
    yaw: float
    pitch: float
    roll: float
    RSSI: int