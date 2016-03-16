from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import jsonify
import MySQLdb
from MySQLdb import escape_string as thwart
import gc
app = Flask(__name__)

def db_connect():
    conn = MySQLdb.connect(
        host="sqltest.chbtyotwmrhe.us-east-1.rds.amazonaws.com",
        user = "kent",
        passwd = "1234567890",
        db = "testdataset")

    c = conn.cursor()

    return c, conn


@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return redirect('/users')


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        try:
            c, conn = db_connect()

            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')

            c.execute(
                "INSERT INTO Users (firstname, lastname, email) VALUES (%s, %s, %s)",
                (thwart(first_name), thwart(last_name), thwart(email)))

            conn.commit()
            c.close()
            conn.close()
            gc.collect()
        except Exception as e:
            print str(e)
            return jsonify(success=False)

        return jsonify(
            success=True,
            firstname=first_name,
            lastname=last_name,
            email=email)
    else:
        try:
            c, conn = db_connect()
            c.execute("SELECT * FROM Users")
            results = c.fetchall()
            c.close()
            conn.close()
            gc.collect()
        except Exception as e:
            return(str(e))

        users = []
        for row in results:
            users.append({
                'id': row[0],
                'firstname': row[1],
                'lastname': row[2],
                'email': row[3]
            })
            print row[0]

        return render_template('register.html', users=users)


if __name__ == "__main__":
    app.run(debug=True)