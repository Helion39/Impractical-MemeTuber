# TODO — Impractical PNGTuber With Memes

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

> Created: 2026-02-15
> Status: 🟡 Phase 3: Coding "Waduh" Detector

---

## Phase 0: Environment Setup
- [x] Install Python 3.11 (via winget)
- [x] Create virtual environment (`python -m venv venv`)
- [x] Install core dependencies (mediapipe, opencv, etc.)


- [ ] Install core dependencies:
  ```
  pip install mediapipe opencv-python numpy Pillow pyvirtualcam
  ```
- [ ] Verify OBS Studio is installed (needed for virtual camera backend on Windows)
- [ ] Test webcam access with a simple OpenCV script

---

## Phase 1: Mirror Test (Skeleton Viewer) 🪞
> **Goal:** See your skeleton in real-time. Confirm camera + lighting works.

- [ ] Create `scripts/1_mirror_test.py`
  - [ ] Open webcam with OpenCV
  - [ ] Run MediaPipe Holistic on each frame
  - [ ] Draw Pose skeleton (33 pts) on screen
  - [ ] Draw Hand landmarks (21 pts per hand) on screen
  - [ ] Draw Face Mesh (468 pts) on screen
  - [ ] Display FPS counter
  - [ ] Press `Q` to quit
- [ ] **TEST:** Can you see all 3 layers (body, hands, face) clearly?
- [ ] **TEST:** Move around — does the skeleton follow smoothly?

---

## Phase 2: Pose Recorder (Snapshot Tool) 📸
> **Goal:** Save your "meme poses" as JSON data files.

- [ ] Create `scripts/2_record_pose.py`
  - [ ] Show live skeleton (reuse Phase 1 code)
  - [ ] Display instructions on screen ("Strike a pose, press SPACE to save")
  - [ ] On SPACE press:
    - [ ] Capture all landmark coordinates (Pose + Hands + Face)
    - [ ] Normalize landmarks (relative to body center, scale-independent)
    - [ ] Calculate key joint angles (elbows, shoulders, wrists)
    - [ ] Save to `poses/[meme_name].json`
  - [ ] Allow typing a meme name via console input
  - [ ] Press `Q` to quit
- [ ] Create `poses/` directory
- [ ] **TEST:** Record all 7 meme poses and verify JSON files are saved

---

## Phase 3: Gesture Engine (The Brain) 🧠
> **Goal:** Real-time comparison of live skeleton vs saved poses.

- [ ] Create `src/gesture_engine.py` (Started)
  - [ ] Implement rule-based detectors for each meme:


### Per-Meme Detection Rules

| # | Meme | Rule | Priority |
|---|------|------|----------|
| 1 | **FreakyCat** (Tongue Out) | Face mesh: mouth open ratio > threshold | 🔴 Hard |
| 2 | **MewingCat** (Shhh) | Hand index tip near face mouth + 1 finger extended | 🔴 Hard |
| 3 | **MilesMorales** (Hands Behind Head) | Both wrists above & behind ears | 🟢 Easy |
| 4 | **Pointing At Self** | Index finger extended toward own chest | 🟡 Medium |
| 5 | **SneakyGolem** (Hand on Mouth) | Palm near mouth + multiple fingers extended | 🟡 Medium |
| 6 | **Waduh** (Hand on Head) | One wrist above nose, palm down | 🟢 Easy |
| 7 | **CatLaugh** (Point at Camera) | Index extended + smallest Z-depth | 🔴 Hard |

  - [ ] Implement confidence scoring (0.0 - 1.0) for each gesture
  - [ ] Implement cooldown timer (prevent flickering between memes)
  - [ ] Implement "idle" state (no gesture matched → default image)
  - [ ] **TEST:** Print detected gesture name to console in real-time

---

## Phase 4: Image Switcher (The Face) 🎭
> **Goal:** Display the correct meme image when a gesture is detected.

- [ ] Create `src/image_switcher.py`
  - [ ] Load all meme images from `assets/memes/`
  - [ ] Handle PNG (static) and GIF (animated) formats
  - [ ] Resize meme images to match virtual camera resolution (e.g., 1280x720)
  - [ ] On gesture match → display corresponding meme
  - [ ] On no match → display idle/default image
  - [ ] Smooth transition (fade or instant swap — TBD)
- [ ] Create/find a default idle image (`assets/memes/idle.png`)
- [ ] **TEST:** Manually trigger each meme and verify it displays correctly

---

## Phase 5: Virtual Camera Output 📹
> **Goal:** Make OBS/Discord/Zoom see the meme images as your "webcam."

- [ ] Create `src/virtual_cam.py`
  - [ ] Initialize `pyvirtualcam` with OBS backend
  - [ ] Set resolution to 1280x720 @ 20 FPS
  - [ ] Pipe the output from Image Switcher to virtual cam
  - [ ] Handle color space conversion (BGR → RGB for pyvirtualcam)
- [ ] **TEST:** Open Discord/Zoom → check if "OBS Virtual Camera" shows meme images
- [ ] **TEST:** Open OBS → add "Video Capture Device" → select virtual cam

