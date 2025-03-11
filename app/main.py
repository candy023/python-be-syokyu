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


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

#API4 Helthを追加
@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}

# API6 TodoItemの新規作成    
@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    """指定されたIDのTODOリストを取得する"""
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
   # if db_item is None:
   #  raise HTTPException(status_code=404, detail="Todo list not found")
    
    # レスポンスを明示的に辞書形式で返す
    return {
        "id": db_item.id,
        "title": db_item.title,
        "description": db_item.description,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at
    }
 #課題7   
# 修正後（正しいコード）:
@app.post("/lists", tags=["Todoリスト"])
def post_todo_list(todo_list: NewTodoList, db: Session = Depends(get_db)):
 
    db_todo_list = ListModel( 
                             
      title=todo_list.title,
      description=todo_list.description
    )
        
    # データベースにデータを追加
    db.add(db_todo_list)
    db.commit()
    db.refresh(db_todo_list)
        
        # 登録されたデータを返却
    return {
            "id": db_todo_list.id,
            "title": db_todo_list.title,
            "description": db_todo_list.description,
            "created_at": db_todo_list.created_at,
            "updated_at": db_todo_list.updated_at
        }
#API8 TodoItemの更新    
@app.put("/lists/{todo_list_id}", tags=["Todoリスト"])
def put_todo_list(todo_list_id: int, todo_list: UpdateTodoList, db: Session = Depends(get_db)):
    # 既存のTODOリストを取得
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
    # 指定されたIDのTODOリストが存在しない場合は404エラー
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    # 更新するフィールドが指定されている場合のみ更新(重要)
    if todo_list.title is not None:
        db_todo_list.title = todo_list.title
    
    if todo_list.description is not None:
        db_todo_list.description = todo_list.description
    
    # 変更をコミットしてデータベースを更新
    db.commit()
    
    # 更新後のデータを再取得
    db.refresh(db_todo_list)
    
    # 更新されたデータを返却
    return {
        "id": db_todo_list.id,
        "title": db_todo_list.title,
        "description": db_todo_list.description,
        "created_at": db_todo_list.created_at,
        "updated_at": db_todo_list.updated_at
    }

#API9 TodoItemの削除
@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int,db: Session = Depends(get_db)):
      # 削除対象のTODOリストを取得
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    # データベースからレコードを削除
    db.delete(db_todo_list)
    db.commit()
    return{}

#TODO項目取得 API を作成しよう
@app.get("/lists/{todo_list_id}/items/{todo_item_id}",tags=["Todo項目"])
def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    """指定されたIDのTODOリストを取得する"""
    db_item = db.query(ItemModel).filter(ItemModel.id == todo_item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    # レスポンスを明示的に辞書形式で返す
    return {
        "id": db_item.id,
        "todo_list_id": db_item.todo_list_id,
        "title": db_item.title,
        "description": db_item.description,
        "status_code": db_item.status_code,
        "due_at": db_item.due_at,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at
    }
    
@app.post("/lists/{todo_list_id}/items", tags=["Todo項目"])
def post_todo_item(todo_list_id: int, todo_item: NewTodoItem, db: Session = Depends(get_db)):
    do_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
    db_todo_item = ItemModel(
        todo_list_id=todo_list_id,
        title=todo_item.title,
        description=todo_item.description,
        due_at=todo_item.due_at
    )
    db_todo_item.status_code = TodoItemStatusCode.NOT_COMPLETED.value
    
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    
    return {
        "id": db_todo_item.id,
        "todo_list_id": db_todo_item.todo_list_id,
        "title": db_todo_item.title,
        "description": db_todo_item.description,
        "status_code": db_todo_item.status_code,
        "due_at": db_todo_item.due_at,
        "created_at": db_todo_item.created_at,
        "updated_at": db_todo_item.updated_at
    }
    
@app.put("/lists/{todo_list_id}/items/{todo_item_id}",tags=["Todo項目"])
def put_todo_item(todo_list_id: int, todo_item_id: int, todo_item: UpdateTodoItem, db: Session = Depends(get_db)):
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
    db_todo_item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()
    
    # 更新するフィールドが指定されている場合のみ更新(重要)
    if todo_item.title is not None:
        db_todo_item.title = todo_item.title
    
    if todo_item.description is not None:
        db_todo_item.description = todo_item.description
    
    if todo_item.due_at is not None:
        db_todo_item.due_at = todo_item.due_at
    
    # complete フラグが指定されている場合、status_code を更新
    if todo_item.complete is not None:
        if todo_item.complete:
            db_todo_item.status_code = TodoItemStatusCode.COMPLETED.value
        else:
            db_todo_item.status_code = TodoItemStatusCode.NOT_COMPLETED.value
    # 重要部分ここまで
    # 変更をコミットしてデータベースを更新
    db.commit()
    
    # 更新後のデータを再取得
    db.refresh(db_todo_item)
    
    # 更新されたデータを返却
    return {
        "id": db_todo_item.id,
        "todo_list_id": db_todo_item.todo_list_id,
        "title": db_todo_item.title,
        "description": db_todo_item.description,
        "status_code": db_todo_item.status_code,
        "due_at": db_todo_item.due_at,
        "created_at": db_todo_item.created_at,
        "updated_at": db_todo_item.updated_at
    }
    
@app.delete("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todo項目"])
def delete_todo_item(todo_list_id: int,todo_item_id: int,db: Session = Depends(get_db)):
    
       
    # 指定されたTODOリストが存在するか確認
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
      # 指定されたTODO項目が存在し、かつ指定されたTODOリストに属しているか確認
    db_todo_item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()
    # データベースからレコードを削除
    db.delete(db_todo_item)
    db.commit()
    return{}
