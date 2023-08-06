"""Contains all the constant values used in this module."""

THEME_BLUEPRINT_NAME = "theme"

THEME_URL_PREFIX = "/theme"

BASE_TEMPLATE = "layouts/page.html"
"""The base template that all templates should extend. Defaults to 'layouts/page.html"""

BASE_IFRAME_TEMPLATE = 'layouts/iframe.html'
"""The base template for iframe. Defaults to 'layouts/iframe.html"""

THEME_ACCENT_COLOR = None
"""The color of the hyperlinks. Defaults to None."""

THEME_CONTROLBAR_LIGHT = False
"""Light theme for the control sidebar, the default is dark. Defaults to False."""

THEME_BRAND_HTML = "<b>EAGLE</b> Beta"
"""HTML version of the logo used on login pages and footer. Defaults to '<b>Admin</b>LTE 3'."""

THEME_LOGOUT_ENDPOINT = "" #"security.logout"
"""The name of the endpoint for user logout. Defaults to 'security.logout'."""

THEME_LOGIN_ENDPOINT = "" # "security.login"
"""The name of the endpoint for user login. Defaults to 'security.login'."""

THEME_REGISTRATION_ENDPOINT = "security.register"
"""The name of the endpoint for user registration. Defaults to 'security.register'."""

THEME_PROFILE_ENDPOINT = ""
"""The name of the endpoint for user registration. Defaults to ''."""

THEME_CHANGE_LANGUAGE_ENDPOINT = "translation.change_language"
"""The name of the endpoint for changing the language. Defaults to 'translation.change_language' """

THEME_BRAND_FAVICON = "data:image/x-icon"
"""The favicon url to show in the browser tab.  Defaults to 'data:image/x-icon' to disable on most browsers"""

THEME_JAVASCRIPT_TEMPLATE = "includes/javascript.html"
"""Javascript assets template, normally included in BASE_TEMPLATE.
The default template just includes the AdminLTE3 JavaScript files.
Set a new template if you would like to customize which JavaScript assets are
included on all pages. Defaults to 'includes/javascript.html'
"""

THEME_STYLESHEETS_TEMPLATE = "includes/stylesheets.html"
"""Stylesheet assets template, normally included in BASE_TEMPLATE.
The default template just includes the AdminLTE3 css files.
Set a new template if you would like to customize which CSS assets are
included on all pages. Defaults to 'includes/stylesheets.html'
"""

THEME_SITE_TITLE = "AdminLTE 3"
"""The title of the site. Defaults to 'AdminLTE 3'."""

THEME_META_TEMPLATE = "includes/meta.html"
"""Favicon template normally included in BASE_TEMPLATE. Defaults to 'includes/meta.html'"""

THEME_FAVICON_TEMPLATE = "includes/favicon.html"
"""Favicon template normally included in BASE_TEMPLATE. Defaults to 'includes/favicon.html'"""

THEME_TOPBAR_TEMPLATE = "includes/navigation.html"
"""Navigation top bar template which is normally included in BASE_TEMPLATE. Defaults to 'includes/navigation.html'"""

THEME_TOPBAR_USER_MENU_TEMPLATE = "includes/navigation/user_menu.html"
"""User panel template which is normally included in THEME_TOPBAR_TEMPLATE. Defaults to 'includes/navigation/user_menu.html'"""

THEME_TOPBAR_USER_MENU_DROPDOWN_TEMPLATE = "includes/navigation/user_menu_dropdown.html"
"""User panel dropdown template which is normally included in THEME_TOPBAR_TEMPLATE. Defaults to 'includes/navigation/user_menu_dropdown.html'"""

THEME_TOPBAR_NAV_TEMPLATE = "includes/navigation/nav.html"
"""Navigation Menu template which is normally included in THEME_TOPBAR_TEMPLATE. Defaults to 'includes/navigation/nav.html'"""

THEME_TOPBAR_SEARCH_TEMPLATE = "includes/navigation/search.html"
"""Topbat search which is normally included in THEME_TOPBAR_TEMPLATE. Defaults to 'includes/navigation/search.html'"""

THEME_TOPBAR_NOTIFICATIONS_TEMPLATE = "includes/navigation/notifications.html"
"""Topbar notifications template normally included in THEME_TOPBAR_TEMPLATE. Defaults to 'includes/navigation/notifications.html'"""

THEME_TOPBAR_USER_MENU_ENABLED = True
"""Enable the user menu panel on the top navigation bar. Defaults to True"""

THEME_ASSETS_ENABLED = True
"""Use compressed assets"""

THEME_ASSETS_PATH = None
"""Path to the source assets. Defaults to 'None'. If 'None', path is set to 'app.root_path/../assets'"""

THEME_SIDEBAR_ENABLED = True
"""Enable the main sidebar menu"""

THEME_PRELOADER_ENABLED = False
"""Enable preloading screen."""

THEME_BRAND_IMAGE_CLASS='brand-image img-circle elevation-3'
"""The css class for Brand Image"""

THEME_BRAND_IMAGE_STYLE='opacity: .8'
"""The css style for Brand Image"""

THEME_BRAND_IMAGE_URL = ''
"""URL for the Logo"""

THEME_SIDEBAR_TEMPLATE = "includes/sidebar.html"
"""Sidebar template which is normally included in BASE_TEMPLATE. Defaults to 'includes/sidebar.html'"""

