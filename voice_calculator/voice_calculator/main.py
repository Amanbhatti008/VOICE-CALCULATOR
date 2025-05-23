import tkinter as tk
from tkinter import messagebox, scrolledtext
import re
import speech_recognition as sr
import pyttsx3

# ---------------- Voice Input ----------------
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except Exception as e:
        print("Error:", e)
        return None

# ---------------- Voice Output ----------------
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- Parsing and Calculation ----------------

def is_interest_query(text):
    return "interest" in text.lower() and "on" in text.lower() and "%" in text.lower()

def parse_interest_query(query):
    try:
        query = query.lower()
        principal_match = re.search(r'on\s+(\d+)', query)
        rate_match = re.search(r'at\s+(\d+)%', query)
        time_match = re.search(r'for\s+(\d+)', query)

        if not (principal_match and rate_match and time_match):
            return "Sorry, I couldn't understand the interest calculation.", ""

        principal = float(principal_match.group(1))
        rate = float(rate_match.group(1))
        time = float(time_match.group(1))

        si = (principal * rate * time) / 100

        answer = f"The simple interest is {si} rupees."
        steps = f"Steps:\n1. Principal (P) = {principal}\n2. Rate (R) = {rate}%\n3. Time (T) = {time} years\n4. Formula: SI = (P × R × T) / 100\n5. Calculation: ({principal} × {rate} × {time}) / 100 = {si}"
        return answer, steps
    except Exception:
        return "Sorry, I couldn't understand the interest calculation.", ""

def voice_to_expression(text):
    text = text.lower()
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("multiplied by", "*")
    text = text.replace("times", "*")
    text = text.replace("into", "*")
    text = text.replace("x", "*")
    text = text.replace("divided by", "/")
    # Removed replacing 'by' alone to avoid errors
    text = text.replace("mod", "%")
    # Remove everything except digits, operators, and parentheses
    text = re.sub(r"[^0-9+\-*/().%]", "", text)
    return text

def calculate_expression(expr):
    try:
        result = eval(expr)
        answer = f"The answer is {result}"
        steps = f"Evaluated the expression: {expr} = {result}"
        return answer, steps
    except Exception:
        return "Sorry, I couldn't calculate that expression.", ""

def get_response(text):
    if is_interest_query(text):
        return parse_interest_query(text)
    else:
        expr = voice_to_expression(text)
        return calculate_expression(expr)

def parse_command(text):
    return get_response(text)

# ---------------- GUI Application ----------------

LIGHT_BG = "#f0f0f0"
LIGHT_FG = "#222222"
DARK_BG = "#2e2e2e"
DARK_FG = "#ffffff"
BUTTON_BG = "#4a90e2"
BUTTON_FG = "#ffffff"

class VoiceCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Voice Calculator")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        
        self.dark_mode = False
        
        self.frame = tk.Frame(root, bg=LIGHT_BG)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.title_label = tk.Label(self.frame, text="Voice Calculator", font=("Arial", 24, "bold"), bg=LIGHT_BG, fg=LIGHT_FG)
        self.title_label.pack(pady=(0,20))
        
        # Text input to type question
        self.input_label = tk.Label(self.frame, text="Type your question here:", font=("Arial", 14), bg=LIGHT_BG, fg=LIGHT_FG)
        self.input_label.pack(pady=(5,5))
        
        self.question_entry = tk.Entry(self.frame, font=("Arial", 14), width=40)
        self.question_entry.pack(pady=(0,10))
        
        # Button to calculate typed question
        self.type_button = tk.Button(self.frame, text="Calculate Typed Question", font=("Arial", 14, "bold"), bg="#28a745", fg="white", command=self.process_typed_command)
        self.type_button.pack(pady=10, ipadx=10, ipady=8)
        
        # Or speak button
        self.speak_button = tk.Button(self.frame, text="🎙 Speak Now", font=("Arial", 16, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#357ABD", activeforeground="white", command=self.process_voice_command)
        self.speak_button.pack(pady=10, ipadx=10, ipady=10)
        
        self.result_label = tk.Label(self.frame, text="", font=("Arial", 18), bg=LIGHT_BG, fg="green", wraplength=560)
        self.result_label.pack(pady=(30,10))
        
        self.steps_box = scrolledtext.ScrolledText(self.frame, height=12, font=("Consolas", 12), bg="#eaeaea", fg="#333333", wrap="word")
        self.steps_box.pack(fill="both", expand=True)
        self.steps_box.config(state='disabled')
        
        self.toggle_btn = tk.Button(self.frame, text="Toggle Dark Mode", font=("Arial", 12), bg="#888", fg="white", command=self.toggle_dark_mode)
        self.toggle_btn.pack(pady=15, ipadx=5, ipady=5)
    
    def process_typed_command(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Input Needed", "Please type a question first.")
            return
        self.result_label.config(text="Processing...")
        self.root.update()
        answer, steps = parse_command(question)
        self.result_label.config(text=answer)
        self.steps_box.config(state='normal')
        self.steps_box.delete('1.0', tk.END)
        self.steps_box.insert(tk.END, steps)
        self.steps_box.config(state='disabled')
        speak(answer)
    
    def process_voice_command(self):
        self.result_label.config(text="Listening... 🎧")
        self.root.update()
        cmd = listen_command()
        if cmd:
            answer, steps = parse_command(cmd)
            self.result_label.config(text=answer)
            self.steps_box.config(state='normal')
            self.steps_box.delete('1.0', tk.END)
            self.steps_box.insert(tk.END, steps)
            self.steps_box.config(state='disabled')
            speak(answer)
        else:
            self.result_label.config(text="Sorry, I did not get that.")
            self.steps_box.config(state='normal')
            self.steps_box.delete('1.0', tk.END)
            self.steps_box.config(state='disabled')
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            bg_color = DARK_BG
            fg_color = DARK_FG
            text_bg = "#444444"
            text_fg = "#dddddd"
            btn_bg = "#1a73e8"
        else:
            bg_color = LIGHT_BG
            fg_color = LIGHT_FG
            text_bg = "#eaeaea"
            text_fg = "#333333"
            btn_bg = BUTTON_BG
        
        self.frame.config(bg=bg_color)
        self.title_label.config(bg=bg_color, fg=fg_color)
        self.input_label.config(bg=bg_color, fg=fg_color)
        self.result_label.config(bg=bg_color, fg="lightgreen" if self.dark_mode else "green")
        self.steps_box.config(bg=text_bg, fg=text_fg)
        self.question_entry.config(bg=text_bg, fg=text_fg, insertbackground=fg_color)
        self.speak_button.config(bg=btn_bg, fg=BUTTON_FG, activebackground="#357ABD", activeforeground="white")
        self.type_button.config(bg="#218838" if self.dark_mode else "#28a745", fg="white", activebackground="#1e7e34", activeforeground="white")
        self.toggle_btn.config(bg="#555555" if self.dark_mode else "#888888")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceCalculatorApp(root)
    root.mainloop()
