import os
import sqlite3

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

PRIORITES = ["Faible", "Moyenne", "Élevée"]
STATUTS = ["Nouveau", "En cours", "Résolu"]


def create_app(test_config=None):
    app = Flask(__name__)
    base_dir = os.path.dirname(app.root_path)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.environ.get("DATABASE_PATH", os.path.join(base_dir, "data", "incidents.db")),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        get_db().execute(
            """CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT NOT NULL,
                lieu TEXT NOT NULL,
                priorite TEXT NOT NULL,
                statut TEXT NOT NULL DEFAULT 'Nouveau'
            )"""
        )
        get_db().commit()

    def get_incident_or_404(incident_id):
        row = get_db().execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
        if row is None:
            abort(404)
        return row

    # 2. Afficher la liste
    @app.route("/")
    def index():
        incidents = get_db().execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
        return render_template("index.html", incidents=incidents)

    # 1. Ajouter un incident
    @app.route("/incidents/add", methods=["GET", "POST"])
    def add_incident():
        if request.method == "POST":
            titre = request.form.get("titre", "").strip()
            description = request.form.get("description", "").strip()
            lieu = request.form.get("lieu", "").strip()
            priorite = request.form.get("priorite", "")
            if not (titre and description and lieu) or priorite not in PRIORITES:
                flash("Tous les champs sont obligatoires.", "error")
                return render_template("add.html", priorites=PRIORITES), 400
            db = get_db()
            db.execute(
                "INSERT INTO incidents (titre, description, lieu, priorite) VALUES (?, ?, ?, ?)",
                (titre, description, lieu, priorite),
            )
            db.commit()
            flash("Incident ajouté.", "success")
            return redirect(url_for("index"))
        return render_template("add.html", priorites=PRIORITES)

    # 3. Détails
    @app.route("/incidents/<int:incident_id>")
    def detail(incident_id):
        incident = get_incident_or_404(incident_id)
        return render_template("detail.html", incident=incident, statuts=STATUTS)

    # 4. Modifier le statut
    @app.route("/incidents/<int:incident_id>/statut", methods=["POST"])
    def update_statut(incident_id):
        get_incident_or_404(incident_id)
        statut = request.form.get("statut", "")
        if statut not in STATUTS:
            abort(400)
        db = get_db()
        db.execute("UPDATE incidents SET statut = ? WHERE id = ?", (statut, incident_id))
        db.commit()
        flash("Statut mis à jour.", "success")
        return redirect(url_for("detail", incident_id=incident_id))

    # 5. Supprimer
    @app.route("/incidents/<int:incident_id>/delete", methods=["POST"])
    def delete_incident(incident_id):
        get_incident_or_404(incident_id)
        db = get_db()
        db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
        db.commit()
        flash("Incident supprimé.", "success")
        return redirect(url_for("index"))

    return app
