
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode
from app.models.item_model import ItemModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem


def get_todo_item(db: Session, todo_list_id: int, todo_item_id: int):

    return db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id,
    ).first()


def post_todo_item(db: Session, todo_list_id: int, new_todo_item: NewTodoItem):
    db_todo_item = ItemModel(
        list_id=todo_list_id,
        title=new_todo_item.title,
        description=new_todo_item.description,
        status=new_todo_item.status,
    )

    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)

    return db_todo_item


def put_todo_item(db: Session, todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem):
    """TODO項目を更新する
        db: データベースセッション
        todo_list_id: TODO項目が属するTODOリストのID
        todo_item_id: 更新するTODO項目のID
        update_todo_item: 更新するデータ
    Returns: 更新後のTODO項目のデータ.
    """
    db_todo_item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id,
    ).first()

    # 更新するフィールドが指定されている場合のみ更新
    if update_todo_item.title is not None:
        db_todo_item.title = update_todo_item.title

    if update_todo_item.description is not None:
        db_todo_item.description = update_todo_item.description

    if update_todo_item.due_at is not None:
        db_todo_item.due_at = update_todo_item.due_at

    # complete フラグが指定されている場合、status_code を更新
    if update_todo_item.complete is not None:
        if update_todo_item.complete:
            db_todo_item.status_code = TodoItemStatusCode.COMPLETED.value
        else:
            db_todo_item.status_code = TodoItemStatusCode.NOT_COMPLETED.value

    # 変更をコミットしてデータベースを更新
    db.commit()

    # 更新後のデータを再取得
    db.refresh(db_todo_item)
    return db_todo_item


def delete_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    """TODO項目を削除する.

    db: データベースセッション
    todo_list_id: TODO項目が属するTODOリストのID
    todo_item_id: 削除するTODO項目のID
     Returns:正常に削除できた場合はTrue
    """
    db_todo_item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id,
    ).first()

    # データベースからレコードを削除
    if db_todo_item:
        db.delete(db_todo_item)
        db.commit()
        return True
    return False


def get_todo_items(db: Session, todo_list_id: int):

    return db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id).all()
