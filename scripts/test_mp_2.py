
try:
    import mediapipe.python.solutions.holistic as mp_holistic
    print("Direct import succesful!")
except ImportError as e:
    print(f"Direct import failed: {e}")

import mediapipe
print(f" mediapipe path: {mediapipe.__path__}")
