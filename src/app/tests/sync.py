#from starlette.testclient import TestClient

#@pytest.fixture(scope="session")
#def test_app():
#    client = TestClient(app)
#    yield client

#def test_login(test_app, test_user):
#    with test_app.post("/auth/sign-in/", data=test_user) as response:
#        assert response.status_code == 200
#        user = test_app.get("/auth/user/")
#        assert user.status_code == 200
#        assert user.json()["id"] == 2