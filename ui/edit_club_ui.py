from flask import render_template
class EditClubUI:
    def __init__(self, db_controller):
        self.db_controller = db_controller
    
    def edit_club(self,club_info,message):
        return render_template('edit_club.html', club_info = club_info, message = message)