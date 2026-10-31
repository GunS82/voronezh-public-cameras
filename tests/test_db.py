import pytest
import os
import sqlite3
from src.db import init_db, save_camera, get_all_cameras, DB_PATH

@pytest.fixture(autouse=True)
def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_save_and_get_camera():
    cam = {
        'id': 'test-123',
        'title': 'Test Cam',
        'url': 'http://test.com',
        'operator': 'test-op',
        'category': 'test-cat',
        'status': 'works',
        'confidence': 'high',
        'lat': 51.0,
        'lng': 39.0,
        'address': 'Test addr'
    }
    save_camera(cam)
    cams = get_all_cameras()
    assert len(cams) == 1
    assert cams[0]['id'] == 'test-123'
    assert cams[0]['title'] == 'Test Cam'
