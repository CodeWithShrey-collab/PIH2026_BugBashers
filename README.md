# Dopamine Reset Platform — PIH 2026 🧠✨

Dopamine Reset is a state-of-the-art Behavioral Intelligence Engine and Predictive Attention Analytics Platform built for the KWARCS / Pan India Hackathon 2026. 

This platform acts as a Neuro-Inspired Focus Optimization System, designed to deeply analyze users' browsing habits, score their focus, and connect them with a network of peers to build accountability and break away from instant-gratification loops.

## Features & Subsystems Built

### Core Logging & Categorization
- **Automated Behavioral Tracking:** Ingests live telemetry (browsing data) and converts all timestamps reliably to Indian Standard Time (IST).
- **Intelligent Category Mapping:** A comprehensive mapping system of 100+ popular websites classifies traffic dynamically into `Social Media`, `Entertainment`, `Productivity`, `Shopping`, `News`, and `Browser`.

### Master Analytics (Phase 1)
- **Dopamine Scoring Engine:** Calculates a personalized score based on a proprietary algorithm weighing productivity versus distractions.
- **Behavioral Intelligence Dashboard:** Displays complex insights like *Time to First Distraction (TTFD)*, *Attention Fragmentation*, and *Burst Intensity*.
- **Peak Window Heatmaps:** Highlights the exact hours a user is most primed for peak performance vs. most vulnerable to distraction.

### The Network - Social Connectivity (Phase 2 & 3)
- **Secure Hex Codes:** Every user node is assigned a unique, secure 6-digit hex code upon registration.
- **Privacy-Safe Peer Telemetry:** Users can search and "link connections" (add friends) using hex codes. Viewing a peer's profile only exposes aggregate high-level metrics (Lifetime Points, Current Streak, Top Distraction) to protect granular privacy (Security Clearance Level 2).

### Syndicate (Guild) System (Phase 2 & 3)
- **Guild Creation & Operations:** Form a Syndicate (Guild) with a custom designation and an 8-character secure access code.
- **Aggregated Analytics:** View the real-time "Net Impact" (Total Points), "Total Focus" (Hours spent in Deep Work by all members collectively), and the "Top Distraction" (Primary entropy source) dragging the Syndicate down.
- **Internal Rankings:** Live leaderboards let operatives compete to maintain streaks and build Dopamine Points.

### AI-Driven Profile Dashboard (Phase 2)
- **Pseudo-AI Insight Generation:** An immersive, terminal-style interface that processes a user's behavioral footprint and live-types highly complex, jargon-heavy "AI Analyst" insights (e.g., *Warning: Amygdala hijack detected* or *Circadian Rhythm Alignment verified*).

## Tech Stack
- **Backend:** Python (Flask), Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite DB (`models.py` orchestrates `AppUsage`, `User`, `Guild`, and `Friendships`)
- **Frontend Engine:** Jinja Templating, Vanilla CSS, HTML5
- **Data Visualization:** Chart.js, Advanced Terminal UI Effects 
- **Time Manipulation:** `datetime` (UTC to IST timezone bridging)

## Setup & Running

1. Install dependencies (Flask, Flask-SQLAlchemy, Flask-Login, etc.):
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Run the database seeder to initialize mock operatives, behavior logs, and guilds:
   ```bash
   python seed_db.py
   ```
3. Boot the Flask Server:
   ```bash
   python app.py
   ```
4. Access the system via `http://127.0.0.1:5000`

---
*Created by the BugBashers team for PIH 2026. Breathe, Focus, Live.*
