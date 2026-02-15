
import cv2
import mediapipe as mp
import numpy as np

class GestureEngine:
    def __init__(self):
        # We don't save poses to JSON for rule-based detection yet.
        # This engine analyzes live landmarks frame-by-frame.
        pass

    def detect_gesture(self, results):
        """
        Input: MediaPipe Holistic results object
        Output: String (name of detected meme) or None
        """
        
        # 1. Check for WADUH (Hand on Head)
        # ---------------------------------------------------------------------
        # Logic: 
        # - Wrist (15 or 16) is ABOVE Nose (0)
        # - Wrist.y < Nose.y (Remember: Y=0 is top of screen)
        # - High confidence: The "height difference" is significant
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Get key points
            nose = landmarks[0]
            left_wrist = landmarks[15]
            right_wrist = landmarks[16]
            
            # Check Right Hand Waduh ONLY
            if right_wrist.visibility > 0.5 and right_wrist.y < nose.y:
                if (nose.y - right_wrist.y) > 0.15:
                    return "Waduh"
        
        return None
