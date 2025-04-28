from flask import Flask
from config import Config
from database import db
from routes import api


def create_app():
    app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(api, url_prefix="/api")

    # Serve SPA
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app

if __name__ == "__main__":
    create_app().run(debug=True)