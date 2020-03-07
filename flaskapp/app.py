from flask import Flask, render_template, request, json
from flask_cors import CORS
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)
mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "admin"
app.config["MYSQL_DATABASE_PASSWORD"] = "PasswordPassword"
app.config["MYSQL_DATABASE_DB"] = "BucketListDEV"
app.config[
    "MYSQL_DATABASE_HOST"
] = "development.cnvajlvavtpv.us-east-1.rds.amazonaws.com"
app.config["MYSQL_DATABASE_PORT"] = 8056
mysql.init_app(app)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")


@app.route("/signUp", methods=["POST"])
def signUp():
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


if __name__ == "__main__":
    app.debug = True
    app.run()
