from flask import Blueprint

api_bp = Blueprint("api", __name__)

# routes
from .controllers import DummyController
