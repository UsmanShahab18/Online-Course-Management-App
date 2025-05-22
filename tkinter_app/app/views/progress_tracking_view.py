import tkinter as tk
from tkinter import ttk
from app.utils.style import HEADING_FONT, MAIN_FONT

class ProgressTrackingView(tk.Toplevel):
    def __init__(self, master, current_user, on_close_callback=None): # Add services as needed
        super().__init__(master)
        self.current_user = current_user
        self.on_close_callback = on_close_callback

        self.title("Progress Tracking")
        self.geometry("700x500")
        self.configure(bg="#ecf0f1")

        if self.on_close_callback:
            self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        self.create_widgets()
        self.load_progress_data()

    def on_close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="My Progress" if self.current_user.role == "Student" else "Student Progress Overview", 
                  font=HEADING_FONT).pack(pady=10)

        self.progress_tree = ttk.Treeview(main_frame, columns=("Course", "Completion", "Grade"), show="headings")
        self.progress_tree.heading("Course", text="Course Name")
        self.progress_tree.heading("Completion", text="Completion %")
        self.progress_tree.heading("Grade", text="Overall Grade")
        self.progress_tree.column("Course", width=300)
        self.progress_tree.column("Completion", width=150, anchor=tk.CENTER)
        self.progress_tree.column("Grade", width=100, anchor=tk.CENTER)
        self.progress_tree.pack(expand=True, fill="both", pady=10)
        
        if self.current_user.role == "Teacher" or self.current_user.role == "Admin":
            controls_frame = ttk.Frame(main_frame)
            controls_frame.pack(fill=tk.X, pady=5)
            ttk.Label(controls_frame, text="Select Student (for Teacher/Admin):", font=MAIN_FONT).pack(side=tk.LEFT, padx=5)
            # Add a combobox for student selection by teacher/admin
            self.student_selector = ttk.Combobox(controls_frame, font=MAIN_FONT, state="readonly", width=30)
            self.student_selector.pack(side=tk.LEFT, padx=5)
            # Populate student_selector with students
            # self.student_selector.bind("<<ComboboxSelected>>", self.load_progress_data)

    def load_progress_data(self, event=None):
        for item in self.progress_tree.get_children():
            self.progress_tree.delete(item)

        # This is placeholder data. In a real app, fetch from services.
        if self.current_user.role == "Student":
            # Fetch progress for self.current_user.user_id
            sample_data = [
                ("Introduction to Python", "75%", "B+"),
                ("Web Development Basics", "50%", "In Progress"),
            ]
        elif self.current_user.role == "Teacher" or self.current_user.role == "Admin":
            # Fetch progress for selected student or an overview
            # selected_student_id = self.student_selector.get() # if implemented
            sample_data = [
                ("Course A (Student X)", "90%", "A"),
                ("Course B (Student Y)", "60%", "C"),
            ]
        else:
            sample_data = []
            
        for data_row in sample_data:
            self.progress_tree.insert("", tk.END, values=data_row)
        
        print(f"Loading progress data for {self.current_user.username} ({self.current_user.role})")