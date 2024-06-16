
from descope.flask import descope_validate_auth
from flask.helpers import make_response
from flask.json import jsonify
from flask_restx import Resource, Namespace, fields, reqparse
from marshmallow import ValidationError
from server.app import db, descope_client
from ..decorators import token_required
from .models import ConfigModel
from .schema import ConfigSchema
namespace = Namespace("common", description="Common namespace routes")

user_schema = ConfigSchema()
# config actions models
add_new_config_model =  namespace.model('AddConfig', {
    'key' : fields.String,
    'value' : fields.String,
})
update_config_model =  namespace.model('UpdateConfig', {
    'key' : fields.String,
    'value' : fields.String,
})

class ConfgiRoutes(Resource): 
    """
    Routes
    """
    @descope_validate_auth(
        descope_client,
        roles="admin",
    )
    @namespace.doc(security="jwt")
    @namespace.expect(add_new_config_model)
    def post(self):
        """
        Add new config
        """
        try:
            data = user_schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

        config = ConfigModel(**data)
        db.session.add(config)
        db.session.commit()
        return make_response(jsonify({"success": "✅ config added"}), 200)

    @descope_validate_auth(
        descope_client,
        roles="admin",
    )
    @namespace.doc(security="jwt")
    @namespace.expect(update_config_model)
    def put(self):
        """
        Update config
        """
        try:
            data = user_schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

        config = ConfigModel.query.filter_by(key=data['key']).first()
        if not config:
            return make_response(jsonify({"error": "❌ config not found"}), 404)

        config.value = data['value']
        db.session.commit()
        return make_response(jsonify({"success": "✅ config updated"}), 200)

    @descope_validate_auth(
        descope_client,
    )
    @namespace.doc(security="jwt")
    def get(self):
        """
        Get all configs
        """
        configs = ConfigModel.query.all()
        return make_response(jsonify(user_schema.dump(configs, many=True)), 200)


    @descope_validate_auth(
        descope_client,
    )
    @namespace.doc(security="jwt")
    def get(self, key):
        """
        Get key config
        """
        config = ConfigModel.query.filter_by(key=key).first()
        if not config:
            return make_response(jsonify({"error": "❌ config not found"}), 404)

        return make_response(jsonify(user_schema.dump(config)), 200)

    @descope_validate_auth(
        descope_client,
        roles="admin",
    )
    @namespace.doc(security="jwt")
    @namespace.expect(add_new_config_model)
    def delete(self):
        """
        Delete config
        """
        try:
            data = user_schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

        config = ConfigModel.query.filter_by(key=data['key']).first()
        if not config:
            return make_response(jsonify({"error": "❌ config not found"}), 404)

        db.session.delete(config)
        db.session.commit()
        return make_response(jsonify({"success": "✅ config deleted"}), 200)