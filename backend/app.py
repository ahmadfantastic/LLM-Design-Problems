from flask import Flask
from config import Config
from database import db
from routes import api
from models import User
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        if not User.query.first():
            admin = User(
                username="admin",
                password_hash=generate_password_hash("admin"),
                is_admin=True,
            )
            db.session.add(admin)
            db.session.commit()

    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app

if __name__ == "__main__":
    create_app().run(debug=True)

