# clock.py (tai voit nimetä tämän vaikka kellokortti.py)

import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime


class TimeClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock-In software")

        # Tilamuuttujat
        self.start_time = None
        self.pause_time = None
        self.total_work_time = 0.0
        self.is_working = False
        self.is_paused = False

        # Näyttöelementit
        self.time_label = tk.Label(root, text="00:00:00", font=("Segoe UI", 60, "bold"))
        self.time_label.pack(pady=30)

        self.action_button = tk.Button(
            root,
            text="Clock In",
            command=self.toggle_action,
            bg="#4CAF50",      # vihreä
            fg="white",
            activebackground="#3F9642",
            font=("Segoe UI", 18),
            width=12,
            height=2,
            cursor="watch"
        )
        self.action_button.pack(pady=15)

        self.end_label = tk.Label(
            root,
            text="End day",
            font=("Segoe UI", 14, "underline"),
            fg="#1976D2",
            activeforeground="#3F9642",
            cursor="hand2"
        )
        self.end_label.pack(pady=10)
        self.end_label.bind("<Button-1>", self.end_day)

        # Käynnistetään kellon päivitys
        self.update_clock()

    def toggle_action(self):
        current_time = time.time()

        if not self.is_working:
            # Clock In
            self.start_time = current_time
            self.is_working = True
            self.is_paused = False
            self.action_button.config(text="Break", bg="#F44336")  # punainen

        elif not self.is_paused:
            # Break
            self.pause_time = current_time
            self.total_work_time += self.pause_time - self.start_time
            self.is_paused = True
            self.action_button.config(text="Continue", bg="#4CAF50")  # takaisin vihreäksi

        else:
            # Continue
            self.start_time = current_time
            self.is_paused = False
            self.action_button.config(text="Break", bg="#F44336")  # punainen

    def end_day(self, event):
        if not self.is_working:
            messagebox.showinfo("Huomio", "Et ole vielä kellottanut sisään.")
            return

        # Lopetetaan mahdollinen käynnissä oleva työaika
        if not self.is_paused:
            self.total_work_time += time.time() - self.start_time

        self.save_log()
        self.root.quit()

    def save_log(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total_seconds = int(self.total_work_time)

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        work_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        with open("work_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{today} - Työaika: {work_time_str}\n")

        messagebox.showinfo(
            "Päivä tallennettu",
            f"Päivä kirjattu!\nTyöaika tänään: {work_time_str}"
        )

    def update_clock(self):
        if self.is_working and not self.is_paused:
            elapsed = self.total_work_time + (time.time() - self.start_time)
            hours, remainder = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        self.root.after(1000, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("420x380")
    root.resizable(False, False)
    
    app = TimeClockApp(root)
    root.mainloop()