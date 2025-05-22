import tkinter as tk
from tkinter import ttk, messagebox
from app.services.course_service import CourseService
from app.utils.style import HEADING_FONT, MAIN_FONT

class CourseCreationView(tk.Toplevel):
    def __init__(self, master, course_service, user_service, on_close_callback=None):
        super().__init__(master)
        self.course_service = course_service
        self.user_service = user_service
        self.on_close_callback = on_close_callback

        self.title("Course Management")
        self.geometry("600x500")
        self.configure(bg="#ecf0f1")

        if self.on_close_callback:
            self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        self.create_widgets()
        self.load_courses()

    def on_close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Manage Courses", font=HEADING_FONT).grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Label(main_frame, text="Course Name:", font=MAIN_FONT).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(main_frame, font=MAIN_FONT, width=30)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="Description:", font=MAIN_FONT).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.desc_entry = ttk.Entry(main_frame, font=MAIN_FONT, width=30)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="Teacher ID:", font=MAIN_FONT).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.teacher_id_entry = ttk.Entry(main_frame, font=MAIN_FONT, width=30)
        self.teacher_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(main_frame, text="Credits:", font=MAIN_FONT).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.credits_entry = ttk.Entry(main_frame, font=MAIN_FONT, width=30)
        self.credits_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        add_button = ttk.Button(main_frame, text="Add Course", command=self.add_course, style="Accent.TButton")
        add_button.grid(row=5, column=0, columnspan=2, pady=10, ipadx=5, ipady=2)
        
        self.course_list_frame = ttk.LabelFrame(main_frame, text="Existing Courses", padding="10")
        self.course_list_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ewns")
        
        self.course_tree = ttk.Treeview(self.course_list_frame, columns=("ID", "Name", "Teacher ID", "Credits"), show="headings")
        self.course_tree.heading("ID", text="ID")
        self.course_tree.heading("Name", text="Name")
        self.course_tree.heading("Teacher ID", text="Teacher ID")
        self.course_tree.heading("Credits", text="Credits")
        self.course_tree.column("ID", width=50, anchor=tk.CENTER)
        self.course_tree.column("Name", width=200)
        self.course_tree.column("Teacher ID", width=100, anchor=tk.CENTER)
        self.course_tree.column("Credits", width=70, anchor=tk.CENTER)
        self.course_tree.pack(expand=True, fill=tk.BOTH)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)


    def add_course(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        try:
            teacher_id = int(self.teacher_id_entry.get())
            credits = int(self.credits_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Teacher ID and Credits must be numbers.")
            return

        if name and desc and teacher_id and credits:
            self.course_service.create_course(name, desc, teacher_id, credits)
            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_entries()
            self.load_courses()
        else:
            messagebox.showerror("Error", "All fields are required.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.teacher_id_entry.delete(0, tk.END)
        self.credits_entry.delete(0, tk.END)

    def load_courses(self):
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        courses = self.course_service.get_all_courses()
        for course in courses:
            teacher_name = "N/A"
            teacher = self.user_service.get_user_by_id(course.teacher_id)
            if teacher:
                teacher_name = teacher.full_name
            self.course_tree.insert("", tk.END, values=(course.course_id, course.course_name, f"{teacher_name} (ID:{course.teacher_id})", course.credits))