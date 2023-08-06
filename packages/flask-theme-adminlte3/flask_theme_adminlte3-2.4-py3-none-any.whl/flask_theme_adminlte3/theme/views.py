from flask import current_app, render_template


def unauthorized(e):
    """Error handler to show a 401.html page in case of a 401 error."""
    return render_template(current_app.config["THEME_401_TEMPLATE"]), 401


def insufficient_permissions(e):
    """Error handler to show a 403.html page in case of a 403 error."""
    return render_template(current_app.config["THEME_403_TEMPLATE"]), 403


def page_not_found(e):
    """Error handler to show a 404.html page in case of a 404 error."""
    return render_template(current_app.config["THEME_404_TEMPLATE"]), 404


def too_many_requests(e):
    """Error handler to show a 429.html page in case of a 429 error."""
    return render_template(current_app.config["THEME_429_TEMPLATE"]), 429


def internal_error(e):
    """Error handler to show a 500.html page in case of a 500 error."""
    return render_template(current_app.config["THEME_500_TEMPLATE"]), 500
