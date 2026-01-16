# AI-Based Virtual Mouse using Hand Gestures

AI Virtual Mouse is a computer vision–based system that enables users to control mouse movements and actions using real-time hand gestures captured through a webcam.

The project removes the need for a physical mouse by translating intuitive hand gestures into cursor movement, clicks, scrolling, and other mouse operations. It demonstrates a practical application of Human–Computer Interaction (HCI) using modern AI and vision techniques.

---

## 🚀 Features

- Cursor movement using index finger tracking  
- Left click using index + middle finger gesture  
- Right click using thumb + index finger gesture  
- Scroll up and scroll down using finger combinations  
- Double click using three-finger gesture  
- Real-time hand landmark detection  
- On-screen gesture instruction panel for user guidance  
- Active gesture feedback display  
- Smooth and stable cursor movement using motion smoothing  

---

## 🧠 How It Works

1. The webcam captures live video frames.
2. MediaPipe detects hand landmarks in real time.
3. Specific finger combinations are recognized as gestures.
4. Hand coordinates are mapped to screen coordinates.
5. Mouse actions are triggered using system-level automation libraries.
6. A visual instruction panel guides users with supported gestures.

---

## 🛠️ Tech Stack

- **Python** – Core programming language  
- **OpenCV** – Video capture and image processing  
- **MediaPipe** – Hand landmark detection  
- **NumPy** – Mathematical calculations  
- **AutoPy** – Mouse movement and click control  
- **PyAutoGUI** – Scrolling and system interactions  

---

## 📂 Project Structure

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

## 👤 Author

**Sai B**  
Computer Science Engineer | Data Science & Computer Vision Enthusiast  
  
