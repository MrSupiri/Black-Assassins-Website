from flask import Blueprint, render_template, flash, request, redirect, session
from functools import wraps
from database.database import database
from passlib.hash import sha256_crypt
import random, string

app_users = Blueprint('app_users',__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(request.referrer)
    return wrap

@app_users.route('/login/', methods=["POST"])
def login():
	try:
		if request.method == "POST":
			db = database()
			username = request.form['username']
			data = db.read('''SELECT Username,password,AuthKey,GUID,B3ID,level FROM users WHERE username = (?)''', username)
			if len(data) == 0:
				data = db.read('''SELECT Username,password,AuthKey,GUID,B3ID,level FROM users WHERE username = (?)''', username)
			db.close()
			if len(data) == 1 and sha256_crypt.verify(request.form['password'], data[0][1]):
				session['logged_in'] = True
				session['username'] = data[0][0]
				session['authkey'] = data[0][2]
				session['guid'] = data[0][3]
				session['b3id'] = data[0][4]
				session['level'] = data[0][5]
				flash('You Have Successfully Logged in !')
				return redirect(request.referrer)
			else:
				flash('Invalid credentials. Try Again.')
				return redirect(request.referrer)
	except Exception as e:
		return redirect(request.referrer)

		
@app_users.route('/register/', methods=["POST"])
def register():
	try:
		if request.method == "POST":
			db = database()
			displayname = request.form['displayname']
			username = request.form['username']
			password = sha256_crypt.encrypt(str(request.form['password']))
			email = request.form['email']
			AuthKey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
			x = db.read("SELECT * FROM users WHERE Username = (?)",username)
			y = db.read("SELECT * FROM users WHERE Email = (?)",email)
			if len(x) > 0:
				flash('Username Already in Use')
				return redirect(request.referrer)
			if len(y) > 0:
				flash('Your Email is already Registered')
				return redirect(request.referrer)
			db.write('''INSERT INTO users(Name,Username,Password,Email,AuthKey) VALUES(?,?,?,?,?)''',displayname,username,password,email,AuthKey)
			db.close()
			flash('You Have Successfully Registered !')
			return redirect(request.referrer)
	except Exception as e:
		return render_template("home.html")
		
@app_users.route('/logout/')
@login_required
def logout():
	try:
		session.clear()
		flash("You have been logged out!")
		return redirect(request.referrer)
	except Exception as e:
		return render_template("home.html")
		
@app_users.route('/auth/', methods=["GET","POST"])
def submitss():
	try:
		if request.method == "POST" and request.form['secretkey'] == 'WK3vKwJs4ZDCV5HrthRnOGreY12mEYwS2ljpm0AI':
			db = database()
			b3id = int(request.form['b3id'])
			guid = request.form['guid']
			level = int(request.form['level'])
			authkey = request.form['authkey']
			db.write('''UPDATE users SET b3id = (?), guid = (?) ,level = (?), authkey = (?) WHERE authkey = (?)''',b3id,guid,level,None,authkey)
			db.close()
		return render_template("home.html")
	except Exception as e:
		return render_template("home.html")