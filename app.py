from flask import Flask, render_template, request, redirect, url_for, session
from controllers.club_controller import ClubController
from controllers.db_controller import DbController
from controllers.StudentController import StudentController
from controllers.notification_controller import NotificationController
from datetime import datetime
from ui.register_club_ui import RegisterClubUI
from ui.join_club_ui import JoinClubUI
from ui.club_information_ui import ClubInformationUI
from ui.student_information_ui import StudentInformationUI
from ui.create_notification_ui import CreateNotificationUI
from ui.create_account_ui import CreateAccountUI
from ui.search_club_ui import SearchClubUI
from ui.edit_club_ui import EditClubUI
from controllers.membership_controller import MembershipController
import secrets
import string
app = Flask(__name__)

# Initialize controllers
db_controller = DbController()
club_controller = ClubController(db_controller)
student_controller = StudentController(db_controller)
notification_controller = NotificationController(db_controller)
register_ui = RegisterClubUI()
create_notification_ui = CreateNotificationUI()
create_account_ui = CreateAccountUI()
student_info_ui = StudentInformationUI(db_controller)
join_ui = JoinClubUI()
club_info_ui = ClubInformationUI(db_controller)
membership_controller = MembershipController(db_controller)
search_club_ui = SearchClubUI(db_controller)
edit_club_ui = EditClubUI(db_controller)

def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

app.secret_key = generate_secret_key()

# Render the HTML form

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        idnumber = request.form['idnumber']
        password = request.form['password']
        student = student_controller.check_credentials(idnumber)
        fullname = student_controller.get_fullname(idnumber)
        exists = student_controller.check_login(idnumber, password)
        
        if exists == True:
            session['idnumber'] = idnumber
            session['name'] = fullname
           
            if student['account_type'] == 'Club Leader':
                return redirect(url_for('leader_main'))
            else:
                return redirect(url_for('student_main'))
        else: 
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session upon logout
    session.pop('idnumber', None)
    return redirect(url_for('login'))

@app.route('/student-main')
def student_main():
    if 'idnumber' in session:
        fullname = session['name'] 
        return render_template('student_main.html', fullname=fullname) 
    else: 
        return redirect(url_for('login'))
    
@app.route('/leader-main')
def leader_main():
    if 'idnumber' in session: 
        fullname = session['name']  
        islead = student_controller.check_leadership(session['idnumber'])
        if islead:
            return render_template('leader_main.html', fullname=fullname) 
        else:
           return register_ui.create_new_club('Please Register Your Club', session['idnumber'])
    else:
        return redirect(url_for('login'))
    

@app.route('/register', methods=['GET'])
def register_form():
    return create_account_ui.create_student_account()


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    idnumber = request.form.get('idnumber')
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    account_type = 'Student'
    gender = request.form.get('gender')
    dob = request.form['dob']
    phone = request.form['phone']
    email = request.form['email']
    if password != confirm_password:
        return render_template('create_account.html', error_message="Passwords do not match")
    registration_message = student_controller.register_student(first_name, last_name, idnumber, password, account_type, gender, dob, phone, email)
    
    if registration_message == "Student Account Created Successfully":
       return render_template('login.html', error_message=registration_message)
    else:
        return render_template('login.html', error_message=registration_message)

@app.route('/register-leader', methods=['GET', 'POST'])
def register_leader():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        idnumber = request.form.get('idnumber')
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        account_type = 'Club Leader'
        gender = request.form.get('gender')
        dob = request.form['dob']
        phone = request.form['phone']
        email = request.form['email']
        if password != confirm_password:
            return render_template('create_account_leader.html', error_message="Passwords do not match")
        registration_message = student_controller.register_student(first_name, last_name, idnumber, password, account_type, gender, dob, phone, email)
        
        if registration_message == "Leader Account Created Successfully":
            return render_template('login.html', error_message=registration_message)
        else:
            return render_template('login.html', error_message=registration_message)
    else:
        return create_account_ui.create_club_leader_account()


@app.route('/select-account-type')
def select_account_type():
    return create_account_ui.select_account_type()


@app.route('/get_student_info')
def get_info():
    return student_info_ui.display_student(session['idnumber'])

@app.route('/get_student_info_leader')
def get_info_leader():
    return student_info_ui.display_student_leader(session['idnumber'])

@app.route('/search_clubs')
def search_clubs():
    return search_club_ui.display_clubs()

@app.route('/search_clubs_leader')
def search_clubs_leader():
    return search_club_ui.display_clubs_leader(session['idnumber'])

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        return search_club_ui.search_clubs(query)
    else:
        return search_club_ui.display_clubs()
    
@app.route('/search_leader', methods=['GET'])
def search_leader():
    query = request.args.get('query')
    if query:
        return search_club_ui.search_clubs_leader(query,session['idnumber'])
    else:
        return search_club_ui.display_clubs_leader(session['idnumber'])
    
@app.route('/view_club/<int:club_id>')
def view_club(club_id):
    return club_info_ui.display_club_info_student(club_id,'')

