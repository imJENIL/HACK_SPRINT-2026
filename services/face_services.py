import os
import pickle
import threading
from datetime import datetime

import cv2
import numpy as np
import face_recognition

DATA_PATH = r"C:\Users\jenil\OneDrive\Desktop\HACK_SPRINT\data\faces"
os.makedirs(DATA_PATH, exist_ok=True)

FACE_MATCH_THRESHOLD = 0.4
RESIZE_SCALE = 0.5  # Speed vs accuracy tradeoff

_encodings_cache = {}
_cache_lock = threading.Lock()

def load_encodings_cache():
    """
    Load all saved face encodings into memory once.
    Called at server startup.
    """
    with _cache_lock:
        _encodings_cache.clear()

        for file in os.listdir(DATA_PATH):
            if not file.endswith(".pkl"):
                continue

            path = os.path.join(DATA_PATH, file)
            try:
                with open(path, "rb") as f:
                    data = pickle.load(f)

                name = data["name"]
                _encodings_cache[name] = data
            except Exception as e:
                print(f"[face_service] Failed to load {file}: {e}")


def get_registered_faces():
    """Return metadata only (safe for API exposure)."""
    with _cache_lock:
        return [
            {
                "name": data["name"],
                "registered_at": data.get("registered_at", "unknown")
            }
            for data in _encodings_cache.values()
        ]

def encode_face(frame):
    """
    Encode a single face from a frame.
    Returns: (encoding | None, error_message | None)
    """
    try:
        # Resize for speed
        small = cv2.resize(frame, (0, 0), fx=RESIZE_SCALE, fy=RESIZE_SCALE)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(
            rgb, model="hog", number_of_times_to_upsample=1
        )

        if not locations:
            return None, "No face detected"

        if len(locations) > 1:
            return None, "Multiple faces detected"

        encodings = face_recognition.face_encodings(
            rgb, locations, num_jitters=1
        )

        if not encodings:
            return None, "Failed to encode face"

        return encodings[0], None

    except Exception as e:
        return None, f"Encoding error: {str(e)}"

def save_face(name, encoding):
    """
    Persist encoding to disk and cache.
    """
    with _cache_lock:
        if name in _encodings_cache:
            return False, "Student already registered"

        data = {
            "name": name,
            "encoding": encoding,
            "registered_at": datetime.now().isoformat()
        }

        try:
            path = os.path.join(DATA_PATH, f"{name}.pkl")
            with open(path, "wb") as f:
                pickle.dump(data, f)

            _encodings_cache[name] = data
            return True, None

        except Exception as e:
            return False, str(e)

def match_face(encoding):
    """
    Match a face encoding against cached faces.
    Returns: (name | None, distance | None)
    """
    with _cache_lock:
        if not _encodings_cache:
            return None, None

        known_encodings = [
            data["encoding"] for data in _encodings_cache.values()
        ]
        known_names = list(_encodings_cache.keys())

    distances = face_recognition.face_distance(
        known_encodings, encoding
    )

    best_index = np.argmin(distances)
    best_distance = distances[best_index]

    if best_distance < FACE_MATCH_THRESHOLD:
        return known_names[best_index], float(best_distance)

    return None, float(best_distance)

def delete_face(name):
    """
    Remove a registered face.
    """
    with _cache_lock:
        if name not in _encodings_cache:
            return False

        try:
            os.remove(os.path.join(DATA_PATH, f"{name}.pkl"))
            _encodings_cache.pop(name, None)
            return True
        except Exception:
            return False
