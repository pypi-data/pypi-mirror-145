
try:
    from flask_assets import Environment, Bundle
except ImportError:
    flask_assets = None
import flask
import pathlib
import gzip
import tempfile
import os

def gz(inp, out, **kw):
    n = ''
    with tempfile.NamedTemporaryFile('wb',delete=False) as t:
        with gzip.open(t.name, "wb") as f:
            f.write(inp.read().encode())
            n = t.name
    with open(n,'rb') as f:
        out.write(f.read().decode('ISO-8859–1'))
    os.unlink(n)

def init_app(app:flask.Flask):
    if not flask_assets:
        app.logger.debug(f"Disabling assets extention since 'flask_assets' module is missing")
        return
    filters = []#[gz]
    assets = Environment()
    bp_name = app.config['THEME_BLUEPRINT_NAME']
    prefix = app.config['THEME_ASSETS_PATH']
    if prefix is None:
        prefix = pathlib.Path(app.root_path) / 'assets'

    styles = Bundle(
        f'{prefix}/plugins/icheck-bootstrap/icheck-bootstrap.css',
        f'{prefix}/dist/css/adminlte.min.css',
        f'{prefix}/plugins/overlayScrollbars/css/OverlayScrollbars.min.css',
        f'{prefix}/plugins/fontawesome-free/css/all.min.css',
        filters=['cssmin']+filters,
        output=f'{bp_name}/css/{bp_name}.css',
    )

    scripts = Bundle(
        f'{prefix}/plugins/jquery/jquery.js',
        f'{prefix}/plugins/jquery-ui/jquery-ui.min.js',
        f'{prefix}/plugins/bootstrap/js/bootstrap.bundle.min.js',
        f'{prefix}/plugins/overlayScrollbars/js/jquery.overlayScrollbars.js',
        f'{prefix}/plugins/overlayScrollbars/js/OverlayScrollbars.js',
        f'{prefix}/dist/js/adminlte.js',
        filters=['jsmin']+filters,
        output=f'{bp_name}/js/{bp_name}.js',
    )

    assets.register(f'{bp_name}_css', styles)
    assets.register(f'{bp_name}_js', scripts)

    assets.init_app(app)
