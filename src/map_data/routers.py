from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.map_data.models import data_lora
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.map_data.schema import MapDataIn
from sqlalchemy import desc, select, func, and_
from uuid import UUID

router = APIRouter(
    tags=["list data"],
    prefix="/list"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/",response_class=HTMLResponse)
async def show_data_list(request:Request):
    query = data_lora.select().order_by(desc(data_lora.c.created_at))
    data = await db.fetch_all(query)
    return templates.TemplateResponse("view_list/index.html",{"request":request,"data":data})

@router.get("/map",response_class=HTMLResponse)
async def show_map(request:Request):
    ship_ids = ['1', '2', '3', '4']
    latest_created_at_subquery = (
        select(
            data_lora.c.ship_id,
            func.max(data_lora.c.created_at).label("max_created_at")
        )
        .where(data_lora.c.ship_id.in_(ship_ids))
        .group_by(data_lora.c.ship_id)
        .alias("latest_created_at_subquery")
    )
    latest_data_query = (
        select(data_lora)
        .join(
            latest_created_at_subquery,
            and_(
                data_lora.c.ship_id == latest_created_at_subquery.c.ship_id,
                data_lora.c.created_at == latest_created_at_subquery.c.max_created_at,
            ),
        )
    )
    latest_data = await db.fetch_all(latest_data_query)
    # print(latest_data)
    return templates.TemplateResponse("view_map/index.html",{"request":request,"data_map":latest_data})

@router.post("/")
async def add_data(data:MapDataIn):
    # print(data)
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
