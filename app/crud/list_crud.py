
from sqlalchemy.orm import Session

from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList

  #   TODOリスト一覧取得 API(15)


def get_todo_lists(db: Session):
    return db.query(ListModel).all()


def get_todo_list(db: Session, todo_list_id: int):
    # - 取得した DB データをそのまま返却する関数としてください。
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()


def post_todo_list(db: Session, new_todo_list: NewTodoList):
    db_todo_list = ListModel(
      title=new_todo_list.title,
      description=new_todo_list.description,
    )

    db.add(db_todo_list)
    db.commit()
    db.refresh(db_todo_list)
    # 登録した DB データをそのまま返却する関数としてください。
    return db_todo_list
    # 　-TODOリスト更新処理です。


def put_todo_list(db: Session, todo_list_id: int, todo_list: UpdateTodoList):
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()

    # 更新するフィールドが指定されている場合のみ更新(重要)
    if todo_list.title is not None:
        db_todo_list.title = todo_list.title

    if todo_list.description is not None:
        db_todo_list.description = todo_list.description
     # 変更をコミットしてデータベースを更新
    db.commit()

    # 更新後のデータを再取得
    db.refresh(db_todo_list)

    return db_todo_list

    # 　-TODOリスト削除処理です。


def delete_todo_list(db: Session, todo_list_id: int):
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()

    if db_todo_list:
        db.delete(db_todo_list)
        db.commit()
        return True
    # 削除処理の場合、 DB のデータを返却するのではなく、正常に削除できたか否かを返却するようにしましょう。
    return False
