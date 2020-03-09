import os

from flask import Flask, render_template, request, json
from flask_cors import CORS
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)
mysql = MySQL()


# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = os.getenv("user_name", "test")
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("user_pwd", "test_pwd")
app.config["MYSQL_DATABASE_DB"] = os.getenv("database_db", "BucketListDEV")
app.config["MYSQL_DATABASE_HOST"] = os.getenv(
    "db_host", "development.cnvajlvavtpv.us-east-1.rds.amazonaws.com"
)
app.config["MYSQL_DATABASE_PORT"] = os.getenv("db_port", 8056)
mysql.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/showSignUp")
def show_sign_up():
    return render_template("signup.html")


@app.route("/signUp", methods=["POST"])
def sign_up():
    # read the posted values from the UI
    _name = request.form["inputName"]
    _email = request.form["inputEmail"]
    _password = request.form["inputPassword"]

    # validate the received values
    if _name and _email and _password:

        _hashed_password = generate_password_hash(_password)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc("sp_createUser", (_name, _email, _hashed_password))

        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({"message": "User created successfully !"})
        else:
            return json.dumps({"error": str(data[0])})

    else:
        return json.dumps({"html": "<span>Enter the required fields</span>"})


def main():
    app.run(debug=False)
