class Validator:
    def __init__(self, db_controller):
        self.db_controller = db_controller

    def validate_club_name(self, club_name):
        return not self.db_controller.retrieve_club(club_name)

    def validate_id(self, idnumber):
        return not self.db_controller.check_student(idnumber)

    def validate_membership(self, club_id, student_id):
        return self.db_controller.check_membership(club_id, student_id)