
import sys
import platform

print(f"Current Python Version: {sys.version}")

if sys.version_info >= (3, 12):
    print("\n❌ CRITICAL ERROR: Python version too new!")
    print("MediaPipe (needed for gestures) only supports Python 3.8 to 3.11.")
    print("You are running Python 3.12+ (likely 3.13).")
    print("\nPLEASE DO THIS:")
    print("1. Download Python 3.10 from: https://www.python.org/downloads/release/python-31011/")
    print("2. Run the installer.")
    print("3. Check 'Add Python 3.10 to PATH' during installation.")
    print("4. Restart your terminal/VS Code.")
    print("5. Run this script again to confirm.")
else:
    print("\n✅ Python version is compatible!")
