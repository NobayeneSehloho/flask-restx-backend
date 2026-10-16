from functools import wraps
from flask import request, current_app, g
from flask_restx import abort
import jwt


def token_required(f):
    """Decorator that enforces a valid JWT on the wrapped endpoint method.

    Reads the ``Authorization: Bearer <token>`` header, verifies the token's
    signature and expiry using the shared ``SECRET_KEY`` from app config, and
    aborts with 401 if the header is missing/malformed or the token is
    expired/invalid. On success, the caller's email is stashed on ``flask.g``.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            abort(401, "Missing or malformed Authorization header")

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            abort(401, "Token has expired")
        except jwt.InvalidTokenError:
            abort(401, "Invalid token")

        g.current_user = payload.get("email")
        return f(*args, **kwargs)

    return wrapper
