import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .dependencies import get_db
from app.const import TodoItemStatusCode
from .models.item_model import ItemModel
from .models.list_model import ListModel
from app.routers import list_router, item_router 

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)


if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


#API4 Helthを追加
@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}
# TODOリスト関連のエンドポイント
app.include_router(list_router.router)
# TODO項目関連のエンドポイント
app.include_router(item_router.router)
