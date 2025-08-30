from flask import Flask
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed, RequestEntityTooLarge, HTTPException
from lib.utils.utils import error_response

# https://werkzeug.palletsprojects.com/en/stable/exceptions/
def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(BadRequest)
    def handle_bad_request(e: BadRequest):
        return error_response(400, "Bad request", str(e))

    @app.errorhandler(NotFound)
    def handle_not_found(e: NotFound):
        return error_response(404, "Not found", str(e))

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(e: MethodNotAllowed):
        return error_response(405, "Method not allowed", str(e))

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_entity_too_large(e: RequestEntityTooLarge):
        return error_response(413, "Request entity too large", str(e))

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return error_response(e.code or 500, e.name, e.description)

    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        return error_response(500, "Internal server error")
