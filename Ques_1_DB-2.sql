CREATE DATABASE IF NOT EXISTS test;

-- Switch to the newly created database
USE test;

CREATE TABLE IF NOT EXISTS NEEV_Members (
    M_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Identification_ID BIGINT,
    Gender ENUM('Male', 'Female'),
    Designation VARCHAR(255),
    Photo VARCHAR(255),
    Password VARCHAR(255),
    Phone_No VARCHAR(20)
);
INSERT INTO NEEV_Members (M_ID,Name, Email, Identification_ID, Gender, Designation, Photo, Password, Phone_No)
VALUES 
    (1,'John Smith', 'john@example.com', 1234567890, 'Male', 'Manager', 'link_to_photo', 'password1', '123-456-7890'),
    (2,'Emily Jones', 'emily@example.com', 0987654321, 'Female', 'Developer', 'link_to_photo', 'password2', '987-654-3210'),
    (3,'Michael Lee', 'michael@example.com', 1357924680, 'Male', 'Analyst', 'link_to_photo', 'password3', '456-789-1230'),
    (4,'Sarah Brown', 'sarah@example.com', 2468013579, 'Female', 'Designer', 'link_to_photo', 'password4', '789-123-4560'),
    (5,'David Kim', 'david@example.com', 3692581470, 'Male', 'Intern', 'link_to_photo', 'password5', '321-654-9870');
    SELECT * FROM NEEV_Members;
    
CREATE TABLE IF NOT EXISTS Students (
    S_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Identification_ID BIGINT,
    Gender ENUM('Male', 'Female'),
    Photo VARCHAR(255),
    Family_Background VARCHAR(255),
    Address VARCHAR(255),
    M_ID INT,
    FOREIGN KEY (M_ID) REFERENCES NEEV_Members(M_ID)
);

-- Insert data into the table
INSERT INTO Students (S_ID, Name, Email, Identification_ID, Gender, Photo, Family_Background, Address, M_ID)
VALUES 
    (0001, 'Johny Pal', 'john@example.com', 1234567890, 'Male', 'photo.jpg', 'Upper class', '123 Main St, City', 1),
    (0002, 'Emma Brown', 'emma@example.com', 0987654321, 'Female', 'pic.jpg', 'Middle class', '456 Elm St, Town', 2),
    (0003, 'Michael Lee', 'michael@example.com', 4567890123, 'Male', 'image.jpg', 'Lower class', '789 Oak St, Village', 3),
    (0004, 'Sarah Johnson', 'sarah@example.com', 9876543210, 'Female', 'img.jpg', 'Upper middle class', '321 Pine St, City', 4),
    (0005, 'David Wilson', 'david@example.com', 1357902468, 'Male', 'photo2.jpg', 'Lower middle class', '654 Cedar St, Town', 5),
    (0006, 'Emily Davis', 'emily@example.com', 2468013579, 'Female', 'pic2.jpg', 'Upper class', '987 Maple St, City', 1),
    (0007, 'Daniel Martinez', 'daniel@example.com', 5791357024, 'Male', 'image2.jpg', 'Lower class', '258 Oak St, Village', 1),
    (0008, 'Olivia Taylor', 'olivia@example.com', 7024579135, 'Female', 'img2.jpg', 'Middle class', '753 Elm St, Town', 3),
    (0009, 'James Brown', 'james@example.com', 0147852369, 'Male', 'photo3.jpg', 'Lower middle class', '159 Cedar St, City', 3),
    (0010, 'Sophia Garcia', 'sophia@example.com', 3691478520, 'Female', 'pic3.jpg', 'Upper middle class', '852 Pine St, Town', 3);

SELECT * FROM Students;

    CREATE TABLE IF NOT EXISTS Volunteer(
    V_ID INT NOT NULL,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Identification_ID BIGINT,
    Gender VARCHAR(10),
    Photo VARCHAR(255),
    Phone_No VARCHAR(20),
    M_ID INT,
    FOREIGN KEY (M_ID) REFERENCES NEEV_Members(M_ID),
    Address VARCHAR(255),
    PRIMARY KEY (V_ID)
);
INSERT INTO Volunteer (V_ID, Name, Email, Identification_ID, Gender, Photo, Phone_No, M_ID, Address) VALUES
(1, 'Steve Smith', 'steve@example.com', 123456789, 'Male', '[Link]', '123-456-789', 1, '123 Main St, City'),
(2, 'Emily Johnson', 'emily@example.com', 987654321, 'Female', '[Link]', '987-654-321', 2, '456 Oak Ave, Town'),
(3, 'Michael Brown', 'michael@example.com', 567890123, 'Male', '[Link]', '567-890-123', 1, '789 Elm St, Village'),
(4, 'Sarah Davis', 'sarah@example.com', 456789012, 'Female', '[Link]', '456-789-012', 4, '321 Pine St, County'),
(5, 'David Wilson', 'david@example.com', 234567890, 'Male', '[Link]', '234-567-890', 1, '654 Maple Dr, Township');
SELECT * FROM Volunteer;

 CREATE TABLE IF NOT EXISTS Instructors(
I_ID INT NOT NULL,
Name VARCHAR(255) NOT NULL, 
Email VARCHAR(255) NOT NULL,
Phone_No VARCHAR(12) NOT NULL,
Gender ENUM( 'Male', 'Female') NOT NULL, 
Identification_ID VARCHAR(9) NOT NULL, 
Type ENUM( 'Full', 'Part') NOT NULL, 
PRIMARY KEY (I_ID),
S_ID INT NOT NULL, 
FOREIGN KEY (S_ID) REFERENCES Students(S_ID),
M_ID INT NOT NULL, 
FOREIGN KEY (M_ID) REFERENCES NEEV_Members(M_ID)
);
INSERT INTO Instructors (I_ID, Name, Email, Phone_No, Gender, Identification_ID, Type, S_ID, M_ID) VALUES 
(101, 'John Doe', "johndoe@example.com", '123-456-789','  Male', '123456789', 'Full', '0001', 1 ), 
(102, 'Jane Smith', 'janesmith@example.com', '987-654-321', 'Female', '987654321', 'Part', '0007', 1), 
(103, 'Alex Lee', 'alexlee@example.com', '456-789-012', 'Male', '456789012', 'Full', '0002', 1), 
(104, 'Emily Chen', 'emilychen@example.com', '741-852-963', 'Female', '741852963', 'Full', '0003', 2), 
(105, 'Mark Kim', 'markkim@example.com', '369-258-147', 'Male', '369258147', 'Part', '0010', 1);