@app.route('/view_club_leader/<int:club_id>')
def view_club_leader(club_id):
    return club_info_ui.display_club_info_student_leader(club_id,'')
    
# Handle form submission and create the club

    
@app.route('/submit_student', methods=['POST'])
def submit_student():
    # Get data from the form
    id_number = request.form['idnumber']
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone']
    club = request.form['club_id']

    message = membership_controller.create_member(club, id_number,name,email,phone_number)

    if message == "Successfully joined the club":
       
        return render_template('student_main.html', message = message, fullname = session['name'] )
    elif message == "Already a member of this club":
        return club_info_ui.display_club_info_student(club,message)
    else: 
        return render_template('join.html',message = message)

@app.route('/submit_student_leader', methods=['POST'])
def submit_student_leader():
    # Get data from the form
    id_number = request.form['idnumber']
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone']
    club = request.form['club_id']

    message = membership_controller.create_member(club, id_number,name,email,phone_number)

    if message == "Successfully joined the club":
        
        return render_template('leader_main.html', message = message, fullname = session['name'] )
    elif message == "Already a member of this club":
        return club_info_ui.display_club_info_student_leader(club,message)
    else: 
        return render_template('join_leader.html',message = message)

@app.route('/join_club/<int:club_id>')
def join(club_id):
    return join_ui.join_club(club_id)

@app.route('/join_club_leader/<int:club_id>')
def join_leader(club_id):
    return join_ui.join_club_leader(club_id)


@app.route('/create_club', methods=['POST'])
def create_club():
    club_name = request.form['clubName']
    description = request.form['description']
    club_leader = request.form['clubLeader']
    if club_controller.create_club(club_name, description, club_leader):
        return redirect(url_for('club_info_leader', club_name=club_name))
    else:
        return 'Club Already Exists'
    

@app.route('/club_info_leader/<club_name>')
def club_info_leader(club_name):
    return club_info_ui.display_club_leader(club_name,'')


@app.route('/club_info_member/<club_name>')
def club_info_member(club_name):
    return club_info_ui.display_club_member(club_name)

@app.route('/club_info_member_leader/<club_name>')
def club_info_member_leader(club_name):
    return club_info_ui.display_club_member_leader(club_name)


@app.route('/clubs_im_in')
def clubs_im_in():
    idnumber = session['idnumber']
    clubs = db_controller.get_clubs_by_membership(idnumber)

    # Render the template with the list of clubs
    return render_template('clubs_im_in.html', clubs=clubs)

@app.route('/my_club')
def my_club():
    idnumber = session['idnumber']
    club_id = db_controller.get_club_id_by_leader(idnumber)
    club_name = db_controller.retrieve_club_by_id(club_id)['clubName']
    return club_info_ui.display_club_leader(club_name,'')

@app.route('/clubs_im_in_leader')
def clubs_im_in_leader():
    idnumber = session['idnumber']
    clubs = db_controller.get_clubs_by_membership(idnumber)
    return render_template('clubs_im_in_leader.html', clubs=clubs)

@app.route('/edit-club/<club_name>')
def edit_club(club_name):

    club_info = db_controller.retrieve_club(club_name)
    return edit_club_ui.edit_club(club_info,'')

@app.route('/submit_edit', methods=['POST'])
def edit_club_submit():
    edited_club_name = request.form['clubName']
    edited_description = request.form['description']
    original_club_name = request.form['originalClubName'] 
    
    club_id = db_controller.get_club_id(original_club_name)
    message = club_controller.update_club_info(original_club_name, edited_club_name, edited_description,club_id)
    
    if message == "Club Information successfully edited":
        
        return club_info_ui.display_club_leader(edited_club_name,message)
    elif message == "Club Information could not be edited":
        return club_info_ui.display_club_leader(original_club_name,message)
    else: 
        club_info = db_controller.retrieve_club(original_club_name)
        return edit_club_ui.edit_club(club_info,message)
         
        

@app.route('/create-notification/<int:club_id>/<notification_type>')
def create_notification(club_id, notification_type):
    club_info = db_controller.retrieve_club_by_id(club_id)
    return create_notification_ui.new_notification(club_id, notification_type,club_info)
    

@app.route('/submit-notification', methods=['POST'])
def submit_notification():
        club_id = request.form['club_id']
        subject = request.form['subject']
        message = request.form['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        notification_type = request.form['type']
        
        result = notification_controller.create_notification(club_id, subject,"<br>"+ message, timestamp, notification_type)
        
        if result == 'Successful':
            idnumber = session['idnumber']
            club_id = db_controller.get_club_id_by_leader(idnumber)
            club_name = db_controller.retrieve_club_by_id(club_id)['clubName']
            return club_info_ui.display_club_leader(club_name,'Notification has been successfully published')
        else:
            return render_template('create_notification.html',club_id = club_id, notification_type = notification_type, message = "Notification was not added")


if __name__ == '__main__':
    app.run(debug=True)

