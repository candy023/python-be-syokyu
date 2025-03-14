
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.list_crud import delete_todo_list, get_todo_list, post_todo_list, put_todo_list
from app.dependencies import get_db
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

# APIRouterのインスタンスを作成
router = APIRouter(
    prefix="/lists",  # 共通のパス部分
    tags=["Todoリスト"],  # Swagger UIでのグループ化タグ
)


@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_list(todo_list_id: int, db: Session = Depends(get_db)):
    """指定されたIDのTODOリストを取得する"""
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return db_item


@router.post("", response_model=ResponseTodoList)
def post_list(todo_list: NewTodoList, db: Session = Depends(get_db)):
    """TODOリストを新規作成する"""

    db_todo_list = post_todo_list(db, todo_list)
    return db_todo_list


@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_list(todo_list_id: int, todo_list: UpdateTodoList, db: Session = Depends(get_db)):
    """TODOリストを更新する"""
    db_todo_list = get_todo_list(db, todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")

    # 更新: update_todo_list → put_todo_list
    updated_todo_list = put_todo_list(db, todo_list_id, todo_list)
    return updated_todo_list


@router.delete("/{todo_list_id}")
def delete_list(todo_list_id: int, db: Session = Depends(get_db)):
    """TODOリストを削除する"""
    db_todo_list = get_todo_list(db, todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")

    delete_todo_list(db, todo_list_id)
    return {}
