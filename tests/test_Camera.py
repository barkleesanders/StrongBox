from pathlib import Path
from unittest.mock import Mock

import numpy as np

import Camera


def test_missing_camera_releases_driver(monkeypatch):
    device = Mock()
    device.isOpened.return_value = False
    monkeypatch.setattr(Camera.cv2, "VideoCapture", Mock(return_value=device))
    camera = Camera.Camera(camera_index=99)
    assert camera.take_picture() is None
    assert camera.numOfPhotos == 0
    device.release.assert_called_once()


def test_captured_frame_is_written_and_driver_released(monkeypatch, tmp_path):
    device = Mock()
    device.isOpened.return_value = True
    device.read.return_value = (True, np.zeros((32, 32, 3), dtype=np.uint8))
    monkeypatch.setattr(Camera.cv2, "VideoCapture", Mock(return_value=device))
    monkeypatch.setattr(Camera, "__file__", str(tmp_path / "Camera.py"))
    camera = Camera.Camera()
    result = camera.take_picture()
    assert Path(result).is_file()
    assert Camera.cv2.imread(result).shape == (32, 32, 3)
    assert camera.numOfPhotos == 1
    device.release.assert_called_once()


def test_failed_write_is_not_reported_as_saved(monkeypatch, tmp_path):
    device = Mock()
    device.isOpened.return_value = True
    device.read.return_value = (True, np.zeros((32, 32, 3), dtype=np.uint8))
    monkeypatch.setattr(Camera.cv2, "VideoCapture", Mock(return_value=device))
    monkeypatch.setattr(Camera.cv2, "imwrite", Mock(return_value=False))
    monkeypatch.setattr(Camera, "__file__", str(tmp_path / "Camera.py"))
    camera = Camera.Camera()
    assert camera.take_picture() is None
    assert camera.numOfPhotos == 0
    device.release.assert_called_once()
