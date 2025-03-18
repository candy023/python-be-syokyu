from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import item_model, list_model

client = TestClient(app)

NUM_OF_RECORDS = 15


def test_get_todo_lists(db_session) -> None:
    """Station15合格判定テストコード."""
    db_todo_lists = [list_model.ListModel(
        title=f"station15_test_{str(i).zfill(3)}",
        description="A test record for station15.") for i in range(NUM_OF_RECORDS)]
    db_session.add_all(db_todo_lists)
    db_session.commit()
    for x in db_todo_lists:
        db_session.refresh(x)

    # ******************
    # テスト実行
    # ******************
    response = client.get("/lists")

    # ******************
    # 実行結果の検証開始
    # ******************

    # ステータスコードの確認
    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()

    actual_data_ids = sorted([x["id"] for x in response_body])
    expected_data_ids = sorted([x.id for x in db_todo_lists])
    assert actual_data_ids == expected_data_ids


def test_get_todo_items(db_session) -> None:
    """Station15合格判定テストコード."""
    db_todo_lists = [list_model.ListModel(
        title=f"station15_test_{str(i).zfill(3)}",
        description="A test record for station15.") for i in range(NUM_OF_RECORDS)]
    db_session.add_all(db_todo_lists)
    db_session.commit()
    for x in db_todo_lists:
        db_session.refresh(x)

    todo_list_id = db_todo_lists[0].id
    db_todo_items = [item_model.ItemModel(
        todo_list_id=todo_list_id,
        title=f"station15_test_{str(i).zfill(3)}",
        description="A test record for station15.", status_code=1) for i in range(NUM_OF_RECORDS)]
    db_session.add_all(db_todo_items)
    db_session.commit()
    for x in db_todo_items:
        db_session.refresh(x)

    # ******************
    # テスト実行
    # ******************
    todo_list_id = db_todo_lists[0].id
    response = client.get(f"/lists/{todo_list_id}/items")

    # ******************
    # 実行結果の検証開始
    # ******************

    # ステータスコードの確認
    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()

    actual_data_ids = sorted([x["id"] for x in response_body])
    expected_data_ids = sorted([x.id for x in db_todo_items])
    assert actual_data_ids == expected_data_ids
