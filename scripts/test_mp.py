
import mediapipe as mp
print(f"MediaPipe Version: {mp.__version__}")
try:
    print(f"Has solutions? {hasattr(mp, 'solutions')}")
    if hasattr(mp, 'solutions'):
        print(f"Solutions: {dir(mp.solutions)}")
except Exception as e:
    print(f"Error accessing solutions: {e}")

print(f"Dir(mp): {dir(mp)}")
