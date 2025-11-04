# 🕒 Freelancer Timer

[![Python](https://img.shields.io/badge/Built%20with-Python%203.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Data](https://img.shields.io/badge/Logs-CSV%20%2B%20JSON-orange.svg)]()

A simple, offline **time-tracking app for freelancers**, built with **Python (Tkinter)**.

It helps track client sessions, pause work, apply minimum billing, and calculate total earnings automatically. Each session is saved locally as a CSV log.

---

## 🧭 Version History

| File | Version | Key Features |
|------|----------|---------------|
| `timer_v1.py` | **v1** | Basic Start/Stop timer. Saves session time, project, and description to CSV. |
| `timer_v2.py` | **v2** | Adds **Pause/Continue** control to suspend and resume active timing. |
| `timer_v3.py` | **v3** | Adds **Hourly Rate (£)** input and automatic **earnings calculation**. |
| `timer_v3b.py` | **v3b** | Builds on v3: adds **pause tracking** (records total pause time). |
| `timer_v4.py` | **v4** | Introduces **Minimum Billable Time** logic for automatic billing floors. |
| `timer_v4b.py` | **v4b (Final)** | Combines **pause tracking + refined minimum logic** (blank/0 = no minimum). |

---

## 🧰 Tech Stack

- **Language:** Python 3.8+
- **GUI:** Tkinter (standard library)
- **Storage:** CSV (sessions), JSON (project list)
- **Packaging:** Optional via PyInstaller (.exe build)

No external dependencies are required.

---

## 📦 Installation

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/<your-username>/freelancer-timer.git
   cd freelancer-timer
   ```

2. *(Optional)* Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the latest version:**
   ```bash
   python timer_v4b.py
   ```

---

## 🖥️ How to Use

1. **Project Name**  → Select or enter a new project (stored in `projects.json`).
2. **Description**  → Optional text describing your task.
3. **Hourly Rate (£)** → Enter your hourly charge.
4. **Minimum Billable (min)** → Optional minimum billing floor (leave blank/0 for none).
5. **Start** → Begins tracking.
6. **Pause/Continue** → Stops/resumes active timing (pause time not billed).
7. **Stop** → Ends the session, calculates total & billable time, then saves to CSV.

Each record logs:
```
session_id, project_name, description, start_time, stop_time,
total_duration_min, paused_duration_min, billable_min, rate_gbp, earned_gbp
```

---

## 🧾 Example CSV Output

```
1, "Triple C Services", "Automation task", "2025-11-03 09:00:00", "2025-11-03 09:45:00", 45.0, 5.0, 45.0, 40, 30.0
2, "Harewood Green", "Property file setup", "2025-11-03 14:00:00", "2025-11-03 14:30:00", 30.0, 0.0, 60.0, 35, 35.0
```

---

## 🧩 Folder Structure

```
freelancer-timer/
├── timer_v1.py      # Start/Stop timer
├── timer_v2.py      # Adds Pause/Continue
├── timer_v3.py      # Adds Hourly Rate + Earnings
├── timer_v3b.py     # Adds Pause Tracking
├── timer_v4.py      # Adds Minimum Billable Time
├── timer_v4b.py     # Combines pause tracking + refined minimum logic
├── projects.json    # Project name list
├── sessions.csv     # Time log CSV
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧠 Future Roadmap

| Planned Feature | Description |
|------------------|--------------|
| **v5** | Save last-used hourly rate and min billable to `settings.json`. |
| **v6** | Summary window with totals per project and date range. |
| **v7** | Packaged `.exe` version for Windows (via PyInstaller). |
| **v8** | Optional client grouping & statistics dashboard. |

---

## 👤 Author

**Isaac Orzech**  
Freelancer & Automation Developer  
_Triple C Services Ltd — “IT Automated & Simplified”_