import numpy as np

from ComputerVision import ComputerVision


def test_edge_detection_on_synthetic_frame():
    frame = np.zeros((64, 64), dtype=np.uint8)
    frame[16:48, 16:48] = 255
    edges = ComputerVision().auto_canny(frame)
    assert edges.shape == frame.shape
    assert edges.dtype == np.uint8
    assert np.count_nonzero(edges) > 0
    assert set(np.unique(edges)) <= {0, 255}
