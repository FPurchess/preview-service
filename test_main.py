import io

from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

from main import app


def test_health_endpoint_succeeds():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200


def test_preview_endpoint_succeeds():
    client = TestClient(app)
    file = io.StringIO("plain text file data")
    response = client.post('/preview/100x100', files={'file': file})
    assert response.status_code == 200


def test_preview_endpoint_fails_on_empty_file():
    client = TestClient(app)
    response = client.post('/preview/100x100')
    assert response.status_code == 400


def test_preview_endpoint_fails_on_undetected_mimetype():
    client = TestClient(app)
    file = io.BytesIO()
    response = client.post('/preview/100x100', files={'file': file})
    assert response.status_code == 500
