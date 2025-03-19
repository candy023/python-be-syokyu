
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.item_crud import delete_todo_item, get_todo_item, get_todo_items, post_todo_item, put_todo_item
from app.dependencies import get_db
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem

# APIRouterのインスタンスを作成
router = APIRouter(
    prefix="/lists/{todo_list_id}/items",  # 共通のパス部分パスパラメータも含む）
    tags=["Todo項目"],
)


@router.get("", response_model=list[ResponseTodoItem])
def read_todo_items(todo_list_id: int, db: Annotated[Session, Depends(get_db)]):
    """特定のTODOリストに属する全てのTODO項目を取得する."""
    return get_todo_items(db, todo_list_id)


@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def get_item(todo_list_id: int, todo_item_id: int, db: Annotated[Session, Depends(get_db)]):
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_item


@router.post("", response_model=ResponseTodoItem)
def post_item(todo_list_id: int, todo_item: NewTodoItem, db: Annotated[Session, Depends(get_db)]):
    # リストの存在確認を追加
    from app.crud.list_crud import get_todo_list
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
   
    # 更新: create_todo_item → post_todo_item
    return post_todo_item(db, todo_list_id, todo_item)


@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_item(todo_list_id: int, todo_item_id: int, todo_item: UpdateTodoItem, db: Annotated[Session, Depends(get_db)]):
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")

    # 更新: update_todo_item → put_todo_item
    return put_todo_item(db, todo_list_id, todo_item_id, todo_item)


@router.delete("/{todo_item_id}")
def delete_item(todo_list_id: int, todo_item_id: int, db: Annotated[Session, Depends(get_db)]):
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")

    delete_todo_item(db, todo_list_id, todo_item_id)
    return {}
