
import cv2
import mediapipe as mp
import numpy as np

# Handle MediaPipe solutions import (Win/Py3.11 quirk)
try:
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
except AttributeError:
    import mediapipe.python.solutions.holistic as mp_holistic
    import mediapipe.python.solutions.drawing_utils as mp_drawing
    import mediapipe.python.solutions.drawing_styles as mp_drawing_styles

def detect_waduh_thread():
    cap = cv2.VideoCapture(0)
    
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1
    ) as holistic:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image_rgb)

            image.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            
            # Draw Pose skeleton
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            # WADUH DETECTION LOGIC
            is_waduh = False
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                # Get key points (0=Nose, 15=L_Wrist, 16=R_Wrist)
                nose = landmarks[0]
                left_wrist = landmarks[15]
                right_wrist = landmarks[16]
                
                # Check Right Hand ONLY (as requested)
                # Note: In MediaPipe, 16 is Right Wrist.
                if right_wrist.visibility > 0.5:
                    if right_wrist.y < (nose.y - 0.1):
                        if abs(right_wrist.x - nose.x) < 0.2:
                            is_waduh = True

            # FLIP IMAGE NOW (so text isn't mirrored)
            image = cv2.flip(image, 1)

            # Display Result
            if is_waduh:
                cv2.putText(image, "WADUH DETECTED!", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("WADUH!")

            cv2.imshow('Waduh Detector', image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_waduh_thread()
