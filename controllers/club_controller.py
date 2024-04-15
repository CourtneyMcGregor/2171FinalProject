from validators import Validator
from models.club import Club
from controllers.notification_controller import NotificationController
from datetime import datetime

class ClubController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.validator = Validator(db_controller)
    def create_club(self, club_name, description, club_leader):
        if self.validator.validate_club_name(club_name):
            notification_controller = NotificationController(self.db_controller)
            leader_name = self.db_controller.get_name(club_leader)
            new_club = Club(club_name, description, leader_name)
            self.db_controller.add_club(new_club)
            club_id = self.db_controller.get_club_id(club_name)
            self.db_controller.add_leader(club_id,club_leader)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            notification_controller.create_notification(club_id, "Club Creation","<br> <p>"+ club_name+" has been created </p> <strong>Description:</strong> "+description+ "<p> <strong>Leader:</strong> "+ leader_name +"</p>", timestamp, "New Club")
        
            
            return True
        else:
            return False
    def retrieve_club(self, club_name):
        return self.db_controller.retrieve_club(club_name)
    
    def get_club_by_lead(self,leader_id):
        return self.db_controller.get_club_id_by_leader(leader_id)  
    
    def update_club_info(self, original_club_name, edited_club_name, edited_description,club_id):
        
        if edited_club_name != original_club_name:
            result = self.validator.validate_club_name(edited_club_name)
        else: 
            result = not self.validator.validate_club_name(edited_club_name)
        if result:
            if self.db_controller.edit_club(original_club_name, edited_club_name, edited_description):
                notification_controller = NotificationController(self.db_controller)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                notification_controller.create_notification(club_id, "Club Info Edited", "<br><strong>New Club Name:</strong> "+edited_club_name+", "+ "<div> <strong>New Club descrption:</strong> "+edited_description + "</div>", timestamp, "Info Changes")
                return "Club Information successfully edited"
            else: 
                return "Club Information could not be edited"
        else: 
            return "The Club Name You Entered Already Exists"
       