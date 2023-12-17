import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from ai_get import ai_savol

class TestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Knowledge Test App")
        self.master.geometry("600x600")
        self.current_question = 0
        self.score = 0
        self.questions = []

        self.create_welcome_frame()

    def create_welcome_frame(self):
        self.welcome_frame = tk.Frame(self.master)
        self.welcome_frame.pack(padx=20, pady=20)

        # Welcome message with question number
        self.welcome_label = tk.Label(self.welcome_frame, text="")
        self.welcome_label.pack(pady=15)

        # Button to upload CSV file
        self.load_button = tk.Button(self.welcome_frame, text="Upload CSV File", command=self.load_test)
        self.load_button.pack()

    def create_question_frame(self):
        self.question_frame = tk.Frame(self.master)
        self.question_frame.pack(padx=20, pady=20)

        # Question label with question number
        self.question_label = tk.Label(self.question_frame, text="", font=("Helvetica", 14), wraplength=400)
        self.question_label.pack(pady=15)

        # Radiobuttons for answers
        self.radio_var = tk.IntVar()
        self.radio_buttons = []

        for i in range(4):
            radio_button = tk.Radiobutton(self.question_frame, text="", variable=self.radio_var, value=i, font=("Helvetica", 14), wraplength=400)
            radio_button.pack(pady=10)
            self.radio_buttons.append(radio_button)

        # Buttons for navigation
        tk.Button(self.question_frame, text="Previous", command=self.prev_question, height=1, font=("System", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.question_frame, text="Next", command=self.next_question, height=1, font=("System", 12)).pack(side=tk.RIGHT, padx=10)

    def load_test(self):
        # Display file dialog to select CSV file
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            # Read questions from CSV file
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                self.questions = list(reader)

            if self.questions:
                self.current_question = 0
                self.score = 0
                self.create_question_frame()
                self.display_question()
                self.hide_upload_button()
            else:
                messagebox.showwarning("Error", "No questions found in the CSV file.")

    def hide_upload_button(self):
        self.load_button.pack_forget()

    def display_question(self):
        question_data = self.questions[self.current_question]

        # Update welcome label with question number
        self.welcome_label.config(text=f"Question {self.current_question + 1}/{len(self.questions)}")

        # Display question text
        self.question_label.config(text=question_data["Вопрос"])

        # Display answers
        for i, radio_button in enumerate(self.radio_buttons):
            radio_button.config(text=question_data[f"Ответ{i+1}"])

    def check_answer(self):
        selected_answer_index = self.radio_var.get()
        correct_answer_index = int(self.questions[self.current_question]["Правильный"])

        if selected_answer_index == correct_answer_index:
            self.score += 1
            return True
        else:
            return False

    def next_question(self):
        question_data = self.questions[self.current_question]
        q = question_data["Вопрос"]
        
        if self.check_answer():
            self.current_question += 1

            if self.current_question < len(self.questions):
                self.display_question()
            else:
                self.show_result()
        else:
            # messagebox.showinfo("Incorrect Answer", "Sorry, that answer is not correct. Please try again.")
            otvet=ai_savol(q)
            messagebox.showinfo(f"{q}",otvet)


    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()

    def show_result(self):
        messagebox.showinfo("Result", f"Test completed.")
        self.welcome_frame.destroy()
        self.question_frame.destroy()
        self.create_welcome_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
