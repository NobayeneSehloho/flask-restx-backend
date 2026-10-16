from flask_sqlalchemy import SQLAlchemy 
from flask_restx import Api

# Swagger/OpenAPI security scheme so the UI shows an "Authorize" button.
# NOTE: this is documentation only — actual enforcement is the token_required
# decorator in app/security.py. In Swagger 2.0 (Flask-RESTX) a bearer JWT is
# represented as an apiKey carried in the Authorization header.
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "JWT token. Format: Bearer <your token>",
    }
}

api = Api(authorizations=authorizations, security="Bearer")
db = SQLAlchemy()