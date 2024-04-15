from flask import render_template

class CreateNotificationUI:
    def __init__(self):
        pass
    
    def new_notification(self, club_id, notification_type,club_info):
        return render_template('create_notification.html', club_id=club_id, notification_type=notification_type,club_info=club_info)