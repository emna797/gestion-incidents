def creer_incident(client, titre="Projecteur en panne"):
    return client.post(
        "/incidents/add",
        data={
            "titre": titre,
            "description": "Ne s'allume plus",
            "lieu": "Salle B12",
            "priorite": "Élevée",
        },
        follow_redirects=True,
    )


def test_ajout_incident(client):
    response = creer_incident(client)
    assert response.status_code == 200
    assert "Projecteur en panne" in response.get_data(as_text=True)


def test_liste_incidents(client):
    creer_incident(client, "Incident A")
    creer_incident(client, "Incident B")
    html = client.get("/").get_data(as_text=True)
    assert "Incident A" in html
    assert "Incident B" in html


def test_detail_incident(client):
    creer_incident(client)
    response = client.get("/incidents/1")
    assert response.status_code == 200
    assert "Salle B12" in response.get_data(as_text=True)


def test_modifier_statut(client):
    creer_incident(client)
    response = client.post(
        "/incidents/1/statut", data={"statut": "Résolu"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert "Résolu" in response.get_data(as_text=True)


def test_suppression_incident(client):
    creer_incident(client)
    client.post("/incidents/1/delete")
    assert client.get("/incidents/1").status_code == 404


def test_ajout_invalide_refuse(client):
    response = client.post(
        "/incidents/add",
        data={"titre": "", "description": "", "lieu": "", "priorite": "Faible"},
    )
    assert response.status_code == 400
