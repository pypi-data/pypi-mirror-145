import pytest
import flask


@pytest.fixture()
def runner(app):
    r = app.test_cli_runner()

    def runfunc(command):
        return r.invoke(r.app.cli,command.split())

    yield runfunc