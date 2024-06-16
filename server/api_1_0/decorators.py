"""
JWT Decorators
"""
import os
from flask import Flask, request, make_response, jsonify

from functools import wraps
from server.app import descope_client
from flask.helpers import make_response
from .enums import RoleEnum

def token_required(f): # auth decorator
    @wraps(f)
    def decorator(*args, **kwargs):
        session_token = None

        if 'Authorization' in request.headers: # check if token in request
            auth_request = request.headers['Authorization']
            session_token = auth_request.replace('Bearer ', '')
        if not session_token: # throw error
            return make_response(jsonify({"error": "❌ invalid session token!"}), 401)

        try: # validate token
            jwt_response = descope_client.validate_session(session_token=session_token)
        except:
            return make_response(jsonify({"error": "❌ invalid session token!"}), 401)

        return f(jwt_response, *args, **kwargs)

    return decorator