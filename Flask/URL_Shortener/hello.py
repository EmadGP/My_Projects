import string
import random

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "EMADs137ld"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'url'

mysql = MySQL(app)

def random_url():
    random_url = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    return random_url
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        x = random_url()
        if not url:
            flash("URL bar can not be empty", "error")
            return render_template("index.html")

        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute('''INSERT INTO urls VALUES (%s,%s)''', (url,x))
                mysql.connection.commit()
                flash("URL submitted successfully", "succes")
                return redirect(url_for("home"))
        except mysql.connection.Error as e:
            flash(f"Database error: {e}", "error")
            return render_template("index.html")
        return render_template("index.html")


    return render_template("index.html")
