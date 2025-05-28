import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import HEADING_FONT, MAIN_FONT

class StudentEnrollmentView(tk.Toplevel):
    def __init__(self, master, enrollment_service, course_service, user_service, current_user, on_close_callback=None):
        super().__init__(master)
        self.enrollment_service = enrollment_service
        self.course_service = course_service
        self.user_service = user_service
        self.current_user = current_user
        self.on_close_callback = on_close_callback

        self.title("Student Enrollment")
        self.geometry("700x500")
        self.configure(bg="#ecf0f1")

        if self.on_close_callback:
            self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        self.create_widgets()
        self.load_available_courses()
        self.load_my_enrollments()

    def on_close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(main_frame, text="Course Enrollment", font=HEADING_FONT).pack(pady=10)

        # Available Courses
        available_courses_frame = ttk.LabelFrame(main_frame, text="Available Courses", padding="10")
        available_courses_frame.pack(pady=10, fill="x", expand=False)

        self.course_combobox = ttk.Combobox(available_courses_frame, font=MAIN_FONT, state="readonly", width=40)
        self.course_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        
        enroll_button = ttk.Button(available_courses_frame, text="Enroll", command=self.enroll_in_course, style="Accent.TButton")
        enroll_button.pack(side=tk.LEFT, padx=5, pady=5)

        # My Enrollments
        my_enrollments_frame = ttk.LabelFrame(main_frame, text="My Enrolled Courses", padding="10")
        my_enrollments_frame.pack(pady=10, fill="both", expand=True)

        self.enrolled_tree = ttk.Treeview(my_enrollments_frame, columns=("CourseID", "CourseName", "EnrollmentDate"), show="headings")
        self.enrolled_tree.heading("CourseID", text="Course ID")
        self.enrolled_tree.heading("CourseName", text="Course Name")
        self.enrolled_tree.heading("EnrollmentDate", text="Enrolled On")
        self.enrolled_tree.column("CourseID", width=70, anchor=tk.CENTER)
        self.enrolled_tree.column("CourseName", width=250)
        self.enrolled_tree.column("EnrollmentDate", width=150, anchor=tk.CENTER)
        self.enrolled_tree.pack(expand=True, fill="both")

        unenroll_button = ttk.Button(my_enrollments_frame, text="Unenroll Selected", command=self.unenroll_from_course, style="Accent.TButton")
        unenroll_button.pack(pady=10)


    def load_available_courses(self):
        courses = self.course_service.get_all_courses()
        self.course_map = {f"{c.course_name} (ID: {c.course_id})": c.course_id for c in courses}
        self.course_combobox['values'] = list(self.course_map.keys())
        if self.course_combobox['values']:
            self.course_combobox.current(0)

    def load_my_enrollments(self):
        for item in self.enrolled_tree.get_children():
            self.enrolled_tree.delete(item)
        
        if self.current_user and self.current_user.role == "Student":
            enrollments = self.enrollment_service.get_student_enrollments(self.current_user.user_id)
            for enr in enrollments:
                course = self.course_service.get_course_by_id(enr.course_id)
                if course:
                    self.enrolled_tree.insert("", tk.END, values=(course.course_id, course.course_name, enr.enrollment_date))

    def enroll_in_course(self):
        selected_course_display = self.course_combobox.get()
        if not selected_course_display:
            messagebox.showerror("Error", "Please select a course.")
            return

        course_id = self.course_map.get(selected_course_display)
        if course_id and self.current_user and self.current_user.role == "Student":
            enrollment = self.enrollment_service.enroll_student_in_course(self.current_user.user_id, course_id)
            if enrollment:
                messagebox.showinfo("Success", f"Enrolled in {selected_course_display} successfully!")
                self.load_my_enrollments()
            else:
                messagebox.showwarning("Enrollment Info", f"Could not enroll in {selected_course_display}. You might already be enrolled.")
        elif not self.current_user or self.current_user.role != "Student":
            messagebox.showerror("Error", "Only students can enroll in courses.")
        else:
            messagebox.showerror("Error", "Selected course not found.")


    def unenroll_from_course(self):
        selected_item = self.enrolled_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course from 'My Enrolled Courses' to unenroll.")
            return

        item_values = self.enrolled_tree.item(selected_item, "values")
        course_id = item_values[0] # Assuming Course ID is the first column

        if self.current_user and self.current_user.role == "Student":
            success = self.enrollment_service.unenroll_student_from_course(self.current_user.user_id, int(course_id))
            if success:
                messagebox.showinfo("Success", f"Unenrolled from course ID {course_id} successfully.")
                self.load_my_enrollments()
            else:
                messagebox.showerror("Error", f"Failed to unenroll from course ID {course_id}.")
        else:
            messagebox.showerror("Error", "Action not permitted for current user.")