THEME_SIDEBAR_NAV_TEMPLATE = "includes/sidebar/nav.html"
"""Navigation Menu template which is normally included in THEME_SIDEBAR_TEMPLATE. Defaults to 'includes/sidebar/nav.html'"""

THEME_SIDEBAR_USER_MENU_TEMPLATE = "includes/sidebar/user_menu.html"
"""User panel template which is normally included in THEME_SIDEBAR_TEMPLATE. Defaults to 'includes/sidebar/user_menu.html'"""

THEME_SIDEBAR_SEARCH_TEMPLATE = "includes/sidebar/search.html"
"""Sidebar search which is normally included in THEME_SIDEBAR_TEMPLATE. Defaults to 'includes/sidebar/search.html'"""

THEME_SIDEBAR_LOGO_TEMPLATE = "includes/sidebar/logo.html"
"""Brand Logo template which is normally included in THEME_SIDEBAR_TEMPLATE. Defaults to 'includes/sidebar/logo.html'"""

THEME_SIDEBAR_USER_MENU_ENABLED = True
"""Enable the user menu panel on the sidebar. Defaults to False"""

THEME_SIDEBAR_SEARCH_ENABLED = False
"""Enable the search input field on the sidebar. Defaults to False"""

THEME_CONTROLBAR_TEMPLATE = "includes/controlbar.html"
"""Control sidebar template which is normally included in BASE_TEMPLATE. Defaults to 'includes/controlbar.html'"""

THEME_CONTROLBAR_ENABLED = True
"""Enable the control sidebar. Defaults to False"""

THEME_FOOTER_TEMPLATE = "includes/footer.html"
"""Footer template which is normally included in BASE_TEMPLATE. Defaults to 'includes/footer.html'"""

THEME_BACK_TO_TOP_ENABLED = False
"""Turn on the back to top button. Defaults to False."""

THEME_ERRORS = False
"""Set to True to add the THEME_<error>_TEMPLATE error handlers to app"""

THEME_ERROR_BASE_TEMPLATE = "pages/error.html"
"""The base template that error pages extend"""

THEME_401_TEMPLATE = "pages/401.html"
"""The template used for 401 Unauthorized errors."""

THEME_403_TEMPLATE = "pages/403.html"
"""The template used for 403 Forbidden errors."""

THEME_404_TEMPLATE = "pages/404.html"
"""The template used for 404 Not Found errors."""

THEME_429_TEMPLATE = "pages/429.html"
"""The template used for 429 Too Many Requests errors."""

THEME_500_TEMPLATE = "pages/500.html"
"""The template used for 500 Internal Server Error errors."""

THEME_DARKMODE_SWITCH_ENABLED = True
"""Enable the darkmode switcher"""

THEME_FULLSCREEN_SWITCH_ENABLED = True
"""Enable the fullscreen switcher"""

THEME_STATIC_FOLDER = None
"""Override the theme's static folder path"""

THEME_TEMPLATE_FOLDER = None
"""Override the theme's template folder path"""

THEME_DEMO_ENABLED = False
"""Enable the controlbar theme customizer"""

THEME_LAYOUT_BOXED = False
"""Boxed Layout: use the class .layout-boxed to get a boxed layout that stretches only to 1250px. 
You cannot use both THEME_LAYOUT_BOXED and THEME_LAYOUT_FIXED_TOP_NAV 
or THEME_LAYOUT_FIXED_FOOTER at the same time. Anything else can be mixed together.
"""

THEME_LAYOUT_COLLAPSED_SIDEBAR = False
"""Collapsed Sidebar: use the class .sidebar-collapse to have a collapsed sidebar upon loading."""

THEME_LAYOUT_SIDEBAR_MINI = False
"""Sidebar Mini: use the .sidebar-mini class to show the sidebar when collapsed"""

THEME_LAYOUT_FIXED_FOOTER = True
"""Fixed Footer: use the class .layout-footer-fixed to get a fixed footer."""

THEME_LAYOUT_FIXED_SIDEBAR = True
"""Fixed Sidebar: adds the class .layout-fixed to get a fixed sidebar."""

THEME_LAYOUT_FIXED_TOP_NAV = True
"""Fixed Navbar: use the class .layout-navbar-fixed to get a fixed navbar."""

THEME_LAYOUT_TOP_NAV = False
"""Top Navigation: use the class .layout-top-nav to remove the sidebar and have your links at the top navbar."""


class ThemeColor:
    """Color styles."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"

    WHITE = "white"
    BLACK = "black"
    GRAY_DARK = "gray-dark"
    GRAY = "gray"
    LIGHT = "light"

    INDIGO = "indigo"
    LIGHTBLUE = "lightblue"
    NAVY = "navy"
    PURPLE = "purple"
    FUCHSIA = "fuchsia"
    PINK = "pink"
    MAROON = "maroon"
    ORANGE = "orange"
    LIME = "lime"
    TEAL = "teal"
    OLIVE = "olive"

    GRADIENT_PRIMARY = "gradient-primary"
    GRADIENT_SUCCESS = "gradient-success"
    GRADIENT_DANGER = "gradient-danger"
    GRADIENT_WARNING = "gradient-warning"
    GRADIENT_INFO = "gradient-info"


__all__ = ("ThemeColor",)
