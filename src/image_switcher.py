
import cv2
import os
import numpy as np
from PIL import Image

class ImageSwitcher:
    def __init__(self, assets_dir):
        self.assets_dir = assets_dir
        self.memes = {}
        self.load_memes()
        self.current_meme = "IDLE"
        self.last_shown = "IDLE"
        
        # Default frame (black)
        self.default_frame = np.zeros((720, 1280, 3), dtype=np.uint8)

    def load_memes(self):
        # Specific mapping based on your file list
        # Key = Gesture Name (returned by engine), Value = Filename
        mapping = {
            "Waduh": "Waduh(One_Hand_On_Top_Of_Head).jpg",
            "MilesMorales": "MilesMorales(Two_Hands_Behind_Head).png",
            "FreakyCat": "FreakyCat(Tongue_Out).jpg",
            "MewingCat": "MewingCat(Finger_On_Mouth_Vertical).gif", # GIF support TBD (using first frame for now)
            "SneakyGolem": "SneakyGolem(Holding_Mouth_With_One_Hand).jpg",
            "PointingSelf": "Pointing_FInger_At_Self.png",
            # "CatLaugh": "CatLaugh(Pointing_Finger_At_You).gif", # Ignored/Hard
            "IDLE": "idle.png"
        }

        print("Loading memes...")
        for name, filename in mapping.items():
            path = os.path.join(self.assets_dir, filename)
            if os.path.exists(path):
                try:
                    # Use PIL to load to handle formats, then convert to OpenCV
                    pil_img = Image.open(path).convert('RGB') # Remove alpha for now (simple background)
                    pil_img = pil_img.resize((1280, 720))     # Force resize to HD
                    cv_img = np.array(pil_img)
                    cv_img = cv_img[:, :, ::-1].copy()       # RGB to BGR for OpenCV display
                    self.memes[name] = cv_img
                    print(f"Loaded: {name}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
            else:
                print(f"Warning: {filename} not found! (Using black screen for {name})")
                self.memes[name] = np.zeros((720, 1280, 3), dtype=np.uint8)

    def get_frame(self, gesture_name):
        """Returns the image frame for the given gesture."""
        if gesture_name is None:
            gesture_name = "IDLE"
            
        if gesture_name in self.memes:
            return self.memes[gesture_name]
        return self.memes.get("IDLE", self.default_frame)
