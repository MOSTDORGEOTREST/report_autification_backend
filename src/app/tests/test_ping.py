from httpx import AsyncClient

async def test_ping(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {'massage': 'successful'}