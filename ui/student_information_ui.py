from flask import render_template
class StudentInformationUI:
    def __init__(self, db_controller):
        self.db_controller = db_controller
    
    def display_student(self, idnumber):
        student = self.db_controller.check_student(idnumber) 
        formatted_date = student['dob'].strftime('%A, %B %d, %Y')
        student['dob'] = formatted_date
        student['first_name'] = self.db_controller.get_name(idnumber)
        return render_template('student_profile.html', student=student)
    
    def display_student_leader(self, idnumber):
        student = self.db_controller.check_student(idnumber) 
        formatted_date = student['dob'].strftime('%A, %B %d, %Y')
        student['dob'] = formatted_date
        student['first_name'] = self.db_controller.get_name(idnumber)
        return render_template('student_profile_leader.html', student=student)