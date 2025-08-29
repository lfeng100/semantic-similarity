from lib.api import api_bp

@api_bp.get("/ping")
def ping():
    return {"message": "pong"}, 200
