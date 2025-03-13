import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.list_crud import get_todo_list, create_todo_list, update_todo_list, delete_todo_list
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList
from .models.item_model import ItemModel
from .models.list_model import ListModel

# APIRouterのインスタンスを作成
router = APIRouter(
    prefix="/lists",  # 共通のパス部分
    tags=["Todoリスト"],  # Swagger UIでのグループ化タグ
)

@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def read_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    """指定されたIDのTODOリストを取得する"""
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return db_item

@router.post("", response_model=ResponseTodoList)
def create_list(todo_list: NewTodoList, db: Session = Depends(get_db)):
    """TODOリストを新規作成する"""
    db_todo_list = create_todo_list(db, todo_list)
    return db_todo_list

@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def update_list(todo_list_id: int, todo_list: UpdateTodoList, db: Session = Depends(get_db)):
    """TODOリストを更新する"""
    db_todo_list = get_todo_list(db, todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    updated_todo_list = update_todo_list(db, todo_list_id, todo_list)
    return updated_todo_list

@router.delete("/{todo_list_id}")
def remove_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    """TODOリストを削除する"""
    db_todo_list = get_todo_list(db, todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    delete_todo_list(db, todo_list_id)
    return {}