select*from Instructors;


CREATE TABLE Course (
    C_ID INT PRIMARY KEY,
    Course_name VARCHAR(255),
    Details VARCHAR(255),
    Venue VARCHAR(255)
);

INSERT INTO Course (C_ID, Course_name, Details, Venue) VALUES
(101, 'Mathematics', 'Introduction to Algebra', 'Room 201'),
(102, 'Literature', 'Shakespearean Plays Analysis', 'Auditorium'),
(103, 'History', 'World War II Overview', 'Room 103'),
(104, 'Computer Science', 'Python Programming Basics', 'Lab 301'),
(105, 'Biology', 'Cellular Biology', 'Room 202');

SELECT * FROM Course;


CREATE TABLE Donation (
D_ID INT PRIMARY KEY,
Donor_Name VARCHAR (255), 
Amount DECIMAL (10, 2), 
Details VARCHAR(255), 
Phone_No VARCHAR(15),
Email VARCHAR(255)
);
	INSERT INTO Donation (D_ID, Donor_Name, Amount, Details, Phone_No, Email) VALUES 
	(11, 'Joey Tribianni', 100, 'Transaction ID', '123-456-789', 'johntribianni@example.com'), 
    (12, 'Jane Smith', 250, 'Transaction ID', '987-654-321', 'janesmith@example.com'),
    (23, 'Alice Lee', 50, 'Transaction ID', '555-123-456', 'alicelee@example.com'),
    (54, 'Bob Johnson', 150, 'Transaction ID', '111-222-333', 'bobjohnson@example.com'),
    (55, 'Sarah Brown', 75, 'Transaction ID', '444-555-666', 'sarahbrown@example.com');
    SELECT * FROM donation;
    
    CREATE TABLE  IF NOT EXISTS Admin (
AD_ID INT AUTO_INCREMENT PRIMARY KEY,
Email VARCHAR(255) NOT NULL, Name VARCHAR(255) NOT NULL,
Password VARCHAR(255) NOT NULL
);
INSERT INTO Admin (Email, Name, Password)
VALUES ('admin1@example.com', 'John Doe', 'johndoe123');

SELECT * FROM Admin;



CREATE TABLE STUDENT_COURSE (
    S_ID INT,
    C_ID INT,
    FOREIGN KEY (S_ID) REFERENCES Students(S_ID),
    FOREIGN KEY (C_ID) REFERENCES Course(C_ID),
    PRIMARY KEY (S_ID, C_ID)
);
INSERT INTO STUDENT_COURSE (S_ID,C_ID)
VALUES (0001,101),
(0002,101);

SELECT * FROM STUDENT_COURSE;


CREATE TABLE VOLUNTEER_COURSE (
    V_ID INT,
    C_ID INT,
    FOREIGN KEY (V_ID) REFERENCES Volunteer(V_ID),
    FOREIGN KEY (C_ID) REFERENCES Course(C_ID),
    PRIMARY KEY (V_ID, C_ID)
);
INSERT INTO VOLUNTEER_COURSE (V_ID,C_ID)
VALUES (1,101),
(2,102);

SELECT * FROM VOLUNTEER_COURSE;

CREATE TABLE Funds (
    D_ID INT,
    AD_ID INT,
    FOREIGN KEY (D_ID) REFERENCES Donation(D_ID),
    FOREIGN KEY (AD_ID) REFERENCES Admin(AD_ID),
    PRIMARY KEY (D_ID, AD_ID)
);
INSERT INTO Funds (D_ID,AD_ID)
VALUES (12,1),
(11,1);
SELECT * FROM Funds;


CREATE TABLE Active_courses (
    I_ID INT,
    C_ID INT,
    FOREIGN KEY (I_ID) REFERENCES Instructors(I_ID),
    FOREIGN KEY (C_ID) REFERENCES Course(C_ID),
    PRIMARY KEY (I_ID, C_ID)
);
INSERT INTO Active_courses (I_ID,C_ID)
VALUES (101,102),
(102,103);
SELECT * FROM Active_courses;



