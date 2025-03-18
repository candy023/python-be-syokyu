import os

# 2. サードパーティライブラリのインポート
from fastapi import FastAPI

from app.routers import item_router, list_router

# 3. ローカルアプリケーション/ライブラリのインポート

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


@app.get("/echo", tags=["Hello"])
def get_hello():
    return {"Message": "Hello FastAPI!"}


# API4 Helthを追加
@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}


# TODOリスト関連のエンドポイント
app.include_router(list_router.router)
# TODO項目関連のエンドポイント
app.include_router(item_router.router)
