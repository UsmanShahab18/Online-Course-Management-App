class Course:
    def __init__(self, course_id, course_name, description, teacher_id, credits=0):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.teacher_id = teacher_id
        self.credits = credits

    def __str__(self):
        return f"Course(ID: {self.course_id}, Name: {self.course_name})"