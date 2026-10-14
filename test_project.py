from app import app
import pytest

def test_main():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_shoes():
    response = app.test_client().get("/shoes")
    assert response.status_code == 200


def test_register_page():
    response = app.test_client().get("/register")
    assert response.status_code == 200


def test_login_page():
    response = app.test_client().get("/login")
    assert response.status_code == 200