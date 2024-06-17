
from datetime import timedelta
import os
from typing import Any
from flask import Flask
from dynaconf import FlaskDynaconf
from flask_rabbitmq import RabbitMQ
from flask_rabbitmq.queue import Queue
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from descope import DescopeClient
from dynaconf import settings
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_redis import FlaskRedis
from opentelemetry.metrics import get_meter_provider

meter = get_meter_provider().get_meter("micro-services-app", "1.0")
basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ.get("DATABASE_SQLITE") == True:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, '../' ,'app.db')
# setup db
db = SQLAlchemy()

try:
    print (f"DESCOPE_PROJECT_ID: {settings['DESCOPE_PROJECT_ID']}")
    descope_client = DescopeClient(project_id=settings['DESCOPE_PROJECT_ID']) # initialize the descope client
except Exception as error:
    print ("failed to initialize. Error:")
    print (error)



class ApplicationMgr:
    application:Flask = None
    queue = Queue()
    mqConnector:RabbitMQ = None
    limiter: Limiter = None
    redis_client: FlaskRedis = None
    def init(self,**config_overrides: Any) -> Any:
        # initialize the app
        self.application = self._create_app(config_overrides)
        self.limiter = Limiter(get_remote_address, app=self.application, storage_uri=self.application.config['REDIS_URL'])
        self.redis_client = FlaskRedis(self.application)
        if self.application.config['RABBITMQ_ENABLED']== True:
            self.mqConnector = RabbitMQ(self.application, self.queue)
            self.mqConnector.run_with_flask_app()
    
    def _create_app(**config_overrides: Any) -> Flask:
        """
        Factory application creator
        args: config_overrides = testing overrides
        """
        app = Flask(__name__)
        # Load config
        FlaskDynaconf(app, **config_overrides)
        # apply overrides for tests
        app.config.update(config_overrides)
    
        # setup CORS
        CORS(
            app,
            resources={
                r"/v1.0/*": {
                    "origins": app.config["CORS_ORIGINS"],
                    "allow_headers": [
                        "Content-Type",
                        "Authorization",
                        "Access-Control-Allow-Credentials",
                        "X-CSRF-TOKEN",
                    ],
                }
            },
            supports_credentials=True,
        )
    
        # initialize db
        db.init_app(app)
        Migrate(app, db)
    
        # import blueprints
        from server.api_1_0.api import api_1_0_app
    
        # register blueprints
        app.register_blueprint(api_1_0_app, url_prefix="/api/v1")
    
        return app