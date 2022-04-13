from flask import Flask, render_template, redirect, url_for, session,request
from flask_mysqldb import MySQL
import MySQLdb
import random

app = Flask(__name__)
app.secret_key = "123456"

app.config["MYSQL_HOST"] = "scalableservicesassignment.cz1kzfagdqhy.ap-south-1.rds.amazonaws.com"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "123Amazon"
app.config["MYSQL_DB"] = "UserInfo"

db = MySQL(app)

@app.route ( '/index' )
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'email' in request.form and 'password' in request.form and 'Log In' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM UserInfo.logininfo WHERE email= %s AND Password = %s", (email,password))
            info = cursor.fetchone()

            if info is not None and info['email'] == email and info['Password'] == password:
                session['loginsuccess'] = True
                return redirect(url_for('playVideo'))
            else:
                return "Login Error"

    return render_template("login.html")

@app.route('/PlayVideo', methods=['GET', 'POST'])
def playVideo():
    if request.method == 'POST':
        if 'Course' in request.form:
            Course = request.form['Course']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM Course.CourseVideo  WHERE ID= %s", (Course,))
            info = cursor.fetchone()
            hyperLink = info['Link']
            title = info['Title']
            cursor.execute("SELECT * FROM Course.CourseVideo")
            coursesData = []
            for row in cursor:
                coursesData.append(row)
            return render_template("PlayVideo.html", hyperLink=hyperLink, title=title,coursesData=coursesData)

    elif session['loginsuccess']:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Course.CourseVideo")
        coursesData = []
        for row in cursor:
            coursesData.append(row)
        return render_template("PlayVideo.html", coursesData=coursesData)

    else:
        return "Error"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    app.run(debug=True)