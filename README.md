# 🎓 Smart Face-Based Attendance System

A secure, real-time attendance system that uses live face recognition, professor-controlled sessions, and liveness detection to eliminate proxy and fake attendance.

---

## 📌 Problem Statement

Traditional attendance systems are:
- Time-consuming  
- Easy to manipulate (proxy attendance)  
- Ineffective for hybrid or online environments  

Students can mark attendance using photos, videos, or by sharing credentials.

**There is no strong verification of physical presence.**

---

## 💡 Our Solution

We built a **professor-controlled, face-based attendance system** where:

- Attendance can only start after professor authorization  
- Students must be physically present in front of a live camera  
- Liveness detection blocks photos and recorded videos  
- Duplicate and proxy attendance is automatically prevented  

This ensures **attendance integrity**, not just automation.

---

## 🚀 Features Offered

- Face-based attendance with high accuracy  
- Professor-controlled attendance sessions  
- Liveness detection (anti-photo & anti-video spoofing)  
- Real-time attendance marking  
- Firebase cloud database storage  
- Duplicate & proxy prevention  
- Student registration & management  
- Attendance logs with timestamps  
- Admin dashboard for monitoring  
- Secure role-based access control  

---

## 🧠 What Makes It Different?

Unlike basic face-recognition systems, this solution:

- Requires **explicit professor approval** to start attendance  
- Uses **liveness detection** to stop spoofing  
- Blocks attendance from remote locations  
- Prevents duplicate scans automatically  

It focuses on **trust, security, and fairness**, not just convenience.

---

## 🏗️ Architecture Overview

Frontend (HTML + Tailwind)  
↓  
Flask REST APIs  
↓  
Face Recognition + Liveness Detection  
↓  
Firebase (Authentication & Firestore)

---

## 🔄 Process Flow

1. Professor logs in securely  
2. Professor starts attendance session  
3. Live camera feed activates  
4. Student scans face  
5. Liveness detection verifies real presence  
6. Face is matched with registered data  
7. Attendance is stored in Firebase  
8. Duplicate attempts are blocked  

---

## 🧪 Technologies Used

### Google Technologies
- Firebase Authentication  
- Firebase Firestore  
- Google MediaPipe (Face Mesh & landmarks)

### Other Technologies
- Python (Flask)  
- OpenCV  
- face_recognition (dlib)  
- HTML, Tailwind CSS, JavaScript  

---

## 🔐 Security & Privacy

- Attendance blocked without professor login  
- Liveness detection prevents spoofing attacks  
- No face data exposed through APIs  
- Firebase keys stored using environment variables  
- Sensitive data not committed to GitHub  

---


## ⚙️ How to Run Locally

```bash
git clone https://github.com/your-username/your-repo-name
cd your-repo-name
pip install -r requirements.txt
python app.py
