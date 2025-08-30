from flask import Flask
from lib.api import api_bp
from config import Config
from lib.api.errors import register_error_handlers
from lib.logging.structlog import setup_logging


from dotenv import load_dotenv
load_dotenv()  # loads .env

def create_app(config_class: type = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp, url_prefix="/")
    register_error_handlers(app)
    setup_logging(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
