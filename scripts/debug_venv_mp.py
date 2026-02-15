
import sys
import os
import mediapipe as mp

print(f"Python Executable: {sys.executable}")
print(f"MediaPipe Version: {mp.__version__}")
print(f"MediaPipe Location: {os.path.dirname(mp.__file__)}")

try:
    import mediapipe.solutions
    print("✅ Successfully imported mediapipe.solutions")
    try:
        import mediapipe.solutions.holistic
        print("✅ Successfully imported mediapipe.solutions.holistic")
    except ImportError as e:
        print(f"❌ Failed to import holistic: {e}")
except ImportError as e:
    print(f"❌ Failed to import mediapipe.solutions: {e}")
    # Try alternate path
    try:
        import mediapipe.python.solutions
        print("✅ Found solutions under mediapipe.python.solutions")
    except ImportError as e2:
        print(f"❌ Failed under mediapipe.python.solutions: {e2}")

# List top-level attributes
print("\nDir(mp):", dir(mp))
