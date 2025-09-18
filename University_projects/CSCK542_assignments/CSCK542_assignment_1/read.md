Instructions:

MySQL RDBMS

The purpose of this assignment is to analyse a system and go through design steps using MySQL RDBMS, and perform very simple data entry and database backups. You are not expected to develop any application or login on top of the database. 

A college has decided to develop a database for “admins”, “teachers”, “students” and “courses”. The database needs to support an application that enables students to select from the offered courses. 

Here are the features of the application:

Course availability for each semester is decided by college admins and students can only see the offered courses. 
Admins, assign courses to teachers.
Teachers can pass or fail students.
Here are the steps to follow for this assignment:

Discuss and write down functional and non-functional requirements.
Based on the results from functional requirements analysis, draw an ERD using your favourite tool (we recommend draw.io).
Install MySQL and MySQL Workbench on your PC.
Design tables and ensure they comply at least with NF1 and NF2. You may start by strawman design, and then implement it using MySQL Workbench or SQL commands.
Perform data entry by entry at least 10 course, 2 admin, 7 teachers and 20 students. To simplify your work, look for possibility of writing a script for batch data entry. You may use Random Data Generator (randat.com) to generate random names.
Find out about the possible database backup options and create a backup.

Before starting:

1. Create user and database in terminal
   - create database 'database_name';
   - create user 'user_name'@'localhost' identified by 'password';
   - grant all privileges on 'database_name'.* to 'user_name'@'localhost';
   - flush privileges; 

Functional
Admins set course availability per semester.
Admins assign courses to teachers (per offering). 
Students can view available courses for a semester.
Students enroll only in offered courses.
Teachers record final outcome (pass/fail) per student per offering.