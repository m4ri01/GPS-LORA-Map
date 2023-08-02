from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.map_data.models import data_lora
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.map_data.schema import MapDataIn
from uuid import UUID

router = APIRouter(
    tags=["list data"],
    prefix="/list"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/",response_class=HTMLResponse)
async def show_data_list(request:Request):
    query = data_lora.select()
    data = await db.fetch_all(query)
    return templates.TemplateResponse("view_list/index.html",{"request":request,"data":data})

@router.post("/")
async def add_data(data:MapDataIn):
    print(data)
    query = data_lora.insert().values(
        msg_id = data.msg_id,
        ship_id = data.ship_id,
        nama_kapal = data.nama_kapal,
        latitude = data.latitude,
        longitude = data.longitude,
        yaw = data.yaw,
        pitch = data.pitch,
        roll = data.roll
    )
    await db.execute(query)
    return {"message":"data berhasil ditambahkan"}
