import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import item_model, list_model

client = TestClient(app)

NUM_OF_RECORDS = 15


@pytest.mark.parametrize(("per_page", "page"), [
    (10, 1),
    (10, 2),
])
def test_get_todo_lists_pagination(per_page: int, page: int, db_session) -> None:
    """Station18合格判定テストコード."""
    db_todo_lists = [list_model.ListModel(
        title=f"station18_test_{str(i).zfill(3)}",
        description="A test record for station18.") for i in range(NUM_OF_RECORDS)]
    db_session.add_all(db_todo_lists)
    db_session.commit()
    for x in db_todo_lists:
        db_session.refresh(x)

    # ******************
    # テスト実行
    # ******************
    response = client.get("/lists", params={
        "per_page": per_page,
        "page": page,
    })

    # ******************
    # 実行結果の検証開始
    # ******************
    # ステータスコードの確認
    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()
    assert len(response_body) == per_page if per_page * page <= NUM_OF_RECORDS else NUM_OF_RECORDS % per_page

    actual_data_ids = sorted([x["id"] for x in response_body])
    expected_data_ids = sorted([x.id for x in db_todo_lists])

    idx_from = per_page * (page - 1)
    idx_to = per_page * page
    assert actual_data_ids == expected_data_ids[idx_from:idx_to]


@pytest.mark.parametrize(("per_page", "page"), [
    (10, 1),
    (10, 2),
])
def test_get_todo_items_pagination(per_page: int, page: int, db_session) -> None:
    """Station18合格判定テストコード."""
    db_todo_list = list_model.ListModel(
        title="station18_test_001",
        description="A test record for station18.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    todo_list_id = db_todo_list.id
    db_todo_items = [item_model.ItemModel(
        todo_list_id=todo_list_id,
        title=f"station18_test_{str(i).zfill(3)}",
        description="A test record for station18.", status_code=1) for i in range(NUM_OF_RECORDS)]
    db_session.add_all(db_todo_items)
    db_session.commit()
    for x in db_todo_items:
        db_session.refresh(x)

    # ******************
    # テスト実行
    # ******************
    todo_list_id = db_todo_list.id
    response = client.get(f"/lists/{todo_list_id}/items", params={
        "per_page": per_page,
        "page": page,
    })

    # ******************
    # 実行結果の検証開始
    # ******************

    # ステータスコードの確認
    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()
    assert len(response_body) == per_page if per_page * page <= NUM_OF_RECORDS else NUM_OF_RECORDS % per_page

    actual_data_ids = sorted([x["id"] for x in response_body])
    expected_data_ids = sorted([x.id for x in db_todo_items])

    idx_from = per_page * (page - 1)
    idx_to = per_page * page
    assert actual_data_ids == expected_data_ids[idx_from:idx_to]
