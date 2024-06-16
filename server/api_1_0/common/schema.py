
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates, post_load, post_dump

from .models import ConfigModel

class ConfigSchema(SQLAlchemyAutoSchema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)

    class Meta:
        model = ConfigModel
        include_fk = True
        load_instance = True