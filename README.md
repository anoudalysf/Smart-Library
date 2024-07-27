### BE: GenAI Addition
## Recommendation API Requests :

# Recommendation API Request Based on a user's registered preference :
<img width="1415" alt="Screenshot 1446-01-21 at 5 21 17 PM" src="https://github.com/user-attachments/assets/5ebcaa57-20e2-4918-bf63-6565e4dc4d75">
<img width="580" alt="Screenshot 1446-01-21 at 5 20 58 PM" src="https://github.com/user-attachments/assets/0c704935-9528-4876-bb6c-d557fb1a8ce0">
<img width="473" alt="Screenshot 1446-01-21 at 5 19 51 PM" src="https://github.com/user-attachments/assets/5ff35906-4b91-4618-96f9-b7614816d4ed">

# Recommendation API Request Based on a user's query request :
<img width="555" alt="Screenshot 1446-01-21 at 5 17 58 PM" src="https://github.com/user-attachments/assets/0d0c4ebf-c20b-4704-97ed-fde72c705d43">
<img width="1439" alt="Screenshot 1446-01-21 at 5 18 38 PM" src="https://github.com/user-attachments/assets/721ec271-4d89-4208-a004-c5dd27cd2d26">



## How to create  the postgresql database :

1-

     CREATE DATABASE Smart_Library_Database;

or if you want to drop it

     DROP DATABASE Smart_Library_Database;

2-

       \c smart_library_database
3-

      CREATE TABLE Users (
         User_ID VARCHAR(50) PRIMARY KEY NOT NULL,
         UserName VARCHAR(50) UNIQUE NOT NULL,
         password_hash VARCHAR(255) NOT NULL,
         Role VARCHAR(50) NOT NULL,
         CONSTRAINT check_role CHECK (Role IN ('User', 'Admin'))
     );

     CREATE TABLE Authors (
         Author_ID SERIAL PRIMARY KEY NOT NULL,
         First_Name VARCHAR(50) NOT NULL,
         Last_Name VARCHAR(50) NOT NULL,
         Biography VARCHAR(300) NOT NULL
     );

     CREATE TABLE Books (
         Book_ID SERIAL PRIMARY KEY NOT NULL,
         Title VARCHAR(80) NOT NULL,
         Author_ID INT NOT NULL,
         Genre VARCHAR(50) NOT NULL,
         Description VARCHAR(250) NOT NULL,
         CONSTRAINT key_author FOREIGN KEY (Author_ID) REFERENCES Authors(Author_ID),
         CONSTRAINT check_genre CHECK (Genre IN ('Fiction', 'Nonfiction', 'Biography', 'History', 'Science Fiction'))
     );

     CREATE TABLE UserPreferences (
         Preference_ID SERIAL PRIMARY KEY NOT NULL,
         User_ID VARCHAR(50) NOT NULL,
         Preferences VARCHAR(200) NOT NULL,
         CONSTRAINT key_user FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
     );

     CREATE TABLE Logs (
         Logs_ID SERIAL PRIMARY KEY NOT NULL,
         User_ID VARCHAR(50) NOT NULL,
         TimeStamp VARCHAR(50) NOT NULL,
         Endpoint VARCHAR(200) NOT NULL,
         Method_Type VARCHAR(200) NOT NULL,
         CONSTRAINT key_user FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
     );

4- Insert data

     INSERT INTO Authors (First_Name, Last_Name, Biography)
     VALUES ('Jane', 'Austen', 'English novelist known primarily for her six major novels which interpret, critique and comment upon the British landed gentry at the end of the 18th century.');

     -- Insert data into Books
     -- No need to specify Book_ID if it's an auto-incrementing field
     INSERT INTO Books (Title, Author_ID, Genre, Description)
     VALUES ('Pride and Prejudice', 1, 'Fiction', 'The novel follows the character development of Elizabeth Bennet, the dynamic protagonist, who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.');

     -- Insert data into Users
     INSERT INTO Users (User_ID, UserName, password_hash, Role)
     VALUES ('1', 'Monerah', 'password123', 'User');

     -- Insert data into UserPreferences
     INSERT INTO UserPreferences (Preference_ID, User_ID, Preferences)
     VALUES ('1', '1', 'biographies');


## Unit Testing:
 # Authors

<img width="1112" alt="Screenshot 1446-01-12 at 2 12 38 PM" src="https://github.com/user-attachments/assets/a6b190f8-1734-41d6-b8af-62d5e1218cc0">
