from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


@pytest.fixture(scope="session")
def app(request):
    from flask import Flask

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["FLYWHEEL_DATABASE_HOST"] = "localhost"
    app.config["FLYWHEEL_DATABASE_PORT"] = 8000
    app.config["FLYWHEEL_SECURE"] = False
    return app


@pytest.fixture(scope="session")
def flywheel(app):
    from flask_flywheel import Flywheel

    flywheel = Flywheel(app)
    return flywheel


@pytest.fixture()
def unitialized_flywheel():
    from flask_flywheel import Flywheel

    flywheel = Flywheel()
    return flywheel


def test_init_app(app, flywheel):
    assert app.extensions["flywheel"] == flywheel
    assert flywheel.app == app


def test_engine(app, flywheel):
    from flask_flywheel import Engine
    assert flywheel.engine.__class__ == Engine


def test_uninitialized_engine(unitialized_flywheel):
    with pytest.raises(RuntimeError) as exc:
        unitialized_flywheel.engine.create_schema()
        assert "context" in str(exc.value)
