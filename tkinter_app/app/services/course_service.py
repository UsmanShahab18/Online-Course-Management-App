from app.models.course_model import Course

class CourseService:
    def __init__(self):
        self.courses = [
            Course(1, "Introduction to Python", "Learn the basics of Python programming.", 2, 3),
            Course(2, "Web Development Basics", "Understand HTML, CSS, and JavaScript.", 2, 4)
        ]

    def create_course(self, course_name, description, teacher_id, credits):
        new_id = len(self.courses) + 1
        new_course = Course(new_id, course_name, description, teacher_id, credits)
        self.courses.append(new_course)
        print(f"Course '{course_name}' created.")
        return new_course

    def get_course_by_id(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def get_all_courses(self):
        return self.courses

    def update_course(self, course_id, course_name=None, description=None, teacher_id=None, credits=None):
        course = self.get_course_by_id(course_id)
        if course:
            if course_name: course.course_name = course_name
            if description: course.description = description
            if teacher_id: course.teacher_id = teacher_id
            if credits: course.credits = credits
            print(f"Course ID {course_id} updated.")
            return True
        print(f"Course ID {course_id} not found for update.")
        return False

    def delete_course(self, course_id):
        course = self.get_course_by_id(course_id)
        if course:
            self.courses.remove(course)
            print(f"Course ID {course_id} deleted.")
            return True
        print(f"Course ID {course_id} not found for deletion.")
        return False