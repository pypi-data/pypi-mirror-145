import pytest
import flask
from flask_theme_adminlte3.app import create_app

@pytest.fixture(scope='function')
def app():

    app = create_app()
    app.testing = True
    yield app

@pytest.fixture()
def runner(app):
    r = app.test_cli_runner()

    def runfunc(command):
        return r.invoke(r.app.cli,command.split())

    yield runfunc