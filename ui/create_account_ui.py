from flask import render_template

class CreateAccountUI:
    def __init__(self):
        pass

    def select_account_type(self):
        return render_template('account_type.html')

    def create_student_account(self):
        return render_template('create_account.html')

    def create_club_leader_account(self):
        return render_template('create_account_leader.html')