# Research & Reference

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

> Last updated: 2026-02-15

---

## 1. Project Concept

**"Impractical PNGTuber With Memes"** — A program that replaces your webcam feed with meme images (PNGs/GIFs) based on real-time body/hand/face gesture detection. Built for streaming comedy.

---

## 2. Similar Existing Projects

| Project | What it does | Limitation for us |
|---------|-------------|-------------------|
| **PyNGTuber** (Python, open-source) | PNGTuber app with face tracking, animations, GIFs, keyboard/MIDI triggers. | Tracks face only; no body/hand gestures. No "meme swapping" logic. |
| **PNGTuber Plus** (open-source, itch.io) | 2D PNG avatar with speaking/blinking animations. | Voice-only trigger. No pose detection. |
| **PngTuber Maker** (Steam, free) | Detects sound to swap between emotion PNGs. | Sound-only. No visual gesture recognition. |
| **Blabberize** | Browser-based face-controlled PNGTuber. | Face expressions only. No hands/body. |
| **Xpression Camera** | Real-time face swap onto any image. | Proprietary. Face-only. Not meme-oriented. |
| **Alterkon** | Real-time face tracking for PNGTubers. | Face-only. No hand/body awareness. |

### Verdict
**No existing project does what we want.** All current PNGTubers are either voice-triggered or face-only. None combine full-body + hand + face gesture detection to swap meme images. **This project is unique.**

---

## 3. Technology Decision: MediaPipe vs YOLO

### 3.1 Why NOT YOLO (v8/v10/v11)
| Feature | YOLO Pose | MediaPipe Holistic |
|---------|-----------|-------------------|
| Body keypoints | 17 (major joints) | 33 (detailed joints) |
| Hand tracking | ❌ None (wrist only) | ✅ 21 landmarks per hand (each finger) |
| Face mesh | ❌ None | ✅ 468 landmarks (lips, eyes, brows) |
| Finger detection | ❌ Cannot tell peace from fist | ✅ Detects individual finger positions |
| Tongue/mouth open | ❌ Not possible | ✅ Detectable via face mesh distances |
| Multi-person | ✅ Excellent | ⚠️ Single-person (fine for 1 streamer) |
| Speed (GPU) | 🚀 Very fast | ⚡ Fast enough (~25-30 FPS) |
| Speed (CPU) | ⚡ Fast | ⚡ Fast (optimized for CPU) |
| Training needed | ❌ Custom training for gestures | ✅ Zero training needed |

### 3.2 Why MediaPipe Holistic Wins for THIS Project
- **5 of 7 memes** require finger-level or face-level detection that YOLO simply cannot provide.
- MediaPipe gives us **543 landmarks** (Body + Hands + Face) in a single pass.
- **Zero training needed.** We use rule-based logic (math) instead of ML training.
- Single-person limitation is irrelevant — you are the only one on camera.

---

## 4. Core Libraries

| Library | Purpose | Install |
|---------|---------|---------|
| `mediapipe` | AI detection (pose, hands, face) | `pip install mediapipe` |
| `opencv-python` | Webcam capture + image processing | `pip install opencv-python` |
| `numpy` | Math operations (angle calc, distance) | `pip install numpy` |
| `pyvirtualcam` | Output frames as a virtual webcam | `pip install pyvirtualcam` |
| `Pillow` | Load PNG/GIF meme images with transparency | `pip install Pillow` |

### Virtual Camera Backends
- **Windows:** `pyvirtualcam` uses **OBS Virtual Camera** (built-in to OBS 28+).
  - ⚠️ Limitation: OBS must NOT be using its own virtual camera at the same time.
  - Alternative: Install **Unity Capture** driver for a separate virtual cam.
- **Workflow:** Python script → `pyvirtualcam` → Virtual Camera → OBS/Discord/Zoom picks it up as "webcam."

---

## 5. Meme-by-Meme Detection Strategy

