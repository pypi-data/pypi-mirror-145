import flask, werkzeug
from flask import signals
import pathlib
from flask.signals import Namespace
from .datatypes import Menu, MenuItem
import yaml, os

MENUS_YAML = "menus.yml"
DEFAULT_MENUS_FILE = os.path.join(os.path.dirname(__file__), MENUS_YAML)


class MenuLoader:
    """
    A menu loader from a database or other source.
    """

    def __init__(self, app=None):
        """
        Arguments:
            app (flask.Flask): Flask app
        """

        if app:
            self.init_app(app)

        self._menu_funcs = {}

    def init_app(self, app):
        @app.context_processor
        def processors():
            return dict(
                menu=self,
            )

    def add_menu_items(self, menu_name):
        """
        Decorator for adding new menu items

        menu = MenuLoader()

        @menu.add_menu_items('topbar')
        def more_items():
            return [MenuItem(...),MenuItem(...)]
        """

        def real_decorator(function):
            if menu_name not in self._menu_funcs:
                self._menu_funcs[menu_name] = []
            self._menu_funcs[menu_name].append(function)
            return function

        return real_decorator

    def navbar_menu(self):
        return self.load_menu("topbar")

    def sidebar_menu(self):
        return self.load_menu("sidebar")

    def second_sidebar_menu(self):
        return self.load_menu("second_sidebar")

    def is_active(self, item):
        return item.url == (
            flask.request.script_root
            + flask.request.path
            + (
                f"?{flask.request.query_string.decode()}"
                if flask.request.query_string
                else ""
            )
        )

    def load_menu(self, menu_name):
        items = menu_from_yaml()
        if menu_name not in items:
            return None
        item = items[menu_name][0]["items"]
        title = items[menu_name][0]["title"]
        m = Menu(title=title)
        _create_menu_items(m, item)

        show_menu.send(
            flask.current_app._get_current_object(),
            loader=self,
            menu_name=menu_name,
            menu=m,
        )
        activated = m.activate_by_function(self.is_active, all=True)

        return m


_signals = Namespace()

show_menu = _signals.signal("show-menu")
""" 
show_menu signal is sent before rendering the menu. 
You can use it to add additional items to the menu.

Example:

    @show_menu.connect
    def _add_menu(app,menu_name,menu)
        if menu_name == 'admin_menu':
            menu.add_item(MenuItem(...))
"""

if signals.signals_available:

    @show_menu.connect
    def _add_menu(app, loader, menu_name, menu):
        # Add to menu all menuitems
        # from the menu loader functions
        # for menu_name
        if menu_name in loader._menu_funcs:
            funcs = loader._menu_funcs[menu_name]
            for f in funcs:
                menu_items = f()
                for item in menu_items:
                    menu.add_item(item)


def menu_from_yaml():
    menu_file = DEFAULT_MENUS_FILE
    menu = None

    # overwrrite the menu using the menus.yml in the instance settings
    if flask.has_app_context():
        instance_menu_file = os.path.join(flask.current_app.instance_path, "menus.yml")
        if os.path.exists(instance_menu_file):
            menu_file = instance_menu_file
        else:
            instance_menu_file = pathlib.Path(__file__).parent / "menus.yml"
            if os.path.exists(instance_menu_file):
                menu_file = instance_menu_file

    with open(menu_file) as f:
        menu = yaml.load(f, Loader=yaml.SafeLoader)

    return menu


def _create_menu_items(menu: Menu, items: dict, parent=None):
    """
    Recursively add dictionary of menu items to menu
    """
    for attrs in items:
        children = attrs.pop("items", [])
        title = attrs.pop("title", "Missing Title")
        link = attrs.pop("url", "#")
        badge = attrs.pop("badge", None)
        endpoint = attrs.pop("endpoint", None)
        help = attrs.pop("help", "")
        icon = attrs.pop("icon", None)
        form = attrs.pop("form", None)

        kind = MenuItem.TYPE_FORM if form else MenuItem.TYPE_LINK

        item_type = attrs.pop("item_type", kind)

        endpoint_kwargs = attrs.pop("endpoint_kwargs", "")
        if endpoint:
            try:
                if endpoint_kwargs:
                    if isinstance(endpoint_kwargs, str):
                        link = flask.url_for(endpoint) + "?" + endpoint_kwargs
                    elif isinstance(endpoint_kwargs, dict):
                        link = flask.url_for(endpoint, **endpoint_kwargs)
                    else:
                        print(
                            f"Unexpected endpoint_kwargs type: {type(endpoint_kwargs)} in MenuItem {title}"
                        )
                else:
                    link = flask.url_for(endpoint)

            except werkzeug.routing.BuildError as e:
                help += f"Error: {e}"
                if not badge:
                    badge = ["Soon", "danger"]

        elif link.startswith("/") and not link.startswith("//"):
            link = flask.request.script_root + link

        item = MenuItem(
            id_item=title,
            item_type=item_type,
            title=title,
            url=link,
            parent=parent,
            icon=icon,
            help=help,
            badge=badge,
            form=form,
        )

        menu.add_item(item)

        if children:
            _create_menu_items(menu, children, parent=item)


menu = MenuLoader()


def init_app(app):
    menu.init_app(app)
