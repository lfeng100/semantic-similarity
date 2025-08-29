from flask import Flask
from lib.api import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

if __name__ == "__main__":
    # Dev server for local use (Docker will use the same for this first iteration)
    app = create_app()
    app.run(host="0.0.0.0", port=8080)