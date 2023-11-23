-- create database called dbms_project
CREATE DATABASE dbms_project;
use dbms_project;

CREATE TABLE USER (
    USER_ID INT NOT NULL AUTO_INCREMENT,
    USER_NAME VARCHAR(50) NOT NULL,
    PASSWORD VARCHAR(50) NOT NULL,
    EMAIL VARCHAR(50) NOT NULL,
    -- NOTIFICATION VARCHAR(50),
    PRIMARY KEY (USER_ID)
);

CREATE TABLE USER_PHONE (
    USER_ID INT NOT NULL,
    PHONE_NUMBER VARCHAR(50) NOT NULL,
    PRIMARY KEY (USER_ID, PHONE_NUMBER),
    FOREIGN KEY (USER_ID) REFERENCES USER(USER_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE CALENDAR (
    CALENDAR_ID INT NOT NULL AUTO_INCREMENT,
    CALENDAR_NAME VARCHAR(50) NOT NULL,
    USER_ID INT NOT NULL,
    PRIMARY KEY (CALENDAR_ID),
    FOREIGN KEY (USER_ID) REFERENCES USER(USER_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE EVENTS (
    EVENT_ID INT NOT NULL AUTO_INCREMENT,
    EVENT_TITLE VARCHAR(50) NOT NULL,
    EVENT_DESCRIPTION VARCHAR(50),
    START_TIME DATETIME NOT NULL,
    END_TIME DATETIME NOT NULL,
    CALENDAR_ID INT NOT NULL,
    STATE_ VARCHAR(50),
    CITY VARCHAR(50),
    ZIPCODE VARCHAR(50), 
    DURATION INT AS (TIMESTAMPDIFF(MINUTE, START_TIME, END_TIME)) STORED,
    PRIMARY KEY (EVENT_ID),
    FOREIGN KEY (CALENDAR_ID) REFERENCES CALENDAR(CALENDAR_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE TASK (
    TASK_ID INT NOT NULL AUTO_INCREMENT,
    TASK_TITLE VARCHAR(50) NOT NULL,
    TASK_DESCRIPTION TEXT,
    DUE_TIME DATETIME NOT NULL,
    STATUS_ ENUM('COMPLETED', 'INCOMPLETE') NOT NULL DEFAULT 'INCOMPLETE',
    CALENDAR_ID INT NOT NULL,
    PRIMARY KEY (TASK_ID),
    FOREIGN KEY (CALENDAR_ID) REFERENCES CALENDAR(CALENDAR_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE NOTES (
    NOTE_ID INT NOT NULL AUTO_INCREMENT,
    NOTE_DESCRIPTION VARCHAR(500),
    DATE_CREATED DATETIME NOT NULL,
    CALENDAR_ID INT NOT NULL,
    PRIMARY KEY (NOTE_ID),
    FOREIGN KEY (CALENDAR_ID) REFERENCES CALENDAR(CALENDAR_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE COLLABORATION (
    COLLABORATION_ID INT NOT NULL AUTO_INCREMENT,
    USER_ID1 INT NOT NULL,
    USER_ID2 INT NOT NULL,
    TASK_ID INT NOT NULL,
    PRIMARY KEY (COLLABORATION_ID, USER_ID1, USER_ID2, TASK_ID),
    FOREIGN KEY (USER_ID1) REFERENCES USER(USER_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (USER_ID2) REFERENCES USER(USER_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (TASK_ID) REFERENCES TASK(TASK_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- CREATE TABLE REMINDER (
--     REMINDER_ID INT NOT NULL AUTO_INCREMENT,
--     REMINDER_DESCRIPTION VARCHAR(50),
--     REMINDER_TIME DATETIME NOT NULL,
--     EVENT_ID INT NOT NULL,
--     TASK_ID INT NOT NULL,
--     PRIMARY KEY (REMINDER_ID, EVENT_ID, TASK_ID),
--     FOREIGN KEY (EVENT_ID) REFERENCES EVENTS(EVENT_ID)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE,
--     FOREIGN KEY (TASK_ID) REFERENCES TASK(TASK_ID)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE
-- );

CREATE TABLE SHARES (
    USER_ID INT NOT NULL,
    COLLABORATION_ID INT NOT NULL,
    PRIMARY KEY (USER_ID, COLLABORATION_ID),
    FOREIGN KEY (USER_ID) REFERENCES USER(USER_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (COLLABORATION_ID) REFERENCES COLLABORATION(COLLABORATION_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE SHARED_WITH (
    COLLABORATION_ID INT NOT NULL,
    TASK_ID INT NOT NULL,
    PRIMARY KEY (COLLABORATION_ID, TASK_ID),
    FOREIGN KEY (COLLABORATION_ID) REFERENCES COLLABORATION(COLLABORATION_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (TASK_ID) REFERENCES TASK(TASK_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Procedure: update_task_status
DELIMITER //

CREATE PROCEDURE UpdateTaskStatus(IN task_id_param INT, IN new_status_param VARCHAR(50))
BEGIN
    UPDATE TASK SET STATUS_ = new_status_param WHERE TASK_ID = task_id_param;
END //

DELIMITER ;


-- Trigger: Event start time cannot be after end time
DELIMITER //

CREATE TRIGGER before_insert_event
BEFORE INSERT ON EVENTS
FOR EACH ROW
BEGIN
    IF NEW.START_TIME > NEW.END_TIME THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Start date cannot be greater than end date';
    END IF;
END;
//

DELIMITER ;
