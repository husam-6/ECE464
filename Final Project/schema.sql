CREATE TABLE USERS(
    uid: INTEGER,
    password: VARCHAR(20),
    GPA: FLOAT,
    pid: INTEGER,
    FOREIGN KEY (pid),
    PRIMARY KEY (uid));n

CREATE TABLE NOTIFICATIONS(
    nid: INTEGER,
    aid: INTEGER,
    notifType: VARCHAR(30),
    notifDate: DATE,
    snoozeTimer: INTEGER,
    PRIMARY KEY (nid),
    FOREIGN KEY (aid));

CREATE TABLE GRADES(
    gid: INTEGER,
    assignment: VARCHAR(20),
    aid: INTEGER,
    uid: INTEGER,
    weight: FLOAT,
    grade: FLOAT,
    PRIMARY KEY (gid),
    FOREIGN KEY (uid, aid));

CREATE TABLE PLANNER(
    aid: INTEGER,
    uid: INTEGER, 
    dueDate: DATETIME, 
    view: BOOLEAN, 
    PRIMARY KEY(AID), 
    FOREIGN KEY(UID));

CREATE TABLE ANNOUNCEMENTS(
    announcement: VARCHAR(30),
    description: VARCHAR(100));

CREATE TABLE ASSIGNMENTS(
    assignmentName: VARCHAR(30),
    className: VARCHAR(30),
    completedDate: DATETIME,
    type: VARCHAR(30));
