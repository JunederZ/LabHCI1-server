import mysql.connector
from argon2 import PasswordHasher

class DBUtil:
    def conn(self):
        mydb = mysql.connector.connect(
            host="ned.masuk.id",
            user="uiulutbl_hci",
            password="kipasangin12",
            database="uiulutbl_hci",
        )
        return mydb

    def addUser(self, username, password, device_id, full_name):
        ph = PasswordHasher()
        hashed_pass = ph.hash(password)
        conn = self.conn()
        cur = conn.cursor()
        sql = "INSERT INTO userData (username, password, deviceID, fullName) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (username, hashed_pass, device_id, full_name))
        conn.commit()

    def getByUDID(self, UDID):
        conn = self.conn()
        cur = conn.cursor()
        sql = "select * from userData where deviceID=%s"
        cur.execute(sql, (UDID,))
        res = cur.fetchone()
        return res
    

