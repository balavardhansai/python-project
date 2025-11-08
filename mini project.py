import tkinter as tk
import time
import random

# typing text samples
text_pool = [
    "Python is a powerful and easy to learn programming language.",
    "Artificial Intelligence helps computers make decisions like humans.",
    "Machine learning allows computers to improve from experience.",
    "Data science combines math, statistics, and programming to analyze data.",
    "Tkinter is a standard GUI library for Python applications.",
    "Coding every day helps improve logical thinking and problem solving skills.",
    "Automation saves time and reduces human errors in repetitive tasks.",
    "Simple projects help beginners understand programming concepts clearly."
]

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Analyzer")
        self.root.geometry("850x550")
        self.root.config(bg="#111")

        self.difficulty = tk.StringVar(value="Medium")
        self.timer_option = tk.StringVar(value="1 min")
        self.time_left = 0
        self.start_time = None
        self.running = False

        # heading
        tk.Label(root, text="Typing Speed Analyzer", font=("Arial", 20, "bold"),
                 bg="#111", fg="#0ff").pack(pady=10)

        # options
        opt_frame = tk.Frame(root, bg="#111")
        opt_frame.pack()
        tk.Label(opt_frame, text="Difficulty:", bg="#111", fg="white").grid(row=0, column=0, padx=5)
        tk.OptionMenu(opt_frame, self.difficulty, "Easy", "Medium", "Hard").grid(row=0, column=1, padx=5)
        tk.Label(opt_frame, text="Timer:", bg="#111", fg="white").grid(row=0, column=2, padx=5)
        tk.OptionMenu(opt_frame, self.timer_option, "30 sec", "1 min", "5 min", "1 hr").grid(row=0, column=3, padx=5)

        # text to type
        self.text_display = tk.Label(root, text="", wraplength=750, fg="white",
                                     bg="#111", font=("Consolas", 13), justify="left")
        self.text_display.pack(pady=10)

        # typing area
        self.input_box = tk.Text(root, height=6, width=90, bg="#222", fg="white",
                                 font=("Consolas", 13), insertbackground="#0ff")
        self.input_box.pack()
        self.input_box.bind("<KeyPress>", self.start_typing)
        self.input_box.bind("<Return>", self.stop_test)

        # labels
        self.timer_label = tk.Label(root, text="", bg="#111", fg="#0ff", font=("Consolas", 13))
        self.timer_label.pack(pady=5)
        self.result_label = tk.Label(root, text="Select difficulty and click Start", bg="#111",
                                     fg="#0ff", font=("Consolas", 13))
        self.result_label.pack(pady=5)

        # button
        tk.Button(root, text="Start Test", bg="#0ff", fg="#111", font=("Consolas", 12, "bold"),
                  command=self.start_test).pack(pady=10)

    def start_test(self):
        self.input_box.config(state="normal")
        self.input_box.delete("1.0", "end")
        self.result_label.config(text="Get ready...")
        self.timer_label.config(text="")
        self.text_to_type = self.get_random_paragraph()
        self.text_display.config(text=self.text_to_type)
        self.running = False
        self.start_time = None
        self.time_left = self.get_time_limit()

        # small countdown
        self.root.after(1000, lambda: self.result_label.config(text="2..."))
        self.root.after(2000, lambda: self.result_label.config(text="1..."))
        self.root.after(3000, self.begin_typing)

    def get_random_paragraph(self):
        """Generate 3-4 random lines to type."""
        lines = random.sample(text_pool, 4)
        return " ".join(lines)

    def get_time_limit(self):
        choice = self.timer_option.get()
        return {"30 sec": 30, "1 min": 60, "5 min": 300, "1 hr": 3600}.get(choice, 60)

    def begin_typing(self):
        self.running = True
        self.result_label.config(text="Start typing...")
        self.countdown(self.time_left)

    def countdown(self, t):
        if not self.running:
            return
        if t >= 0:
            m, s = divmod(t, 60)
            self.timer_label.config(text=f"Time Left: {m:02d}:{s:02d}")
            self.root.after(1000, lambda: self.countdown(t - 1))
        else:
            self.time_up()

    def start_typing(self, e):
        if not self.start_time:
            self.start_time = time.time()
        if self.running:
            self.root.after(300, self.update_result)

    def update_result(self):
        if not self.running or not self.start_time:
            return
        typed = self.input_box.get("1.0", "end-1c")
        elapsed = max(time.time() - self.start_time, 1)
        words = len(typed.split())
        wpm = words / elapsed * 60
        correct = sum(a == b for a, b in zip(typed, self.text_to_type))
        accuracy = (correct / len(self.text_to_type)) * 100
        self.result_label.config(text=f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}%")

    def stop_test(self, e):
        if not self.running:
            return
        self.running = False
        self.update_result()
        self.input_box.config(state="disabled")
        self.timer_label.config(text="Test Ended.")
        self.result_label.config(text=self.result_label.cget("text") + " | Completed")
        return "break"

    def time_up(self):
        self.running = False
        self.update_result()
        self.input_box.config(state="disabled")
        self.timer_label.config(text="Time's Up!", fg="red")
        self.result_label.config(text=self.result_label.cget("text") + " | Time Over")

if __name__ == "__main__":
    root = tk.Tk()
    TypingSpeedTest(root)
    root.mainloop()
