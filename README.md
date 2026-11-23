# Gestion des incidents informatiques

![CI](https://github.com/emna797/gestion-incidents/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/emna797/gestion-incidents/actions/workflows/cd.yml/badge.svg)

Application web (Flask + SQLite) permettant de signaler et suivre les incidents
informatiques déclarés par les étudiants et les enseignants.
Projet réalisé dans le cadre du mini-projet DevOps (DSI3, 2026-2027).

## Fonctionnalités

- Ajouter un incident
- Afficher la liste des incidents (statistiques et recherche)
- Consulter les détails d'un incident
- Modifier le statut (Nouveau, En cours, Résolu)
- Supprimer un incident

## Modèle de données

| Champ | Description |
|---|---|
| id | Identifiant unique |
| titre | Intitulé de l'incident |
| description | Description du problème |
| lieu | Salle ou laboratoire concerné |
| priorite | Faible, Moyenne, Élevée |
| statut | Nouveau, En cours, Résolu |

## Technologies

Python 3.12, Flask, SQLite, Gunicorn, Pytest, Docker, Docker Compose,
GitHub Actions, GitHub Container Registry (GHCR).

## Structure du dépôt

```
gestion-incidents/
├── app/                       code de l'application et templates
├── tests/                     tests automatisés (pytest)
├── .github/workflows/
│   ├── ci.yml                 intégration continue
│   └── cd.yml                 publication de l'image dans GHCR
├── Dockerfile                 construction de l'image
├── compose.yaml               exécution avec construction locale
├── compose.deploy.yaml        déploiement depuis l'image GHCR
├── requirements.txt           dépendances de production
├── requirements-dev.txt       dépendances de test
├── run.py                     point d'entrée
└── README.md
```

## Installation locale

```bash
git clone https://github.com/emna797/gestion-incidents.git
cd gestion-incidents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python run.py
```

L'application est accessible sur http://127.0.0.1:5000

## Tests

```bash
python -m pytest -v
```

8 tests couvrent la page d'accueil, l'ajout, la liste, le détail, la
modification du statut, la suppression et la validation du formulaire.

## Docker

```bash
docker build -t gestion-incidents .
docker run -d --name incidents-app -p 5000:5000 gestion-incidents
docker ps
docker logs incidents-app
```

## Docker Compose (construction locale)

```bash
docker compose up -d --build
docker compose ps
docker compose logs
docker compose down
```

La base SQLite est stockée dans le volume nommé `incidents-data` : les données
survivent à la suppression du conteneur. `down -v` supprime aussi les données.

## Pipeline CI/CD

```
Code -> Git/GitHub -> Push/PR -> GitHub Actions
     -> Tests -> Validation Compose -> Build Docker
     -> Publication GHCR -> Pull -> Déploiement Compose
```

### CI (`ci.yml`)

Déclenchée sur push et Pull Request vers `main` :
1. Récupération du code
2. Installation de Python et des dépendances
3. Exécution des tests
4. Validation de la configuration (`docker compose config`)
5. Construction de l'image Docker

### CD (`cd.yml`)

Déclenchée sur push vers `main` :
1. Exécution des tests
2. Construction de l'image
3. Connexion à GHCR avec `GITHUB_TOKEN` (permission `packages: write`)
4. Publication avec deux tags : `latest` et le SHA du commit

La publication dépend de la réussite des tests (`needs: test`).

## Déploiement depuis GHCR

L'image est publiée sur `ghcr.io/emna797/gestion-incidents`.

```bash
docker compose -f compose.deploy.yaml pull
docker compose -f compose.deploy.yaml up -d
docker compose -f compose.deploy.yaml ps
docker compose -f compose.deploy.yaml logs
```

Application : http://localhost:5000

## Mise à jour de l'application

1. Modifier le code, puis `git commit` et `git push origin main`
2. Vérifier que CI et CD sont verts (onglet Actions)
3. Vérifier le nouveau tag dans Packages
4. Récupérer et relancer :

```bash
docker compose -f compose.deploy.yaml pull
docker compose -f compose.deploy.yaml up -d
```

Pour revenir à une version précédente, remplacer `latest` par un tag SHA dans
`compose.deploy.yaml`.

## Variables d'environnement

| Variable | Rôle | Défaut |
|---|---|---|
| DATABASE_PATH | Chemin de la base SQLite | `data/incidents.db` |
| SECRET_KEY | Clé secrète Flask | `dev` |

## Captures d'écran

Voir le dossier `docs/screenshots/`.

## Auteurs

Binôme : Emna bouchnak et Tasnim Arridhi - DSI32
