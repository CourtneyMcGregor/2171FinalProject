from flask import render_template
class SearchClubUI:
    def __init__(self, db_controller):
        self.db_controller = db_controller
    
    def display_clubs(self):
        club_list = self.db_controller.retrieve_all_club()
        return render_template('search_clubs.html',club_list = club_list)
    
    def display_clubs_leader(self, leader_id):
        club_list = self.db_controller.retrieve_all_club()
        
        # Exclude clubs where the given leader_id is the leader
        filtered_club_list = [club for club in club_list if not self.db_controller.is_leader(club['id'], leader_id)]
        
        return render_template('search_clubs_leader.html', club_list=filtered_club_list)
    
    def search_clubs(self, query):
        club_list = self.db_controller.search_clubs(query)
        if len(club_list)==0:
            message = 'Club Not Found'
        else: 
            message  = ''
        return render_template('search_clubs.html', club_list=club_list,message=message)
    
    def search_clubs_leader(self, query,leader_id):
        club_list = self.db_controller.search_clubs(query)
        filtered_club_list = [club for club in club_list if not self.db_controller.is_leader(club['id'], leader_id)]
        if len(filtered_club_list)==0:
            message = 'Club Not Found'
        else: 
            message  = ''
        return render_template('search_clubs_leader.html', club_list=filtered_club_list,message=message)
    