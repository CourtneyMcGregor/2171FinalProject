from flask import render_template

class JoinClubUI:
    def __init__(self):
        pass
    
    def join_club(self,club_id):
        return render_template('join.html',club_id=club_id)
    
    def join_club_leader(self,club_id):
        return render_template('join_leader.html',club_id=club_id)