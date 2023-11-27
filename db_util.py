import mysql.connector
from argon2 import PasswordHasher

class DBUtil:
    def conn(self):
        db = mysql.connector.connect(
            host="ned.masuk.id",
            user="uiulutbl_hci",
            password="kipasangin12",
            database="uiulutbl_hci",
        )
        return db
    
    def deleteUser(self, udid):
        sql = "DELETE FROM userData WHERE deviceID = %s"
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql, (udid,))
        conn.commit()

    def addUser(self, username, password, device_id, full_name, email):
        ph = PasswordHasher()
        hashed_pass = ph.hash(password)
        conn = self.conn()
        cur = conn.cursor()
        sql = "INSERT INTO userData (username, password, deviceID, fullName, email) VALUES (%s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (username, hashed_pass, device_id, full_name, email))
            conn.commit()
        except mysql.connector.errors.IntegrityError:
            return "device already exists"
        return "success"

    def getByUDID(self, UDID):
        conn = self.conn()
        cur = conn.cursor()
        sql = "select * from userData where deviceId=%s"
        cur.execute(sql, (UDID,))
        res = cur.fetchone()
        return res

    def deleteByUDID(self, UDID):
        conn = self.conn()
        cur = conn.cursor()
        sql = "DELETE FROM `userData` WHERE deviceId=%s"
        cur.execute(sql, (UDID,))
        return "success"


    
DBUtil().deleteUser('0865e807c92089cc')
