from models.notification import Notification

class NotificationController:
    def __init__(self, db_controller):
        self.db_controller = db_controller

    def create_notification(self, club_id, subject, message, timestamp, notification_type):
        new_notification = Notification(club_id, subject, message, notification_type, timestamp)
        return  self.db_controller.add_notification(new_notification)
    

        