### 5.1 FreakyCat — Tongue Out 👅
- **Detection:** Face Mesh (468 landmarks)
- **Logic:** Calculate distance between upper lip (landmark #13) and lower lip (landmark #14). If the inner mouth landmarks extend far beyond normal "open mouth" distance → tongue is likely out.
- **Landmark IDs:** Upper lip inner: 13, Lower lip inner: 14, Mouth corners: 61, 291
- **Threshold:** Mouth openness ratio > 0.15 of face height
- **Reference:** `github.com/aaronhubhachen/simple-mediapipe-project` (tongue-out detection)
- **Difficulty:** ⭐⭐⭐ (Medium — tongue vs open mouth is subtle)

### 5.2 MewingCat — Finger on Mouth (Shhh) 🤫
- **Detection:** Hand Landmarks + Face Mesh (combined)
- **Logic:**
  1. Detect index finger tip (Hand landmark #8).
  2. Detect mouth center (Face landmark #13).
  3. Calculate Euclidean distance between finger tip and mouth.
  4. If distance < threshold AND index finger is extended (other fingers curled) → "Shhh" gesture.
- **Threshold:** Distance < 40px (normalized)
- **Difficulty:** ⭐⭐⭐⭐ (Hard — requires cross-model coordination, Hand + Face)

### 5.3 MilesMorales — Two Hands Behind Head 😱
- **Detection:** Pose Landmarks (33 body points)
- **Logic:**
  1. Detect both wrists (Pose landmarks #15, #16).
  2. Detect head top / ears (Pose landmarks #7, #8).
  3. If both wrists are ABOVE the ears AND behind/near the head (Z-depth or X-position near ears) → trigger.
- **Threshold:** `wrist.y < ear.y` for both hands AND `abs(wrist.x - ear.x) < threshold`
- **Difficulty:** ⭐⭐ (Easy — large body movement, very distinct)

### 5.4 Pointing Finger At Self 👈
- **Detection:** Hand Landmarks + Pose Landmarks
- **Logic:**
  1. Detect index finger tip (Hand landmark #8) and index finger direction.
  2. Detect chest/torso center (midpoint of Pose landmarks #11, #12 — shoulders).
  3. If index finger is extended, pointing INWARD toward torso, and finger tip is near chest → trigger.
- **Difficulty:** ⭐⭐⭐ (Medium — need to determine pointing direction via finger joint angles)

### 5.5 SneakyGolem — Hand Over Mouth 🤭
- **Detection:** Hand Landmarks + Face Mesh
- **Logic:**
  1. Detect palm center (Hand landmark #0 or #9).
  2. Detect mouth region (Face landmarks #13, #14).
  3. If palm is near mouth AND multiple fingers are extended (open hand, not just one finger) → trigger.
  4. Differentiate from "Shhh" by checking: Shhh = 1 finger extended, Sneaky = whole hand.
- **Difficulty:** ⭐⭐⭐ (Medium — must distinguish from Shhh gesture)

### 5.6 Waduh — Hand On Top Of Head 😅
- **Detection:** Pose Landmarks + Hand Landmarks
- **Logic:**
  1. Detect wrist position (Pose landmark #15 or #16).
  2. Detect head top (estimated from Pose landmarks #0 Nose, offset upward).
  3. If one wrist is directly above the nose AND palm is facing down → trigger.
- **Difficulty:** ⭐⭐ (Easy — very distinct large movement)

### 5.7 CatLaugh — Pointing Finger At Camera 😂👉
- **Detection:** Hand Landmarks
- **Logic:**
  1. Detect index finger extended (Hand landmarks #5, #6, #7, #8 in a straight line).
  2. Check Z-depth: If index finger tip (landmark #8) has the *smallest Z value* (closest to camera) → pointing AT camera.
  3. Other fingers should be curled.
- **Difficulty:** ⭐⭐⭐⭐ (Hard — Z-depth is noisy; "pointing at camera" vs "pointing sideways" is tricky)

---

## 6. Pose Matching Approach: "Snapshot & Compare"

Instead of hardcoding every gesture rule, we use a **hybrid approach**:

### 6.1 Rule-Based (Primary)
- Simple geometric checks (distances, angles) for each gesture.
- Fast, deterministic, no false positives from unrelated poses.
- **Best for:** Waduh, Miles Morales (clear, distinct body poses).

### 6.2 Cosine Similarity (Secondary / Future)
- Save a "snapshot" of all 543 landmarks as a vector.
- Compare live landmarks to saved vectors using cosine similarity.
- If similarity > 0.85 → match.
- **Reference:** `github.com/siwonkh/mediapipe-pose-compare`
- **Best for:** Complex poses that are hard to describe with simple rules.

### 6.3 Joint Angle Comparison (Tertiary)
- Calculate angles at key joints (elbow, shoulder, wrist).
- Compare angles to saved reference angles.
- More robust to camera distance/position changes than raw coordinates.

---

## 7. Architecture Overview

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Webcam      │────▶│  MediaPipe        │────▶│  Gesture Engine  │
│  (Real Face) │     │  Holistic         │     │  (Rule Matching) │
└─────────────┘     │  - 33 Pose pts    │     │                  │
                    │  - 42 Hand pts    │     │  Compares live   │
                    │  - 468 Face pts   │     │  skeleton to     │
                    └──────────────────┘     │  saved triggers  │
                                             └────────┬─────────┘
                                                      │
                                            ┌─────────▼──────────┐
                                            │  Image Switcher     │
                                            │                     │
                                            │  Match? → Show Meme │
                                            │  No Match? → Idle   │
                                            └─────────┬──────────┘
                                                      │
                                            ┌─────────▼──────────┐
                                            │  PyVirtualCam       │
                                            │  (Virtual Webcam)   │
                                            │                     │
                                            │  OBS / Discord /    │
                                            │  Zoom sees this     │
                                            └────────────────────┘
```

---

## 8. Key MediaPipe Landmark Reference

### Pose Landmarks (33 points)
| ID | Name | Use for |
|----|------|---------|
| 0  | Nose | Head position reference |
| 7  | Left Ear | Head tracking |
| 8  | Right Ear | Head tracking |
| 11 | Left Shoulder | Torso/chest reference |
| 12 | Right Shoulder | Torso/chest reference |
| 13 | Left Elbow | Arm angle |
| 14 | Right Elbow | Arm angle |
| 15 | Left Wrist | Hand position (coarse) |
| 16 | Right Wrist | Hand position (coarse) |

### Hand Landmarks (21 points per hand)
| ID | Name | Use for |
|----|------|---------|
| 0  | Wrist | Hand base |
| 4  | Thumb Tip | Thumbs up detection |
| 8  | Index Finger Tip | Pointing, Shhh |
| 12 | Middle Finger Tip | Peace sign |
| 16 | Ring Finger Tip | Finger curl check |
| 20 | Pinky Tip | Finger curl check |

### Face Mesh Key Landmarks (out of 468)
| ID | Name | Use for |
|----|------|---------|
| 13 | Upper Lip (inner) | Mouth open detection |
| 14 | Lower Lip (inner) | Mouth open detection |
| 61 | Left Mouth Corner | Smile detection |
| 291 | Right Mouth Corner | Smile detection |
| 159 | Left Eye Upper | Eye tracking |
| 145 | Left Eye Lower | Blink detection |

---

## 9. Performance Considerations

- **Target FPS:** 15-20 FPS is sufficient for a PNGTuber (it's static images, not smooth video).
- **MediaPipe Holistic:** ~25-30 FPS on a modern CPU. Faster on GPU.
- **Optimization tricks:**
  - Process every 2nd or 3rd frame (skip frames).
  - Reduce webcam resolution to 640x480 (sufficient for skeleton detection).
  - Use `model_complexity=1` instead of `2` for faster processing.
- **Memory:** <500MB RAM total. Meme images are small PNGs.

---

## 10. References & Links

1. **MediaPipe Holistic Docs:** https://google.github.io/mediapipe/solutions/holistic
2. **MediaPipe Face Mesh Guide:** https://google.dev/mediapipe/solutions/vision/face_landmarker
3. **MediaPipe Hand Landmarks:** https://google.dev/mediapipe/solutions/vision/hand_landmarker
4. **PyVirtualCam (PyPI):** https://pypi.org/project/pyvirtualcam/
5. **Pose Compare (Cosine Similarity):** https://github.com/siwonkh/mediapipe-pose-compare
6. **Tongue-Out Detection:** https://github.com/aaronhubhachen/simple-mediapipe-project
7. **Mouth Open Detection:** https://github.com/ashraf-minhaj/Mouth-Opening-Detection
8. **PyNGTuber (Reference PNGTuber):** https://github.com/pyngtuber
9. **hand-gesture-engine (PyPI):** https://libraries.io/pypi/hand-gesture-engine
10. **OBS WebSocket Python:** https://pypi.org/project/obs-websocket-py/
