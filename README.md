# 🎮 Dopamine Detox RPG
### A Gamified Digital Discipline & Screen Time Analytics Platform

Dopamine Detox RPG is a full-stack web application designed to combat excessive screen time and digital distraction using RPG-based gamification mechanics.

Built for **Pan India Hackathon 2026**, the platform tracks user activity, provides behavioral insights, and encourages healthy digital habits through rewards, XP systems, and progression mechanics.

---

## 🚀 Problem Statement

Excessive usage of high-dopamine applications (e.g., social media platforms) negatively affects productivity, focus, and mental well-being.  

Users lack:
- Awareness of their actual screen time
- Structured behavioral analytics
- Motivation systems to build discipline

Dopamine Detox RPG solves this by:
- Logging browsing sessions
- Analyzing usage patterns
- Converting discipline into gamified rewards
- Providing a dashboard with actionable insights

---

## 🏗 System Architecture

User Browser  
→ Chrome Extension logs usage  
→ Sends session data to Flask API  
→ Backend processes & stores analytics  
→ Dashboard visualizes insights  

---

## ✨ Core Features

### 🔹 Screen Time Tracking
- Logs website name
- Start time & end time
- Calculates session duration

### 🔹 Gamification Engine
- XP-based reward system
- RPG-style progression logic
- Achievement mechanics

### 🔹 Analytics Dashboard
- Usage breakdown
- Time distribution insights
- Performance feedback

### 🔹 Secure Backend API
- RESTful endpoints
- Structured modular architecture
- Environment variable support

---

## ⚔ Procrastination Combat Engine

Digital distractions are modeled as symbolic entities
(e.g., Procrastination Lich).

Users must:
- Complete discipline tasks
- Increase combat power
- Reduce corruption levels
- Avoid relapses

Failure increases corruption.
Victory grants XP and progression.
---

## 🛠 Tech Stack

### Backend
- Python 3.8+
- Flask
- SQLAlchemy
- PostgreSQL (Production)
- psycopg2-binary

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Extension
- Chrome Extension (Manifest V3)
- Background script
- Tab tracking events

### Deployment
- Render (Production hosting)
- Vercel-ready configuration included

---

## 📂 Project Structure

```
/app.py                  # Main Flask application entry point
/models                  # Database schema & ORM models
/routes                  # API route definitions
/services                # Business logic & analytics engine
/scripts                 # Setup & administrative scripts
/templates               # HTML (Jinja2) views
/static                  # CSS, JS, images, assets
/extension               # Chrome extension source code
/tests                   # Test cases
requirements.txt         # Python dependencies
vercel.json              # Vercel deployment config
README.md
```

---

## ⚙️ Installation & Setup (Local)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/CodeWithShrey-collab/PIH2026_BugBashers.git
cd PIH2026_BugBashers
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

Copy environment template:

```bash
cp .env.example .env
```

Update:
- SECRET_KEY
- DATABASE_URL

---

### 4️⃣ Setup Database

```bash
python scripts/setup_project.py
```

---

### 5️⃣ Run Application

```bash
python app.py
```

Application runs at:

```
http://localhost:5000
```

---

## 🌍 Live Deployment

Production URL:

```
https://dopaminereset.onrender.com/
```

---

## 🔌 Chrome Extension Setup

1. Go to `chrome://extensions/`
2. Enable Developer Mode
3. Click "Load Unpacked"
4. Select `/extension` folder

The extension will:
- Track tab activity
- Capture session duration
- Send data to backend API

---

## 🔐 Environment Variables

Required:

```
SECRET_KEY=
DATABASE_URL=
```

---

## 📊 Data Flow

1. User opens a tracked website
2. Extension records start time
3. On tab close → data sent to backend
4. Backend calculates duration
5. Analytics engine updates XP & stats
6. Dashboard reflects progress

---

## 🧠 Innovation Highlights

- Behavioral discipline through gamification
- Structured modular backend
- Real-time usage analysis
- Scalable architecture
- Hackathon-ready deployment setup

---

## 👨‍💻 Contributors

- Hanshal Bobate  
- CodeWithShrey-collab  

---

## 📌 Future Enhancements

- AI-based behavioral prediction
- Personalized productivity recommendations
- Multi-device sync
- Mobile companion app
- Advanced leaderboard system

---

## 📜 License

This project was developed for academic and hackathon purposes (Pan India Hackathon 2026).
