from flask import render_template

class RegisterClubUI:
    def __init__(self):
        pass

    def create_new_club(self, message, leader_id):
        return render_template('register_club.html',message = message, leader_id = leader_id)