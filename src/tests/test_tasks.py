import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post("/tasks/", json={"title": "Test task", "description": "desc"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "desc"
    assert "id" in data


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    create_resp = await client.post("/tasks/", json={"title": "To delete", "description": "tmp"})
    task_id = create_resp.json()["id"]

    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted"}

    get_resp = await client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):

    create_resp = await client.post("/tasks/", json={"title": "Old title", "description": "Old desc"})
    task_id = create_resp.json()["id"]


    update_resp = await client.put(f"/tasks/{task_id}", json={"title": "New title"})
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["title"] == "New title"
    assert data["description"] == "Old desc"  # не меняли


@pytest.mark.asyncio
async def test_get_nonexistent_task(client: AsyncClient):

    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/tasks/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
