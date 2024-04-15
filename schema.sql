DROP DATABASE IF EXISTS Project2171;
CREATE DATABASE Project2171;

    USE Project2171;

CREATE USER 'kraem'@'localhost' IDENTIFIED BY 'Custodian';

GRANT ALL PRIVILEGES ON Project2171.* TO 'kraem'@localhost;

CREATE TABLE clubs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clubName VARCHAR(255) ,
    description VARCHAR(255) ,
    clubLeader VARCHAR(255)
);

CREATE TABLE student (
    idnumber INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    account_type VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    dob DATE,
    phone VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE club_member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT,
    student_id INT,
    student_name  VARCHAR(255),
    student_email VARCHAR(255),
    phone_number VARCHAR(255),
    FOREIGN KEY (club_id) REFERENCES clubs(id),
    FOREIGN KEY (student_id) REFERENCES student(idnumber),
    UNIQUE (club_id, student_id)
);


CREATE TABLE leadership (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT,
    leader_idnumber INT,
    FOREIGN KEY (club_id) REFERENCES clubs(id),
    FOREIGN KEY (leader_idnumber) REFERENCES student(idnumber),
    UNIQUE (club_id, leader_idnumber)
);


CREATE TABLE notification (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT,
    subject VARCHAR(255),
    message TEXT,
    type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id)
);

