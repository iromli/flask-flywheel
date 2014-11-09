from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from dynamo3.connection import DynamoDBConnection
from flywheel import Engine as _Engine


class Engine(_Engine):
    def connect(self, region, **kwargs):
        self.dynamo = DynamoDBConnection.connect(region, **kwargs)


class Flywheel(object):
    def __init__(self, app=None):
        self._engine = None

        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        app.config.setdefault("FLYWHEEL_DATABASE_HOST", None)
        app.config.setdefault("FLYWHEEL_DATABASE_PORT", None)
        app.config.setdefault("FLYWHEEL_REGION", "us-east-1")
        app.config.setdefault("FLYWHEEL_IS_SECURE", True)
        app.config.setdefault("AWS_ACCESS_KEY", None)
        app.config.setdefault("AWS_SECRET_ACCESS_KEY", None)

        app.extensions = getattr(app, "extensions", {})
        app.extensions["flywheel"] = self
        self.app = app

    @property
    def engine(self):
        if self.app is None:
            raise AttributeError(
                "The flywheel extension was not registered "
                "to the current application. Please make sure "
                "to call init_app() first."
                )

        if self._engine is None:
            self._engine = Engine()
            self._engine.connect(
                self.app.config["FLYWHEEL_REGION"],
                access_key=self.app.config["AWS_ACCESS_KEY"],
                secret_key=self.app.config["AWS_SECRET_ACCESS_KEY"],
                host=self.app.config["FLYWHEEL_DATABASE_HOST"],
                port=self.app.config["FLYWHEEL_DATABASE_PORT"],
                is_secure=self.app.config["FLYWHEEL_IS_SECURE"],
                )
        return self._engine
