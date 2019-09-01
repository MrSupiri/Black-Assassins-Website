from flask import Flask, render_template, request, redirect, flash, jsonify
from users import app_users
from cod4 import app_cod4
from flask_mail import Mail
from database.database import database
from random import shuffle

app = Flask(__name__)
app.secret_key = '\xdfyJ\xfeh!\x82\xc1\xd5\x014\x06*J\x7f\xd1\xcaqi\xffn)\x1e\x11'
app.register_blueprint(app_users)
app.register_blueprint(app_cod4)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='legionsesport@gmail.com',
    MAIL_PASSWORD='LegionS12345678'
)
mail = Mail(app)


@app.route('/')
def homepage():
    try:
        db = database()
        data = db.read('''SELECT ID,Name FROM ScreenShots WHERE Banned IS NULL ORDER BY ID DESC''')[:100]
        db.close()
        shuffle(data)
        return render_template("home.html", fullwidth=True, ss=data[:6])
    except:
        return render_template("home.html", fullwidth=True)


@app.route('/ads_blocker')
def adsblocker():
    return render_template("adsblocker.html", fullwidth=True)


if __name__ == "__main__":
    app.run()
