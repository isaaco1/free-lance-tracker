# Freelancer Timer v3 - Added Hourly Rate + £ Calculation
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import csv
import os
import time
import threading

# ---------- Load & Save Projects ----------
def load_projects():
    if os.path.exists("projects.json"):
        with open("projects.json", "r") as f:
            data = json.load(f)
        return data.get("projects", [])
    return []

def save_project(project_name):
    projects = load_projects()
    if project_name and project_name not in projects:
        projects.append(project_name)
        with open("projects.json", "w") as f:
            json.dump({"projects": projects}, f, indent=4)

# ---------- Timer App ----------
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Freelancer Timer")

        # State variables
        self.running = False
        self.paused = False
        self.start_time = None
        self.elapsed_seconds = 0

        # --- UI ---
        ttk.Label(root, text="Project:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.project_var = tk.StringVar()
        self.project_box = ttk.Combobox(root, textvariable=self.project_var, values=load_projects(), width=40)
        self.project_box.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Description:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(root, textvariable=self.desc_var, width=43)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Hourly Rate (£):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.rate_var = tk.StringVar(value="40")  # default rate
        self.rate_entry = ttk.Entry(root, textvariable=self.rate_var, width=10)
        self.rate_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        self.time_label = ttk.Label(root, text="00:00:00", font=("Consolas", 24))
        self.time_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Buttons
        self.start_button = ttk.Button(root, text="Start", command=self.start_timer)
        self.start_button.grid(row=4, column=0, padx=5, pady=10)

        self.pause_button = ttk.Button(root, text="Pause", command=self.toggle_pause, state="disabled")
        self.pause_button.grid(row=4, column=1, padx=5, pady=10, sticky="w")

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_button.grid(row=4, column=1, padx=5, pady=10, sticky="e")

        # CSV header
        if not os.path.exists("sessions.csv"):
            with open("sessions.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "session_id", "project_name", "description",
                    "start_time", "stop_time", "total_duration_min",
                    "rate_gbp", "earned_gbp"
                ])

    # --- Timer update thread ---
    def update_timer(self):
        while self.running:
            if not self.paused:
                elapsed = int(time.time() - self.start_time) + self.elapsed_seconds
                h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
                self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            time.sleep(1)

    # --- Start ---
    def start_timer(self):
        if self.running:
            return
        project = self.project_var.get().strip()
        if not project:
            messagebox.showwarning("Missing Info", "Please enter or select a project name.")
            return

        save_project(project)
        self.desc = self.desc_var.get().strip()
        self.start_time = time.time()
        self.start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.running = True
        self.paused = False
        self.pause_button.config(state="normal", text="Pause")
        self.stop_button.config(state="normal")
        self.start_button.config(state="disabled")

        threading.Thread(target=self.update_timer, daemon=True).start()

    # --- Pause / Continue ---
    def toggle_pause(self):
        if not self.running:
            return

        if not self.paused:
            self.paused = True
            self.elapsed_seconds += int(time.time() - self.start_time)
            self.pause_button.config(text="Continue")
        else:
            self.paused = False
            self.start_time = time.time()
            self.pause_button.config(text="Pause")

    # --- Stop ---
    def stop_timer(self):
        if not self.running:
            return
        if not self.paused:
            total_seconds = int(time.time() - self.start_time) + self.elapsed_seconds
        else:
            total_seconds = self.elapsed_seconds

        self.running = False
        self.paused = False
        self.pause_button.config(state="disabled", text="Pause")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.elapsed_seconds = 0

        stop_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_minutes = round(total_seconds / 60, 2)

        # --- Calculate earnings ---
        try:
            rate = float(self.rate_var.get())
        except ValueError:
            rate = 0.0
        earned = round(rate * (total_minutes / 60), 2)

        # --- Write to CSV ---
        with open("sessions.csv", "a", newline="") as f:
            writer = csv.writer(f)
            session_id = sum(1 for _ in open("sessions.csv"))
            writer.writerow([
                session_id, self.project_var.get(), self.desc_var.get(),
                self.start_dt, stop_dt, total_minutes, rate, earned
            ])

        # --- Reset + Summary ---
        self.time_label.config(text="00:00:00")
        messagebox.showinfo(
            "Session Saved",
            f"Session recorded:\n"
            f"Duration: {total_minutes} min\n"
            f"Rate: £{rate}/hr\n"
            f"Earnings: £{earned}"
        )

# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()