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
        self.pause_start_time = None
        self.total_pause_seconds = 0

        # --- UI ---
        ttk.Label(root, text="Project:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.project_var = tk.StringVar()
        self.project_box = ttk.Combobox(root, textvariable=self.project_var,
                                        values=load_projects(), width=40)
        self.project_box.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Description:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.desc_var, width=43).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Hourly Rate (£):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.rate_var = tk.StringVar(value="40")
        ttk.Entry(root, textvariable=self.rate_var, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(root, text="Minimum Billable (min):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.min_var = tk.StringVar(value="")
        ttk.Entry(root, textvariable=self.min_var, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        self.time_label = ttk.Label(root, text="00:00:00", font=("Consolas", 24))
        self.time_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.pause_label = ttk.Label(root, text="Paused: 0.0 min", font=("Segoe UI", 10))
        self.pause_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        # Buttons
        self.start_button = ttk.Button(root, text="Start", command=self.start_timer)
        self.start_button.grid(row=6, column=0, padx=5, pady=10)

        self.pause_button = ttk.Button(root, text="Pause", command=self.toggle_pause, state="disabled")
        self.pause_button.grid(row=6, column=1, padx=5, pady=10, sticky="w")

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_button.grid(row=6, column=1, padx=5, pady=10, sticky="e")

        # CSV header
        if not os.path.exists("sessions.csv"):
            with open("sessions.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "session_id", "project_name", "description",
                    "start_time", "stop_time",
                    "total_duration_min", "paused_duration_min",
                    "billable_min", "rate_gbp", "earned_gbp"
                ])

    # --- Timer update thread ---
    def update_timer(self):
        while self.running:
            if not self.paused:
                elapsed = int(time.time() - self.start_time) + self.elapsed_seconds
                h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
                self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            else:
                # Show pause duration live
                current_pause = self.total_pause_seconds
                if self.pause_start_time:
                    current_pause += int(time.time() - self.pause_start_time)
                pause_min = current_pause / 60
                self.pause_label.config(text=f"Paused: {pause_min:.1f} min")

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
        self.start_time = time.time()
        self.start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.running = True
        self.paused = False
        self.elapsed_seconds = 0
        self.total_pause_seconds = 0
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
            self.pause_start_time = time.time()
            self.pause_button.config(text="Continue")
        else:
            self.paused = False
            pause_duration = int(time.time() - self.pause_start_time)
            self.total_pause_seconds += pause_duration
            self.start_time = time.time()
            self.pause_start_time = None
            self.pause_button.config(text="Pause")

    # --- Stop ---
    def stop_timer(self):
        if not self.running:
            return

        # If stopped while paused, include that final pause
        if self.paused and self.pause_start_time:
            pause_duration = int(time.time() - self.pause_start_time)
            self.total_pause_seconds += pause_duration
            total_seconds = self.elapsed_seconds
        else:
            total_seconds = int(time.time() - self.start_time) + self.elapsed_seconds

        # Reset UI and states
        self.running = False
        self.paused = False
        self.pause_button.config(state="disabled", text="Pause")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

        stop_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_minutes = round(total_seconds / 60, 2)
        pause_minutes = round(self.total_pause_seconds / 60, 2)
        self.elapsed_seconds = 0
        self.total_pause_seconds = 0

        # --- Calculate billable ---
        try:
            rate = float(self.rate_var.get())
        except ValueError:
            rate = 0.0

        try:
            minimum_minutes = float(self.min_var.get()) if self.min_var.get().strip() else 0.0
        except ValueError:
            minimum_minutes = 0.0

        billable_minutes = max(total_minutes, minimum_minutes)
        earned = round(rate * (billable_minutes / 60), 2)

        # --- Write to CSV ---
        with open("sessions.csv", "a", newline="") as f:
            writer = csv.writer(f)
            session_id = sum(1 for _ in open("sessions.csv"))
            writer.writerow([
                session_id, self.project_var.get(), self.desc_var.get(),
                self.start_dt, stop_dt,
                total_minutes, pause_minutes, billable_minutes,
                rate, earned
            ])

        self.time_label.config(text="00:00:00")
        self.pause_label.config(text="Paused: 0.0 min")

        messagebox.showinfo(
            "Session Saved",
            f"Session recorded:\n"
            f"Duration: {total_minutes} min\n"
            f"Paused: {pause_minutes} min\n"
            f"Billable: {billable_minutes} min\n"
            f"Rate: £{rate}/hr\n"
            f"Earnings: £{earned}"
        )


# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()