---

## Phase 6: Main App (All Together) 🚀
> **Goal:** Single script that runs everything.

- [ ] Create `main.py`
  - [ ] Initialize webcam
  - [ ] Initialize MediaPipe Holistic
  - [ ] Initialize Gesture Engine (load poses)
  - [ ] Initialize Image Switcher (load memes)
  - [ ] Initialize Virtual Camera
  - [ ] Main loop:
    1. Read webcam frame
    2. Process with MediaPipe → get landmarks
    3. Pass landmarks to Gesture Engine → get matched gesture
    4. Pass gesture to Image Switcher → get meme image
    5. Send meme image to Virtual Camera
    6. (Optional) Show debug window with skeleton overlay
  - [ ] Press `Q` to quit
  - [ ] Clean up resources on exit

---

## Phase 7: Polish & QoL ✨
> **Goal:** Make it actually usable for streaming.

- [ ] Add config file (`config.json`) for:
  - [ ] Webcam device index
  - [ ] Resolution
  - [ ] Confidence thresholds per gesture
  - [ ] Cooldown timer duration
  - [ ] Debug mode on/off
- [ ] Add on-screen overlay showing current detected gesture (debug mode)
- [ ] Add sound effects on gesture trigger (optional, fun)
- [ ] Handle edge cases:
  - [ ] No webcam found
  - [ ] MediaPipe fails to detect (poor lighting)
  - [ ] Multiple gestures detected simultaneously (priority system)
- [ ] GIF animation support (frame-by-frame playback for animated memes)
- [ ] Performance profiling and optimization

---

## Phase 8 (Future): GUI & Ease of Use 🎨
> **Goal:** Make it easy for non-technical users.

- [ ] Simple GUI (Tkinter or web-based) with:
  - [ ] Live preview window
  - [ ] "Record New Pose" button
  - [ ] Drag-and-drop meme image upload
  - [ ] Gesture sensitivity sliders
  - [ ] Start/Stop toggle
- [ ] Package as standalone `.exe` (PyInstaller or similar)

---

## File Structure (Target)

```
Impractical_PNG-tuber_With_Memes/
├── main.py                          # Entry point
├── config.json                      # Settings
├── requirements.txt                 # pip dependencies
├── README.md                        # Project overview
├── RESEARCH_AND_REFERENCE.md        # Tech research
├── TODO.md                          # This file
├── memes_list.md                    # Meme catalog
│
├── assets/
│   └── memes/
│       ├── idle.png                 # Default "no gesture" image
│       ├── FreakyCat(Tongue_Out).jpg
│       ├── MewingCat(Finger_On_Mouth_Vertical).gif
│       ├── MilesMorales(Two_Hands_Behind_Head).png
│       ├── Pointing_FInger_At_Self.png
│       ├── SneakyGolem(Holding_Mouth_With_One_Hand).jpg
│       ├── Waduh(One_Hand_On_Top_Of_Head).jpg
│       └── CatLaugh(Pointing_Finger_At_You).gif
│
├── poses/                           # Saved pose snapshots (JSON)
│   ├── freaky_cat.json
│   ├── mewing_cat.json
│   ├── miles_morales.json
│   ├── pointing_self.json
│   ├── sneaky_golem.json
│   ├── waduh.json
│   └── cat_laugh.json
│
├── scripts/                         # Development/testing scripts
│   ├── 1_mirror_test.py             # Phase 1: See your skeleton
│   └── 2_record_pose.py             # Phase 2: Save pose snapshots
│
└── src/                             # Core modules
    ├── __init__.py
    ├── gesture_engine.py            # Phase 3: Gesture detection logic
    ├── image_switcher.py            # Phase 4: Meme display logic
    └── virtual_cam.py               # Phase 5: Virtual camera output
```

---

## Priority Order (What to build first)

1. 🟢 **Phase 0** — Setup (5 min)
2. 🟢 **Phase 1** — Mirror Test (30 min) — *Proves the AI works*
3. 🟡 **Phase 3** — Gesture Engine for EASY memes first:
   - `Waduh` (hand on head) — easiest to detect
   - `MilesMorales` (hands behind head) — second easiest
4. 🟡 **Phase 4** — Image Switcher (show the meme on screen)
5. 🟡 **Phase 5** — Virtual Camera (so OBS can see it)
6. 🔴 **Phase 3 continued** — Hard memes:
   - `SneakyGolem` (hand on mouth)
   - `Pointing At Self` (finger direction)
   - `MewingCat` (shhh — finger on lips)
   - `FreakyCat` (tongue out)
   - `CatLaugh` (pointing at camera)
7. 🟢 **Phase 6** — Combine everything into `main.py`
8. ⚪ **Phase 7-8** — Polish (later)

---

## Notes
- Skip Phase 2 (Pose Recorder) initially. Start with hardcoded rules for the easy memes.
- Only build the recorder if the rule-based approach becomes too tedious.
- GIF support can wait — static frame display is fine for the prototype.
- Every phase should be independently testable before moving to the next.
