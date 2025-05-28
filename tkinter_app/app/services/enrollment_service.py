from app.models.enrollment_model import Enrollment
from datetime import datetime

class EnrollmentService:
    def __init__(self):
        self.enrollments = []

    def enroll_student_in_course(self, student_id, course_id):
        # Check if already enrolled
        for enrollment in self.enrollments:
            if enrollment.student_id == student_id and enrollment.course_id == course_id:
                print(f"Student {student_id} already enrolled in course {course_id}.")
                return None
        
        new_id = len(self.enrollments) + 1
        enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_enrollment = Enrollment(new_id, student_id, course_id, enrollment_date)
        self.enrollments.append(new_enrollment)
        print(f"Student {student_id} enrolled in course {course_id}.")
        return new_enrollment

    def get_student_enrollments(self, student_id):
        return [e for e in self.enrollments if e.student_id == student_id]

    def get_course_enrollments(self, course_id):
        return [e for e in self.enrollments if e.course_id == course_id]

    def unenroll_student_from_course(self, student_id, course_id):
        enrollment_to_remove = None
        for enrollment in self.enrollments:
            if enrollment.student_id == student_id and enrollment.course_id == course_id:
                enrollment_to_remove = enrollment
                break
        if enrollment_to_remove:
            self.enrollments.remove(enrollment_to_remove)
            print(f"Student {student_id} unenrolled from course {course_id}.")
            return True
        print(f"Enrollment not found for student {student_id} in course {course_id}.")
        return False