import pytest
import flask
from  flask_mkdocs import documentation
def create_app():
    app = flask.Flask('test')
    documentation.init_app(app)
    return app

@pytest.fixture(scope='function')
def app():

    app = create_app()
    app.testing = True
    yield app

@pytest.fixture()
def runner(app:flask.Flask):
    import os
    r = app.test_cli_runner(env=os.environ)

    def runfunc(command):
        return r.invoke(r.app.cli,command.split())

    yield runfunc