import sqlite3

# database class, establish connection to database
class Database:
        def __init__(self, db):
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
            # create table if it does not exist with these columns with table name Patient_Logs
            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS Patient_Logs
                (id INTEGER PRIMARY KEY,
                PatientNo integer,
                DateOfVisit text,
                FirstName text,
                LastName text,
                Birthday text,
                PhoneNo text,
                Complaint text)''')
            self.conn.commit()
        # gather value from table and return rows
        def fetch(self):
            self.cur.execute("SELECT * FROM Patient_Logs")
            rows = self.cur.fetchall()
            return rows
        # insert new patient log
        def insert(self, PatientNo, DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint):
            self.cur.execute("INSERT INTO Patient_Logs VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                             (PatientNo, DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint))
            self.conn.commit()
        # remove patient log based on PatientNo provided
        def remove(self, PatientNo):
            self.cur.execute("DELETE FROM Patient_Logs WHERE PatientNo=?", (PatientNo,)) # comma is needed after PatientNo to be a tuple and to allow function to accept multiple characters
            self.conn.commit()
        # update patient log
        def update(self, PatientNo, DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint):
            self.cur.execute('''UPDATE Patient_Logs SET                             
                            DateOfVisit = ?,
                            FirstName = ?,
                            LastName = ?,
                            Birthday = ?,
                            PhoneNo = ?,
                            Complaint = ?
                            WHERE PatientNo =?''',
                             (DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint, PatientNo))

        def __del__(self):
            self.conn.close()


