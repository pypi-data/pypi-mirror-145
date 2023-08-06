from flask_theme_adminlte3.app import create_app

def test_home_exists():
    app = create_app()

    client = app.test_client()

    resp = client.get('/home')

    assert resp.status_code == 200