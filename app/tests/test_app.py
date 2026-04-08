def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

def test_404(client):
    response = client.get("/thispagedoesnotexist")
    assert response.status_code == 404

def test_protected_route_requires_login(client):
    response = client.get("/admin/users")
    assert response.status_code in (301, 302, 401, 403, 404)
