import cv2
import mediapipe as mp
import time
import numpy as np

mp_face = mp.solutions.face_mesh

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, eye):
    p = [landmarks[i] for i in eye]
    v1 = np.linalg.norm(p[1] - p[5])
    v2 = np.linalg.norm(p[2] - p[4])
    h = np.linalg.norm(p[0] - p[3])
    return (v1 + v2) / (2.0 * h)

def check_liveness(frames):
    blink_detected = False
    movement_detected = False
    prev_nose_x = None

    with mp_face.FaceMesh(max_num_faces=1) as face_mesh:
        for frame in frames:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = face_mesh.process(rgb)

            if not res.multi_face_landmarks:
                return False, "No face detected"

            lm = res.multi_face_landmarks[0].landmark
            pts = np.array([[p.x, p.y] for p in lm])

            left_ear = eye_aspect_ratio(pts, LEFT_EYE)
            right_ear = eye_aspect_ratio(pts, RIGHT_EYE)
            ear = (left_ear + right_ear) / 2

            if ear < 0.26:
                blink_detected = True

            nose_x = pts[1][0]
            if prev_nose_x is not None and abs(nose_x - prev_nose_x) > 0.01:
                movement_detected = True

            prev_nose_x = nose_x

    if blink_detected or movement_detected:
        return True, "Liveness confirmed"

    return False, "Blink or head movement not detected"
