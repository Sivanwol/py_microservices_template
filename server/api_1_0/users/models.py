from sqlalchemy import event
from server.app import db
from flask_restx import api, fields

class ConfigModel(db.Model):
    __tablename__ = "configuration"
    key = db.Column(db.String(100), nullable=False , primary_key=True)
    value = db.Column(db.String, nullable=True)

    def __repr__(self) -> str:
        return f"<Config {ConfigModel.key}>"

# event.listen(ConfigModel, 'before_insert', lambda _, __, obj: obj.key.lower())