
from validators import Validator
from models.student import Student

class StudentController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.validator = Validator(db_controller)


    def check_credentials(self, idnumber):
        return self.db_controller.check_student(idnumber)
           

    def get_fullname(self, idnumber):
        return self.db_controller.get_name(idnumber)
        
    def check_login(self, idnumber, password):
        return self.db_controller.check_login_info(idnumber,password)



    def check_leadership(self,idnumber):
        return self.db_controller.check_lead(idnumber)

    def register_student(self, first_name, last_name, idnumber, password, account_type, gender, dob, phone, email):
        if self.validator.validate_id(idnumber):
            new_student = Student(first_name, last_name, idnumber, password, account_type, gender, dob, phone, email)
            return self.db_controller.add_student(new_student)
        else: 
            return "Student account already exists"