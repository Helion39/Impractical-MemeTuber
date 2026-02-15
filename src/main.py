
import cv2
import mediapipe as mp
import numpy as np
import sys
import os
import pyvirtualcam
import time

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gesture_engine import GestureEngine
from src.image_switcher import ImageSwitcher

switcher = ImageSwitcher('assets/memes')
engine = GestureEngine()

# Handle MediaPipe solutions import
try:
    import mediapipe.solutions.holistic as mp_holistic
    import mediapipe.solutions.drawing_utils as mp_drawing
    import mediapipe.solutions.drawing_styles as mp_drawing_styles
except (ImportError, AttributeError):
    import mediapipe.python.solutions.holistic as mp_holistic
    import mediapipe.python.solutions.drawing_utils as mp_drawing
    import mediapipe.python.solutions.drawing_styles as mp_drawing_styles

def crop_center_square(frame):
    h, w = frame.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

def resize_with_padding(image, target_size=(1280, 720)):
    # Resize keeping aspect ratio to fit into 1280x720 (or target size)
    h, w = image.shape[:2]
    target_w, target_h = target_size
    
    scale = min(target_w/w, target_h/h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h))
    
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas

def main():
    cap = cv2.VideoCapture(0)
    
    # Debug Window Setup
    cv2.namedWindow('Skeleton Debug', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Skeleton Debug', 600, 600)

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    
    print("Initializing Virtual Camera (1280x720 @ 30fps)...")
    
    # Initialize Virtual Camera
    # Note: If this fails, user likely needs OBS or Unity Capture installed.
    # We use 'obs' backend by default if available, or native.
    try:
        with pyvirtualcam.Camera(width=1280, height=720, fps=30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
            print(f"Virtual Camera Output: {cam.device}")
            
            with mp_holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
                model_complexity=1
            ) as holistic:
                
                while cap.isOpened():
                    success, image = cap.read()
                    if not success:
                        continue

                    # 1. Process MediaPipe (Original Image)
                    image.flags.writeable = False
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = holistic.process(image_rgb)

                    # 2. Draw Skeleton (Original)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                    mp_drawing.draw_landmarks(
                        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    
                    # 3. Detect Gesture
                    detected_gesture = engine.detect_gesture(results)

                    # 4. Debug Window Preparation
                    debug_frame = cv2.flip(image, 1) # Mirror for debugging
                    debug_frame = crop_center_square(debug_frame)
                    debug_frame = cv2.resize(debug_frame, (600, 600))
                    
                    status_text = f"STATUS: {detected_gesture if detected_gesture else 'IDLE'}"
                    color = (0, 255, 0) if detected_gesture else (200, 200, 200)
                    cv2.putText(debug_frame, status_text, (20, 40), font, 0.9, color, 1, cv2.LINE_AA)
                    cv2.imshow('Skeleton Debug', debug_frame)

                    # 5. Output to Virtual Camera
                    # Get Frame -> Resize to 1280x720
                    meme_frame = switcher.get_frame(detected_gesture)
                    
                    # Ensure meme_frame is correct size
                    if meme_frame.shape[:2] != (720, 1280):
                         # Usually loaded as 1280x720 in switcher, but just in case
                         meme_frame = cv2.resize(meme_frame, (1280, 720))

                    # Send to Virtual Cam
                    # pyvirtualcam expects RGB usually? or we specified BGR?
                    # We specified `fmt=pyvirtualcam.PixelFormat.BGR` so we can send OpenCV images directly!
                    cam.send(meme_frame)
                    cam.sleep_until_next_frame()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

    except Exception as e:
        print(f"Error starting Virtual Camera: {e}")
        print("Ensure you have OBS installed and 'Start Virtual Camera' is NOT active (it should be idle waiting for input, or just installed).")
        # Fallback loop if cam fails? No, just exit.

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
