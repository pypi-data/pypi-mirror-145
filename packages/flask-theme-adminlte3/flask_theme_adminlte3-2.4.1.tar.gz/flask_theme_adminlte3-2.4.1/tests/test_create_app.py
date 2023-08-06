from flask.testing import FlaskClient
from flask_theme_adminlte3.app import create_app
import pytest

def test_configfile_not_exists(client:FlaskClient):

    with pytest.raises(EnvironmentError) as e_info:
        app = create_app('doesnotexist.py')

def test_configfile_does_load(tmp_path):
    conf = tmp_path / "config.py"
    conf.write_text("""CONFIG_KEY_1='CONFIG_VAL_1'""")
    app = create_app(conf)
    assert app.config['CONFIG_KEY_1']=='CONFIG_VAL_1'

def test_config_kwargs_does_load():
    app = create_app(CONFIG_KEY_2='CONFIG_VAL_2')
    assert app.config['CONFIG_KEY_2']=='CONFIG_VAL_2'
