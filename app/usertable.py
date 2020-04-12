
from database import Database
import json
import utils

class UserTable(Database):

    def get(self, id):

        sql =  "SELECT id,useremail,username,userphone,userdesc,views "
        sql += "FROM users "
        sql += "WHERE id={};".format(id)

        print("DEBUG SQL ===>{}".format(sql))

        result = ()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            return {"error" : "{}".format(e)}

        result = {} if len(result) == 0 else result[0]

        return result


    def list(self,page=0, itemsInPage=20):
        page = page * itemsInPage;
        sql =  "SELECT id,useremail,username,userphone,userdesc,views "
        sql += "FROM users "
        sql += "LIMIT {page},{itemsInPage};".format(page=page,itemsInPage=itemsInPage)

        print("DEBUG SQL ===>{}".format(sql))

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result


    def insert(self, j):

        sql = "INSERT INTO users(useremail,username,userphone,userdesc) "
        sql = sql + "values('{useremail}','{username}','{userphone}','{userdesc}')".format(
            useremail = utils.addslashes( j.get("useremail","")),
            username = utils.addslashes( j.get("username","")),
            userphone = utils.addslashes( j.get("userphone","")),
            userdesc = utils.addslashes( j.get("userdesc",""))
            )

        print("DEBUG SQL ===>{}".format(sql))
        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error" : "{}".format(e)}

        return result


    def update(self, id, j):

        useremail = j.get("useremail","")
        username = j.get("username","")
        userphone = j.get("userphone","")
        userdesc = j.get("userdesc","")

        sql = "UPDATE users SET "
        if len(useremail) > 0:
            sql += " useremail = '{}', ".format(useremail)
        if len(username) > 0:
            sql += " username = '{}', ".format(username)
        if len(userphone) > 0:
            sql += " userphone = '{}', ".format(userphone)
        if len(userdesc) > 0:
            sql += " userdesc = '{}', ".format(userdesc)

        sql += " views = views "
        sql += " WHERE id = {} ".format(id)

        print("DEBUG SQL ===>{}".format(sql))        


        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error" : "{}".format(e)}

        return result


    def delete(self, id):

        sql =  "DELETE FROM users "
        sql += " WHERE id = '{}' ".format(id)

        print("DEBUG SQL ===>{}".format(sql))

        result = None
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            result = {"error" : "{}".format(e)}

        return result