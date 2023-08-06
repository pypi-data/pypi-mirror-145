import flask
import os
from . import filters
from . import constants


class Theme:
    def __init__(self, app=None) -> None:
        if app:
            self.init_app(app)

    def init_app(self, app: flask.Flask):

        for k in dir(constants):
            if k.startswith("THEME_"):
                app.config.setdefault(k, getattr(constants, k))

        bp = flask.Blueprint(
            app.config["THEME_BLUEPRINT_NAME"],
            __name__,
            static_folder=app.config["THEME_STATIC_FOLDER"] or "static",
            template_folder=app.config["THEME_TEMPLATE_FOLDER"] or "templates",
        )

        app.register_blueprint(bp, url_prefix=app.config["THEME_URL_PREFIX"])

        if app.config["THEME_ERRORS"]:
            set_theme_errors(app)

        for name in filters.__all__:
            app.jinja_env.filters.setdefault(name, getattr(filters, name))

        @app.context_processor
        def processors():
            return dict(
                ThemeColor=constants.ThemeColor,
            )

        try:
            from flask_gravatar import Gravatar

            Gravatar(app, default="mp")
        except ImportError as e:

            @app.template_filter("gravatar")
            def gravatar(email):
                return email

            app.logger.debug(f'Missing "flask_gravatar" package')


def set_theme_errors(app):

    # Register errors handlers.
    from .views import (
        unauthorized,
        insufficient_permissions,
        page_not_found,
        too_many_requests,
        internal_error,
    )

    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, insufficient_permissions)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(429, too_many_requests)
    app.register_error_handler(500, internal_error)
