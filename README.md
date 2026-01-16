# AI Virtual Mouse using Hand Gestures

An AI-powered virtual mouse system that enables hands-free control of cursor movement and mouse actions using real-time hand gestures captured via a webcam.

The system leverages computer vision and hand landmark detection to replace traditional mouse interactions with intuitive hand gestures.

---

## ✨ Features

- Cursor movement using index finger
- Left click using index + middle finger
- Right click using thumb + index finger
- Scroll up and down using finger combinations
- Double click using three-finger gesture
- Real-time gesture instruction panel
- Live action feedback (FPS & current action)
- Smooth cursor movement with noise reduction

---

## 🛠️ Tech Stack

- **Python** – Core programming language  
- **OpenCV** – Video capture and image processing  
- **MediaPipe** – Hand landmark detection  
- **NumPy** – Mathematical computations  
- **AutoPy** – System-level mouse control  
- **PyAutoGUI** – Scrolling and system interactions  

---

## 📁 Project Structure

```text
Virtual-Mouse/
│
├── assets/
│   ├── move.png
│   ├── left_click.png
│   ├── right_click.png
│   ├── scroll_up.png
│   ├── scroll_down.png
│   └── double_click.png
│
├── HandtrackingModule.py
├── Virtual_Mouse.py
├── requirements.txt
└── README.md
```
---

## 🧠 How It Works

1. The webcam captures live video frames.
2. MediaPipe detects hand landmarks in real time.
3. Specific finger combinations are recognized as gestures.
4. Hand coordinates are mapped to screen coordinates.
5. Mouse actions are triggered using system-level automation libraries.
6. A visual instruction panel guides users with supported gestures.

---

## 👤 Author

**Sai B**  
Computer Science Engineer | Data Science & Computer Vision Enthusiast  
  
