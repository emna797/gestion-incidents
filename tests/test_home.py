def test_home_page_accessible(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Incidents" in response.get_data(as_text=True)


def test_add_page_accessible(client):
    response = client.get("/incidents/add")
    assert response.status_code == 200
