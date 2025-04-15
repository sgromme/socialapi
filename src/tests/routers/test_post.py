import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    """
    Helper function to create a post using the async client.
    """
    response = await async_client.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    """
    Helper function to create a comment using the async client.
    """
    response = await async_client.post(
        "/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()


@pytest.fixture()
async def created_post(
    async_client: AsyncClient,
):  # async_client comes from tests\conftest.py
    return await create_post("Test post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test post"

    response = await async_client.post("/post", json={"body": body})

    assert response.status_code == 201
    assert {"id": 0, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_no_body(async_client: AsyncClient):
    """Test creating a post without a body."""
    response = await async_client.post("/post", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    """Test getting all posts."""
    response = await async_client.get("/posts")

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    """Test creating a comment."""
    body = "Test comment"

    response = await async_client.post(
        "/comment", json={"body": body, "post_id": created_post["id"]}
    )

    assert response.status_code == 201
    assert {
        "id": 0,
        "body": body,
        "post_id": created_post["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    """Test getting comments on a post."""
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_empty_post(
    async_client: AsyncClient, created_post: dict
):
    """Test getting comments on a post."""
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    """Test getting post with comments."""
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == 200
    assert response.json() == {"post": created_post, "comments": [created_comment]}


@pytest.mark.anyio
async def test_get_post_that_doesnt_exist_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    """Test getting post with comments."""
    response = await async_client.get("/post/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
