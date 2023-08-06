# -*- coding: utf-8 -*-
import flask, click
from pathlib import Path
from . import theme, menu, assets

def create_app(config_file: Path = None,**overrides:flask.Config):
    """Create an application with custom configurations.

    Configurations passed into this function will override
    all other configurations.

    Args:
        config_file (Path, optional): Path to a config file. Relative
            paths will be relative to the instance_path. Defaults to None.
        overrides (dict, optional): dictionary of configuration value overrides.

    Raises:
        EnvironmentError: The configuration file does not exist
    """

    app = flask.Flask('theme')

    if config_file and app.config.from_pyfile(config_file):
        app.logger.debug(f"Loaded config_file from {config_file}")

    for k,v in overrides.items():
        app.config[k.upper()] = v

    theme.init_app(app)
    menu.init_app(app)
    assets.init_app(app)

    text = '\n'.join([f"{k}: {v}" for k,v in app.config.items() if k.startswith('THEME_')])

    app.logger.debug(text)

    @app.route('/')
    def home():
        return flask.render_template_string(
        """
        {% extends config.BASE_TEMPLATE %}
        {% block page_content %}
            Hello World
        {% endblock %}
        """)

    @app.cli.command('version',help=f"Print the curent version of {app.name}")
    def print_version():
        f"""Print the version of {app.name}"""
        click.echo(flask.current_app.config['VERSION'])

    return app
