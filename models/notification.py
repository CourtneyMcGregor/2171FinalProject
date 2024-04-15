class Notification:
    def __init__(self, club_id, subject, message, type, timestamp):
        self.club_id = club_id
        self.subject = subject
        self.message = message
        self.type = type
        self.timestamp = timestamp