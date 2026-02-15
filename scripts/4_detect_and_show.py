
import cv2
import mediapipe as mp
import numpy as np
import sys
import os

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
except ImportError:
    import mediapipe.python.solutions.holistic as mp_holistic
    import mediapipe.python.solutions.drawing_utils as mp_drawing
    import mediapipe.python.solutions.drawing_styles as mp_drawing_styles

def crop_center_square(frame):
    h, w = frame.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

def resize_with_padding(image, target_size=800):
    h, w = image.shape[:2]
    scale = target_size / max(h, w)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h))
    
    # Create black canvas
    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    
    # Center image
    x_offset = (target_size - new_w) // 2
    y_offset = (target_size - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas

def main():
    cap = cv2.VideoCapture(0)
    
    # Window setup
    cv2.namedWindow('Skeleton Debug', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Meme Output', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Skeleton Debug', 800, 800)
    cv2.resizeWindow('Meme Output', 800, 800)

    # Font Setup (Notepad-style: Monospace/Small)
    # FONT_HERSHEY_COMPLEX_SMALL usually looks clean and techy
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    font_scale = 0.9
    font_color = (0, 255, 0) # Green text
    font_thick = 1

    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1
    ) as holistic:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            # 1. Process MediaPipe (ON ORIGINAL IMAGE to preserve Left/Right handedness)
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image_rgb)

            # 2. Draw Skeleton (On Original)
            image.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            # 3. Detect Gesture (On Original Coordinates)
            detected_gesture = engine.detect_gesture(results)

            # 4. Flip horizontally NOW (For Mirror View Display)
            image = cv2.flip(image, 1)
            
            # 5. Crop to Square (for display)
            debug_frame = crop_center_square(image)
            debug_frame = cv2.resize(debug_frame, (800, 800))
            
            # 6. Draw Status Text (After Flip, so it's readable)
            status_text = f"STATUS: {detected_gesture if detected_gesture else 'IDLE'}"
            color = (0, 255, 0) if detected_gesture else (200, 200, 200) # Green or Grey
            
            # Add text background strip for readability? Optional.
            # cv2.rectangle(debug_frame, (0,0), (800, 40), (0,0,0), -1)
            
            cv2.putText(debug_frame, status_text, (20, 40), 
                        font, font_scale, color, font_thick, cv2.LINE_AA)

            # 7. Get Meme (and resize to 800x800 square with padding)
            raw_meme = switcher.get_frame(detected_gesture)
            meme_frame = resize_with_padding(raw_meme, 800)

            # Display
            cv2.imshow('Skeleton Debug', debug_frame)
            cv2.imshow('Meme Output', meme_frame)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
