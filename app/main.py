import sys

from database import Database
from flask import Flask

app = Flask(__name__)

# private SELECT query
def _select():
    db = Database()

    sql = "SELECT id, test \
           FROM smishing.testTable"
    row = db.executeAll(sql)

    return row

# INSERT 함수 예제
@app.route('/insert', methods=['GET'])
def insert():
    db = Database()
 
    sql = "INSERT INTO smishing.testTable(test) \
           VALUES('%s')"% ('testData')
    db.execute(sql)
    db.commit()

    return "inserted=>{}".format(_select())

# SELECT 함수 출력
@app.route('/select', methods=['GET'])
def select():
    return "selected=>{}".format(_select())

# UPDATE 함수 예제
@app.route('/update', methods=['GET'])
def update():
    db = Database()

    sql = "UPDATE smishing.testTable \
           SET test='%s' \
           WHERE test='testData'"% ('update_Data')
    db.execute(sql)
    db.commit()

    return "updated => {}".format(_select())

# DELETE 함수 예제
@app.route('/delete', methods=['GET'])
def delete():
    db = Database()

    sql = "DELETE FROM smishing.testTable \
           WHERE test='update_Data'"

    db.execute(sql)
    db.commit()

    return "updated => {}".format(_select())

@app.route("/")
def hello():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} on Alpine (default)".format(
        version
    )
    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
