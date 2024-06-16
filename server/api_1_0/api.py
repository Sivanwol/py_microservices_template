"""
Api v1 namespace entrypoint
"""

from flask import Blueprint
from flask_restx import Api

from .common.resources import ConfgiRoutes, namespace as common_namespace


api_1_0_app = Blueprint("api_1_0", __name__)

# Add JWT authorization header for swagger
authorizations = {
    "jwt": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "JWT authorization token, Example: 'Bearer JWT'",
    }
}


api = Api(
    api_1_0_app,
    version="1.0",
    title="Server API",
    description="Server API Platform",
    validate=True,
    authorizations=authorizations,
)
api.add_namespace(common_namespace)
common_namespace.add_resource(ConfgiRoutes, "/config")
