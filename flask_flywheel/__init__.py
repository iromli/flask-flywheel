# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from dynamo3.connection import DynamoDBConnection
from flywheel import Engine as _Engine

from _meta import __version__  # noqa


class Engine(_Engine):
    """A subclass of ``flywheel.Engine`` that adds additional features.
    """

    def connect(self, region, **kwargs):
        """Connect to AWS region.
        """
        self.dynamo = DynamoDBConnection.connect(region, **kwargs)


class Flywheel(object):
    """This class is used to control the Flywheel integration to Flask
    application.

    This class accepts various configuration to be used to customize its
    behavior, e.g. connecting to DynamoDB local instance:

    FLYWHEEL_DATABASE_HOST:
        DynamoDB host. Set the value (e.g. ``"localhost"``) to connect to
        local instance. Default to ``None``.

    FLYWHEEL_DATABASE_PORT:
        DynamoDB port. Set the value (e.g. 8000) to connect to local instance.
        Default to ``None``.

    FLYWHEEL_REGION:
        AWS region. If connected to local instance, this value is ignored.
        Default to ``"us-east-1"``.

    FLYWHEEL_SECURE:
        Determine whether the connection must use secure protocol (HTTPS).
        Default to ``True``.

    AWS_ACCESS_KEY:
        AWS access key. Default to ``None``.

    AWS_SECRET_ACCESS_KEY:
        AWS secret access key. Default to ``None``.

    There are two usage modes which work very similar. One is binding
    the instance to a very specific Flask application::

        from flask import Flask

        app = Flask(__name__)
        db = Flywheel(app)

    The second possibility is to create the object once and configure
    application later to support it::

        db = Flywheel()

        def create_app():
            app = Flask(__name__)
            db.init_app(app)
            return app

    Since this class acts as a thin layer of ``flywheel`` library,
    to declare a model and its field, use ``flywheel.Model`` and
    ``flywheel.Field`` directly::

        from flywheel import Model, Field

        class User(Model):
            username = Field(hash_key=True)

    Afterwards, instead of using the original ``flywheel.Engine`` to
    interact with DynamoDB, use the ``engine`` attribute provided by
    this class::

        db.engine.register(User)
        db.engine.create_schema()

    Refer to `flywheel documentation <http://flywheel.readthedocs.org/>`_
    for details on how to interact with DynamoDB.
    """

    def __init__(self, app=None):
        self._engine = None
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This callback can be used to initialize an application for the
        use with this database setup.
        """
        app.config.setdefault("FLYWHEEL_DATABASE_HOST", None)
        app.config.setdefault("FLYWHEEL_DATABASE_PORT", None)
        app.config.setdefault("FLYWHEEL_REGION", "us-east-1")
        app.config.setdefault("FLYWHEEL_SECURE", True)
        app.config.setdefault("AWS_ACCESS_KEY", None)
        app.config.setdefault("AWS_SECRET_ACCESS_KEY", None)

        app.extensions = getattr(app, "extensions", {})
        app.extensions["flywheel"] = self
        self.app = app

    @property
    def engine(self):
        """Returns a cached object of DynamoDB connection. It's worth
        noting that accessing this property without having a proper
        initialization step will raise an error.
        """
        assert self.app is not None, \
            "The flywheel extension was not registered " \
            "to the current application. Please make sure " \
            "to call init_app() first."

        if self._engine is None:
            self._engine = Engine()
            self._engine.connect(
                self.app.config["FLYWHEEL_REGION"],
                access_key=self.app.config["AWS_ACCESS_KEY"],
                secret_key=self.app.config["AWS_SECRET_ACCESS_KEY"],
                host=self.app.config["FLYWHEEL_DATABASE_HOST"],
                port=self.app.config["FLYWHEEL_DATABASE_PORT"],
                is_secure=self.app.config["FLYWHEEL_SECURE"],
                )
        return self._engine
