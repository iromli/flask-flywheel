# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.1.0"

from dynamo3.connection import DynamoDBConnection
from flywheel import Engine as _Engine
from flask import _app_ctx_stack


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

    FLYWHEEL_ENGINE_NAMESPACE:
        String prefix or list of component parts of a prefix for models. All
        table names will be prefixed by this string or strings (joined by '-').
        Default to ``None``.

    FLYWHEEL_ENGINE_DEFAULT_CONFLICT:
        Can be on of: 'update', 'overwrite', 'raise' which sets the default setting for delete(), save(), and sync()
        See `flywheel documentation <http://flywheel.readthedocs.io/en/latest/ref/flywheel.engine.html#module-flywheel.engine>`_
        Default to ``update``.

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
        if self.app is None:
            self.app = app

        app.config.setdefault("FLYWHEEL_DATABASE_HOST", None)
        app.config.setdefault("FLYWHEEL_DATABASE_PORT", None)
        app.config.setdefault("FLYWHEEL_REGION", "us-east-1")
        app.config.setdefault("FLYWHEEL_SECURE", True)
        app.config.setdefault("FLYWHEEL_ENGINE_NAMESPACE", ())
        app.config.setdefault("FLYWHEEL_ENGINE_DEFAULT_CONFLICT", "update")
        app.config.setdefault("AWS_ACCESS_KEY", None)
        app.config.setdefault("AWS_SECRET_ACCESS_KEY", None)

        app.extensions = getattr(app, "extensions", {})
        app.extensions["flywheel"] = self

    @property
    def engine(self):
        """Returns a cached object of DynamoDB connection. It's worth
        noting that accessing this property without having a proper
        initialization step will raise an error.
        """
        if self._engine is None:
            app = self._get_app()

            self._engine = Engine(
                namespace=app.config["FLYWHEEL_ENGINE_NAMESPACE"],
                default_conflict=app.config["FLYWHEEL_ENGINE_DEFAULT_CONFLICT"]
            )

            self._engine.connect(
                app.config["FLYWHEEL_REGION"],
                access_key=app.config["AWS_ACCESS_KEY"],
                secret_key=app.config["AWS_SECRET_ACCESS_KEY"],
                host=app.config["FLYWHEEL_DATABASE_HOST"],
                port=app.config["FLYWHEEL_DATABASE_PORT"],
                is_secure=app.config["FLYWHEEL_SECURE"],
                )
        return self._engine

    def _get_app(self):
        if self.app:
            return self.app

        ctx = _app_ctx_stack.top
        if ctx:
            return ctx.app

        raise RuntimeError("application not registered on flywheel "
                           "instance and no application bound "
                           "to current context")
