import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud.item_crud import get_todo_item, create_todo_item, update_todo_item, delete_todo_item
from app.crud.list_crud import get_todo_list
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem

# APIRouterのインスタンスを作成
router = APIRouter(
    prefix="/lists/{todo_list_id}/items",  # 共通のパス部分（パスパラメータも含む）
    tags=["Todo項目"],  
)

@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def read_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    """指定されたIDのTODO項目を取得する"""
    # TODOリストの存在確認
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    # TODO項目の取得
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    return db_item

@router.post("/{todo_item_id}", response_model=ResponseTodoItem)
def create_item(todo_list_id: int, todo_item: NewTodoItem, db: Session = Depends(get_db)):
    """TODO項目を新規作成する"""
    # TODOリストの存在確認
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    # TODO項目の作成
    db_todo_item = create_todo_item(db, todo_list_id, todo_item)
    return db_todo_item

@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def update_item(todo_list_id: int, todo_item_id: int, todo_item: UpdateTodoItem, db: Session = Depends(get_db)):
    """TODO項目を更新する"""
    # TODOリストの存在確認
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    # TODO項目の存在確認
    db_todo_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    # TODO項目の更新
    updated_todo_item = update_todo_item(db, todo_list_id, todo_item_id, todo_item)
    return updated_todo_item

@router.delete("/{todo_item_id}")
def remove_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    """TODO項目を削除する"""
    # TODOリストの存在確認
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    
    # TODO項目の存在確認
    db_todo_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    # TODO項目の削除
    delete_todo_item(db, todo_list_id, todo_item_id)
    return {}