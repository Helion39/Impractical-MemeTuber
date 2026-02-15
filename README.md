# Impractical PNG-tuber With Memes

> **⚠️ IMPORTANT PROMPT FOR ALL AGENTS / CONTRIBUTORS:**
>
> 1. ALWAYS UPDATE THIS LOG when making any change, fix, or progress -- no matter how small.
> 2. ALWAYS SHOW DATES in the format YYYY-MM-DD HH:MM (24-hour, UTC+7 Jakarta time).
> 3. NEVER DELETE PROGRESS -- even if a task is completed, keep the log entry and mark it as ✅ DONE.
> 4. ADD NEW ENTRIES AT THE TOP of each section's log (newest first).
> 5. When starting work on any task, update its status to 🔄 IN PROGRESS.
> 6. When completing a task, update its status to ✅ DONE and add a summary of what was done.
> 7. If a task is blocked, mark it as 🚫 BLOCKED with a reason.
> 8. Reference commit hashes where applicable.

## Change Log
- 2026-02-15 09:49: ✅ DONE Updated log instructions to use numbered list.
- 2026-02-15 09:47: ✅ DONE Added standard log instructions and Change Log section.

This project aims to create a gesture-controlled virtual camera that replaces your webcam feed with meme images based on your body language.

## Purpose
- Detect specific body poses (e.g., Facepalm, Peace Sign, Shrug).
- Trigger corresponding Meme Images (PNGs) to be displayed on a virtual camera.
- Utilizes computer vision (MediaPipe or YOLO) to interpret poses without extensive training.

## Usage
1. Place your meme images in the `assets/memes` directory.
2. Define the pose triggers in `memes_list.md`.
3. Run the application to start the virtual camera.

## Technology Stack
- **Python**: Core logic.
- **OpenCV**: Image capture and processing.
- **MediaPipe / YOLO**: Pose estimation and gesture recognition.
- **PyVirtualCam**: To output the frames to OBS/Zoom/Discord.
