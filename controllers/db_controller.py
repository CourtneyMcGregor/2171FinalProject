import mysql.connector 
class DbController:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="kraem",
            password="Custodian",
            database="Project2171"
        )
        self.cursor = self.connection.cursor()

    def add_club(self, club):
        try:
            query = "INSERT INTO clubs (clubName, description, clubLeader) VALUES (%s, %s, %s)"
            values = (club.club_name.strip(), club.description.strip(), club.club_leader.strip())
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            # Log or handle the error
            print(f"Error adding club: {err}")

    def get_club_id(self, club_name):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id FROM clubs WHERE clubName = %s"
        try:
            cursor.execute(query, (club_name,))
            result = cursor.fetchone()
            if result:
                return result['id']  # Assuming 'id' is the name of the column containing the club ID
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error retrieving club ID: {err}")
            return None

    def add_leader(self, club_id, leader_idnumber):
        try:
            query = "INSERT INTO leadership (club_id, leader_idnumber) VALUES (%s, %s)"
            values = (club_id, leader_idnumber)
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            # Log or handle the error
            print(f"Error adding leader: {err}")

    def retrieve_club(self, club_name):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM clubs WHERE clubName = %s"
        cursor.execute(query, (club_name,))
        club_row = cursor.fetchone()  
        if club_row:
            return club_row
        else:
            return None
        
    def retrieve_all_club(self):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clubs")
        club_list = cursor.fetchall()
        return club_list

    def search_clubs(self, query):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        search_query = "SELECT * FROM clubs WHERE Clubname LIKE %s"
        cursor.execute(search_query, ('%' + query + '%',))
        club_list = cursor.fetchall()
        return club_list   
  
  
    def get_password(self, idnumber):
        try:
            query = "SELECT password FROM student WHERE idnumber = %s"
            self.cursor.execute(query, (idnumber,))
            student = self.cursor.fetchone()
            if student:
                return student[0]  # Assuming password is the first column in the result
            else:
                return None  # Return None if the student with the given idnumber doesn't exist
        except mysql.connector.Error as error:
            print("Error retrieving password:", error)
            return None 
        
    def retrieve_club_by_id(self, club_id):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM clubs WHERE Id = %s"
        cursor.execute(query, (club_id,))
        club_row = cursor.fetchone()  
        if club_row:
            
            return club_row
        else:
            return None
  
    def add_member(self, club_id, id_number, name, email, phone_number):
        query = "INSERT INTO club_member (club_id, student_id, student_name, student_email, phone_number) VALUES (%s, %s, %s, %s, %s)"
        values = (club_id, id_number, name.strip(), email.strip(), phone_number)
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return "Successfully joined the club"
        except Exception  as err:
            return "Error occured while joining the club"

    def check_membership(self, club_id, student_id):
        query = "SELECT * FROM club_member WHERE club_id = %s AND student_id = %s"
        self.cursor.execute(query, (club_id, student_id))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False
    

    def check_student(self, idnumber):
        
        query = "SELECT * FROM student WHERE Idnumber = %s"
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (idnumber,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return False
    
    def get_club_members(self, club_id):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT student_id, student_name, student_email, phone_number FROM club_member WHERE club_id = %s"
        try:
            cursor.execute(query, (club_id,))
            members = cursor.fetchall()
            return members
        except mysql.connector.Error as err:
            print(f"Error retrieving club members: {err}")
            return None
    
    def get_club_leader_id(self, club_id):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT leader_idnumber FROM leadership WHERE club_id = %s"
        try:
            cursor.execute(query, (club_id,))
            leader_id = cursor.fetchone()
            if leader_id:
                return leader_id['leader_idnumber'] 
            else:
                return None 
        except mysql.connector.Error as err:
            return f"Error retrieving club leader ID: {err}"
         


    def check_lead(self, idnumber):
        query = "SELECT * FROM Leadership WHERE leader_idnumber = %s "
        self.cursor.execute(query, (idnumber,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False
        
    def is_leader(self, club_id, leader_id):
        query = "SELECT COUNT(*) FROM leadership WHERE club_id = %s AND leader_idnumber = %s"
        try:
            self.cursor.execute(query, (club_id, leader_id))
            result = self.cursor.fetchone()[0]
            return result > 0 
        except mysql.connector.Error as err:
            print(f"Error checking leader: {err}")
            return False
        
        
    def get_name(self, idnumber):
        query = "SELECT first_name, last_name FROM student WHERE idnumber = %s"

        self.cursor.execute(query, (idnumber,))
        result = self.cursor.fetchone()
        if result:
            full_name = result[0] + " " + result[1]
            return full_name
        else:
            return False

    def add_student(self, student):
        query = "INSERT INTO Student (first_name, last_name, idnumber, password, account_type, gender, dob, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            student.first_name.strip(),
            student.last_name.strip(),
            student.idnumber,
            student.password.strip(),  
            student.account_type.strip(),
            student.gender.strip(),
            student.dob, 
            student.phone,
            student.email.strip()
        )
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            if student.account_type == "Student":
                return "Student Account Created Successfully"
            else: 
                return "Leader Account Created Successfully"
        except Exception as e:
            self.connection.rollback()
            return "Error occurred while creating student account:" + str(e)
        

    def get_club_id_by_leader(self, leader_id):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT club_id FROM leadership WHERE leader_idnumber = %s"
        try:
            cursor.execute(query, (leader_id,))
            result = cursor.fetchone()
            if result:
                return result['club_id']  # Assuming 'club_id' is the name of the column containing the club ID
            else:
                return None
        except mysql.connector.Error as err:
            return None
        
    def check_login_info(self, idnumber, password):
        query = "SELECT * FROM student WHERE idnumber = %s AND password = %s"
        try:
            self.cursor.execute(query, (idnumber, password))
            student = self.cursor.fetchone()
            if student:
                return True  # Return the student record if credentials are valid
            else:
                return False  # Return None if credentials are invalid
        except mysql.connector.Error as err:
            print(f"Error checking login info: {err}")
            return None
        

    def get_clubs_by_membership(self, idnumber):
        conn = self.connection
        cursor = conn.cursor(dictionary=True)
        query = "SELECT c.clubName FROM clubs c INNER JOIN club_member cm ON c.id = cm.club_id WHERE cm.student_id = %s"
        try:
            cursor.execute(query, (idnumber,))
            clubs = cursor.fetchall()
            return clubs
        except mysql.connector.Error as err:
            print(f"Error retrieving clubs by membership: {err}")
            return None
    
    def get_clubs_by_leadership(self, idnumber):
        try:
            conn = self.connection
            cursor = conn.cursor(dictionary=True)
            query = "SELECT c.clubName FROM clubs c INNER JOIN leadership l ON c.id = l.club_id WHERE l.leader_idnumber = %s"
            cursor.execute(query, (idnumber,))
            clubs = cursor.fetchall()
            cursor.close()  # Close the cursor after fetching results
            return clubs
        except mysql.connector.Error as err:
            return f"Error retrieving clubs by leadership: {err}"
            
          
  
        
    def edit_club(self,original_club_name, edited_club_name, edited_description):
            conn = self.connection
            cursor = conn.cursor()

            query = "UPDATE clubs SET clubName = %s, description = %s WHERE clubName = %s"
            cursor.execute(query, (edited_club_name.strip(), edited_description.strip(), original_club_name))
            conn.commit()
            return True
        
    def add_notification(self, notification):
        try:
            # Assuming self.connection is your database connection object
            cursor = self.connection.cursor()

            # Assuming your notifications table is named 'notifications'
            query = "INSERT INTO notification (club_id, subject, message, type, timestamp) VALUES (%s, %s, %s, %s, %s)"
            values = (notification.club_id, notification.subject.strip(), notification.message.strip(), notification.type.strip(), notification.timestamp)
            
            cursor.execute(query, values)
            self.connection.commit()
            return "Successful"  
        except mysql.connector.Error as err:
            return f"Error adding notification: {err}"

        
            

    def get_notifications(self, club_id):
        try:
            # Assuming self.connection is your database connection object
            cursor = self.connection.cursor(dictionary=True)

            # Query to fetch notifications for a specific club ID
            query = "SELECT subject, message, type, TIME(timestamp) as time, DATE (timestamp) as date FROM notification WHERE club_id = %s"
            cursor.execute(query, (club_id,))

            # Fetch all the notifications
            notifications = cursor.fetchall()
            return notifications
        except mysql.connector.Error as err:
            print(f"Error retrieving notifications: {err}")
            return None
        
    