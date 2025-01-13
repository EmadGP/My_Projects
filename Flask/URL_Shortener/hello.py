import string
import random

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "EMADs137ld"


# <---------- configures the Flask app to connect to a MySQL database ---------->
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'url'

mysql = MySQL(app)

# <---------- Generates a random url incase a custom one hasn't been provided ---------->
def random_url():
    random_url = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    return random_url

# <---------- Handeling the url shortening logic ---------->
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # <------ Determine which url to use for the shortened version ------>

        url = request.form["url"]
        custom_url = request.form["custom_url"].replace(" ","")

        if custom_url == "":
            custom_url = random_url()

        # <------ Error handeling incase form is not filled ------>
        if not url:
            flash("URL bar can not be empty", "error")
            return render_template("index.html")

        try:
            # <------ Pushing the data into the MySQL database ------>
            with mysql.connection.cursor() as cursor:
                cursor.execute('''INSERT INTO urls VALUES (%s,%s)''', (url,custom_url))
                mysql.connection.commit()
                flash("URL submitted successfully", "succes")
                return redirect(url_for("home"))
        except mysql.connection.Error as e:
            flash(f"Database error: {e}", "error")
            return render_template("index.html")

    return render_template("index.html")

# <---------- Redirecting to the original url logic ---------->
@app.route("/<short_url>")
def redirect_to_original(short_url):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute('''SELECT ORG FROM urls WHERE Shortend= %s''', (short_url,))
            result = cursor.fetchone()

        if result:
            original_url = result[0]
            return redirect(original_url)
        else:
            flash("Shortened URL not found", "error")
            return redirect(url_for("home"))

    except mysql.connection.Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("home"))