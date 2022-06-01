import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///institute.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure SQLALCHEMY Library to use SQLite database
db = SQLAlchemy(app)


class students(db.Model):
    rollno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    birth = db.Column(db.String(40), nullable=False)
    sport = db.Column(db.String(40), nullable=False)


class teachers(db.Model):
    tno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=["GET", "POST"])
def success():
    return render_template("success.html")


@app.route("/studentlogin", methods=["GET", "POST"])
def studentlogin():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        birth = request.form['DOB']
        gender = request.form['gender']
        sport = request.form["sport"]
        student = students(name=name, email=email,
                           gender=gender, birth=birth, sport=sport)
        db.session.add(student)
        db.session.commit()
        return render_template("success.html")
    else:
        return render_template("studentlogin.html")


@app.route("/teacherlogin", methods=["GET", "POST"])
def teacherlogin():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("teacherlogin.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"

        username = request.form["username"]
        password = request.form["password"]
        sqlconnection = sqlite3.Connection("institute.db")
        cursor = sqlconnection.cursor()
        rows = cursor.execute(
            "SELECT username, password FROM teachers WHERE username = ? AND password =?", (username, password))
        row = rows.fetchall()
        if len(row) == 1:
            return render_template("loggedIn.html", username= username)
        else:
            return render_template("register.html")
    else:
        return render_template("teacherlogin.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if (password != confirm):
            return "Confirm Password Must be Same"
        else:
            teacher = teachers(username=username, password=password)
            db.session.add(teacher)
            db.session.commit()
            return render_template("teacherlogin.html")
    else:
        return render_template("teacherlogin.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("/index.html")

@app.route("/entry")
def show():
    allstudents = students.query.all()
    return render_template("entry.html",allstudents=allstudents)

@app.route("/delete/<int:rollno>")
def delete(rollno):
    student = students.query.filter_by(rollno =rollno).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/entry")

if __name__ == "__main__":
    app.run(debug=True,port = 8080)
