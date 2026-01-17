import cv2
import threading
import time

_camera = None
_lock = threading.Lock()

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 70


def get_camera():
    global _camera
    if _camera is None or not _camera.isOpened():
        _camera = cv2.VideoCapture(0)
        _camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        _camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        time.sleep(0.5)  # camera warm-up
    return _camera


def capture_frame():
    with _lock:
        cam = get_camera()
        if not cam.isOpened():
            return None

        ret, frame = cam.read()
        if not ret:
            return None

        return frame


def gen_frames():
    cam = get_camera()

    while True:
        with _lock:
            ret, frame = cam.read()

        if not ret:
            continue

        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )