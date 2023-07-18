from httpx import AsyncClient

async def test_auth(ac: AsyncClient, test_user):
    response = await ac.post("/auth/sign-in/", data=test_user)
    assert response.status_code == 200

async def test_user(ac: AsyncClient, test_user):
    response = await ac.get("/auth/user/")
    assert response.status_code == 200
    assert response.json()["id"] == 2