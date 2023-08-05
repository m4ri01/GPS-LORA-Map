from sqlalchemy import Table, Column, String, DateTime, Date, Interval, ForeignKey, Numeric, Float, Integer
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import MetaData

metadata = MetaData()
data_lora = Table(
    "data_lora",
    metadata,
    Column("id", GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL),
    Column("msg_id", String(255), nullable=False),
    Column("ship_id", String(255), nullable=False),
    Column("nama_kapal", String(255), nullable=False),
    Column("latitude", Numeric(precision=10, scale=8), nullable=False),
    Column("longitude", Numeric(precision=11, scale=8), nullable=False),
    Column("yaw",Float, nullable=False),
    Column("pitch",Float, nullable=False),
    Column("roll",Float, nullable=False),
    Column("RSSI",Integer,nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now(), nullable=True),
)