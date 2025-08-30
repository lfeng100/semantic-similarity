import time, sys, uuid
from flask import Flask, request, g
import structlog

def setup_structlog():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()

log = setup_structlog()

def setup_logging(app: Flask) -> None:
    @app.before_request
    def _start_timer_and_request_id():
        # Request timing
        g._start_time = time.perf_counter()
        # Correlation ID
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        g.request_id = rid

    @app.after_request
    def _log_response(resp):
        # Attach X-Request-ID
        resp.headers["X-Request-ID"] = getattr(g, "request_id", "")

        dur_ms = None
        try:
            dur_ms = round((time.perf_counter() - g._start_time) * 1000.0, 2)
        except Exception:
            pass

        log.bind(request_id=getattr(g, "request_id", None)).info(
            "http_request",
            method=request.method,
            path=request.path,
            status=resp.status_code,
            duration_ms=dur_ms,
            content_length=request.content_length,
            user_agent=request.user_agent.string,
        )
        return resp

    @app.teardown_request
    def _log_exception(exc):
        if exc is not None:
            log.bind(request_id=getattr(g, "request_id", None)).error(
                "http_error", error=str(exc), path=request.path
            )
