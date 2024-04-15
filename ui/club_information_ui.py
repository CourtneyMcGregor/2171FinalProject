from flask import render_template
from datetime import datetime


class ClubInformationUI:
    def __init__(self, db_controller):
        self.db_controller = db_controller


    def display_club_info_student(self, club_id,message):
        club_list = self.db_controller.retrieve_club_by_id(club_id)
        if club_list:
            return render_template('club_info_student.html', club_list=club_list, message = message)
        else:
            return render_template('club_not_found.html')
        
    def display_club_info_student_leader(self, club_id,message):
        club_list = self.db_controller.retrieve_club_by_id(club_id)
        if club_list:
            return render_template('club_info_student_leader.html', club_list=club_list, message = message)
        else:
            return render_template('club_not_found.html')
        
    def display_club_leader(self, club_name,message):
        club_id = self.db_controller.get_club_id(club_name)
        club_info = self.db_controller.retrieve_club_by_id(club_id)
        club_members = self.db_controller.get_club_members(club_id)
        notifications = self.db_controller.get_notifications(club_id)
        for notification in notifications:
                    formatted_date = notification['date'].strftime('%A, %B %d, %Y')
                    notification['date'] = formatted_date
                    time_str = str(notification['time'])
                    time_obj = datetime.strptime(time_str, '%H:%M:%S')
                    notification['time'] = time_obj.strftime("%I:%M %p")
        return render_template('club_info_leader.html',club_info = club_info, club_members = club_members,message = message,notifications = notifications)


    def display_club_member(self, club_name):
        club_id = self.db_controller.get_club_id(club_name)
        club_info = self.db_controller.retrieve_club_by_id(club_id)
        notifications = self.db_controller.get_notifications(club_id)
        for notification in notifications:
                    formatted_date = notification['date'].strftime('%A, %B %d, %Y')
                    notification['date'] = formatted_date
                    time_str = str(notification['time'])
                    time_obj = datetime.strptime(time_str, '%H:%M:%S')
                    notification['time'] = time_obj.strftime("%I:%M %p")
        return render_template('club_info_member.html',club_info = club_info, notifications = notifications)
    
    def display_club_member_leader(self, club_name):
        club_id = self.db_controller.get_club_id(club_name)
        club_info = self.db_controller.retrieve_club_by_id(club_id)
        notifications = self.db_controller.get_notifications(club_id)
        for notification in notifications:
                    formatted_date = notification['date'].strftime('%A, %B %d, %Y')
                    notification['date'] = formatted_date
                    time_str = str(notification['time'])
                    time_obj = datetime.strptime(time_str, '%H:%M:%S')
                    notification['time'] = time_obj.strftime("%I:%M %p")
        return render_template('club_info_member_leader.html',club_info = club_info, notifications = notifications)