
import cv2
import mediapipe as mp
import numpy as np

class GestureEngine:
    def __init__(self):
        # We don't save poses to JSON for rule-based detection yet.
        # This engine analyzes live landmarks frame-by-frame.
        pass

    def calculate_angle(self, a, b, c):
        """Calculates angle ABC (in degrees) at point B."""
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def detect_gesture(self, results):
        """
        Input: MediaPipe Holistic results object
        Output: String (name of detected meme) or None
        """
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Get key points
            nose = landmarks[0]
            left_ear = landmarks[7]
            right_ear = landmarks[8]
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            left_wrist = landmarks[15]
            right_wrist = landmarks[16]
            right_elbow = landmarks[14]
            right_shoulder = landmarks[12] # Redundant but fine

            # -------------------------------------------------------------
            # 1. Check for MILES MORALES (Two Hands Behind Head) FIRST!
            # -------------------------------------------------------------
            # Priority: High (Specific 2-hand pose overrides generic 1-hand poses)
            
            # Visibility Check (Use LOWER threshold because hands behind head are hard to see)
            if left_wrist.visibility > 0.3 and right_wrist.visibility > 0.3:
                # Height Check: Wrists ABOVE Shoulders
                if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
                    # Horizontal Check: Wrists near Ears (approx head width)
                    if abs(left_wrist.x - left_ear.x) < 0.2 and abs(right_wrist.x - right_ear.x) < 0.2:
                        return "MilesMorales"

            # -------------------------------------------------------------
            # 2. Check for WADUH (Right Hand on Head)
            # -------------------------------------------------------------
            if right_wrist.visibility > 0.5 and right_wrist.y < nose.y:
                vertical_dist = nose.y - right_wrist.y
                if 0.02 < vertical_dist < 0.25:
                    if abs(right_wrist.x - nose.x) < 0.12:
                        angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                        if angle < 130:
                            return "Waduh"

        
        return None
