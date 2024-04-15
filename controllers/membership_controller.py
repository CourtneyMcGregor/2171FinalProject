
from validators import Validator
from controllers.notification_controller import NotificationController
from datetime import datetime

class MembershipController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.validator = Validator(db_controller)
        


    def create_member(self, club_id, id_number,name,email,phone_number):
        notification_controller = NotificationController(self.db_controller)
        if self.validator.validate_id(id_number):
            return "Incorrect ID Number"
        else:
            if self.validator.validate_membership(club_id,id_number):
                return "Already a member of this club"
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                notification_controller.create_notification(club_id, "New Member", "<br> A new member has joined the club, please make "+name+" feel welcomed.", timestamp, "New Member")
                return self.db_controller.add_member(club_id, id_number,name,email,phone_number)
                 