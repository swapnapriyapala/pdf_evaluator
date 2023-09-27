# Create Query

# User Table Query
- create table users(userid int NOT NULL AUTO_INCREMENT primary key,username varchar(26),email varchar(30),pnnumber int(21),hcdu varchar(40),password varchar(20)); 

# PDF upload Query

- 
CREATE TABLE pdfupload (
    pdfid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    userid INT,
    FOREIGN KEY (userid) REFERENCES users(userid)
);

fk_attendant_cc character_varying(15)

# Get pdf content:

<embed src="{{ url_for('static', filename='uploads/' + pdf_filename) }}" width="800" height="600" type="application/pdf">
