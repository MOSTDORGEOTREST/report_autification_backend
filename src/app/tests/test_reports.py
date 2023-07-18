from httpx import AsyncClient

async def test_report_create(ac: AsyncClient):
    response = await ac.post(
        "/reports/",
        json={
            'object_number': 'pytest',
            'laboratory_number': 'pytest',
            'test_type': 'pytest',
            'data': {
                'pytest': 'pytest'
            },
            'active': True}
    )
    assert response.status_code == 200

async def test_report_update(ac: AsyncClient):
    response = await ac.put(
        "/reports/",
        params={'id': '1b71da0735b27f8104bcd46a2082cc8f362b477f'},
        json={
            'data': {
                'pytest_update': 'pytest_update'
            },
        'active': True},
    )
    assert response.status_code == 200

async def test_report_delete(ac: AsyncClient):
    response = await ac.delete("/reports/", params={'id': '1b71da0735b27f8104bcd46a2082cc8f362b477f'})
    assert response.status_code == 204