from flask import Blueprint, render_template, redirect, request, session, flash, jsonify
from functools import wraps
from database.database import remoteDB, database
from flask_mail import Message
import urllib.request, json 
from requests_toolbelt import MultipartEncoder
import requests
import json as js
from helper import getstatus
import re
import traceback
import os

_reColor = re.compile(r'\^[0-9a-z]')

app_cod4 = Blueprint('app_cod4',__name__)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'level' in session and session['level'] >= 32:
            return f(*args, **kwargs)
        else:
            flash("You need be admin or Higher")
            return redirect(request.referrer)
    return wrap

def mod_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'level' in session and session['level'] >= 16:
            return f(*args, **kwargs)
        else:
            flash("You need be Moderator or Higher")
            return redirect(request.referrer)
    return wrap


    
@app_cod4.route('/ss/banned/')
def banned():
    try:
        db = database()
        data = db.read('''SELECT * FROM ScreenShots WHERE Banned IS NOT NULL ORDER BY ID DESC''')
        db.close()
        return render_template("cod4/banlist.html", data = data,fullwidth=True)
    except:
        flash('Something Went Wrong')
        return render_template("cod4/banlist.html")    
    
    
@app_cod4.route('/ss/')
def ssview():
    try:
        db = database()
        data = db.read('''SELECT ID,Name,B3ID,GUID,Score FROM ScreenShots WHERE Banned IS NULL ORDER BY ID DESC''')
        db.close()
        return render_template("cod4/ssviewer.html", data = data)
    except:
        flash('Something Went Wrong')
        return render_template("cod4/ssviewer.html")        

@app_cod4.route('/ss/view/')
@app_cod4.route('/ss/viewss/')
def imageview():
    try:
        db = database()
        data = db.read('''SELECT * FROM ScreenShots WHERE ID = (?)''', request.args.get('ssid'))
        db.close()
        metadata = ['screenshots/{}'.format(data[0][0]),'Screenshot of {} (@{})'.format(data[0][1],data[0][2]),'ss/view/?ssid={}'.format(data[0][0])]
        return render_template("cod4/imageview.html", data = data,metadata=metadata )

    except:
        flash('Something Went Wrong :/')
        return redirect(request.referrer)

@app_cod4.route('/ss/take/')
def takess():
    try:
        id = str(int(request.args.get('id')))
        m = MultipartEncoder(
            fields={"b3id": str(-1), "cmd": 'getss', "args": '@'+id, "secretkey": 'WK3vKwJs4ZDCV5HrthRnOGreY12mEYwS2ljpm0AI'}
        )
        r = str(requests.post('http://188.166.187.32:5001/wufcw66i5aetl2w1f1zp24', data=m, headers={'Content-Type': m.content_type}).text)
        if 'true' in r:
            flash('ScreenShot Will be Uploaded Shortly')
            return redirect(request.referrer)
        else:
            flash('Something went wrong try again in bit')
            return redirect(request.referrer)
    except:
        flash('Something Went Wrong :/')
        return redirect(request.referrer)

        
@app_cod4.route('/ss/ban/')
@mod_required
def banplayer():
    try:
        db = database()
        id = str(db.read('''SELECT B3ID from ScreenShots where ID = (?)''',str(int(request.args.get('ssid'))))[0][0])
        
        m = MultipartEncoder(
            fields={"b3id": str(session['b3id']), "cmd": 'ban', "args": '@'+id,"args2": '^3WallHacker^0|^1Proof- blackassassins.tk/ss/view/?ssid='+str(int(request.args.get('ssid'))), "secretkey": 'WK3vKwJs4ZDCV5HrthRnOGreY12mEYwS2ljpm0AI'}
        )
        r = str(requests.post('http://188.166.187.32:5001/wufcw66i5aetl2w1f1zp24', data=m, headers={'Content-Type': m.content_type}).text)
        if 'true' in str(r):
            data = db.write('''UPDATE ScreenShots SET banned = (?) WHERE ID = (?)''',session['username'],str(int(request.args.get('ssid'))))
            flash('Player Was Successfully Banned')
        else:
            flash('There was a error while banning the player, Try Again in Bit !')
            flash('Make Sure You are Connected to Server Before Banning Again')
        db.close()
        return redirect(request.referrer)
    except:
        flash('Something Went Wrong')
        return redirect(request.referrer)
        
        
@app_cod4.route('/ss/submit/', methods=["POST"])
def submitss():
    try:
        if request.method == "POST" and request.form['secretkey'] == 'WK3vKwJs4ZDCV5HrthRnOGreY12mEYwS2ljpm0AI':
            db = database()
            try:
                id = int(db.read('''SELECT ID FROM ScreenShots''')[-1][0])+1
            except:
                id = 1
            name = request.form['name'][:-2]
            b3id = int(request.form['b3id'])
            connections = int(request.form['connections'])
            aliases = request.form['aliases']
            guid = request.form['guid']
            penalties = int(request.form['penalties'])
            ip = request.form['ip']
            score = request.form['score']
            try:
                with urllib.request.urlopen("https://ipinfo.io/{}/json".format(ip)) as url:
                    data = json.loads(url.read().decode())
                    address = '{}, {}'.format(data['city'],data['country'])
            except:
                address = 'Not Found'
            f = request.files['ss']
            f.save('static/screenshots/{}.jpg'.format(id))
            query = '''INSERT INTO ScreenShots (Name,B3ID,Connections,Aliases,GUID,Address,IP,Penalties,Score) VALUES ('{}',{},{},'{}','{}','{}','{}',{},{})'''.format(
                        name, b3id, connections, aliases, guid, address, ip, penalties, score)
            db.write(query)
            db.close()
            return jsonify('Got IT')
    except Exception as e:
        print(e, file=open('/home/ba_error.log', 'a'))
        return jsonify('Something Went Wrong')
        
@app_cod4.route('/request/kmusic/', methods=["POST","GET"])
def requestsongs():
    try:
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            songname = request.form['songname']
            artists = request.form['artists']
            starttime = int(request.form['starttime'])
            url = "https://www.youtube.com/embed/{}?start={}&end={}".format(request.form['videoid'],starttime,starttime+10)
            db = database()
            x = db.read("SELECT * FROM KMusic WHERE Name LIKE (?)",name)
            if len(x) > 0:
                flash('Song is Already in the Request List')
                return render_template("requestsongs.html")
            db.write('''INSERT INTO KMusic(Name,Email,Song,Artist,URL) VALUES(?,?,?,?,?)''',name,email,songname,artists,url)
            db.close()
            
            flash('Your Request is Send to Admins')

        return render_template("cod4/requestsongs.html")
    except:
        flash('There was Error while sending the request')
        return render_template("cod4/requestsongs.html")

@app_cod4.route('/admins/')
def adminlist():
    try:
        db = remoteDB()
        data = db.getadmins()
        db.close()
        return render_template("cod4/admins.html", data=data)
    except:
        flash('Something Went Wrong')
        return render_template("cod4/admins.html", data=[])
    
    
@app_cod4.route('/penalties/')
def penalties():
    try:
        db = remoteDB()
        data = db.penalties()
        db.close()
        fdata = []
        for d in data:
            reason = re.sub(_reColor, '', d[3]).strip()
            fdata.append([d[0],d[1],d[2],reason,d[4],d[5]])
        return render_template("cod4/penalties.html", data=fdata)
    except:
        flash('Something Went Wrong')
        return render_template("cod4/penalties.html", data=[])


@app_cod4.route('/appeal/ban/')
def reportadmin():
    try:
        db = database()
        emails = db.read('''SELECT Email from users where Level >= 64''')
        emaillist = []
        for email in emails:
            emaillist.append(email[0])
        
        data = request.args.get('data')
        adminid = request.args.get('adminid')
        reason = str(request.args.get('reason'))
        
        if len(data) != int(adminid)+20:
            flash('Something Went Wrong :(')
            return redirect(request.referrer)
        
        data = data.split(';;;')
        try:
            msg = Message("{} Made a Ban appeal".format(data[2]),
                        sender="legionsesport@gmail.com",
                        recipients=emaillist)
            msg.body = '''Ban appeal by {}\n
                        {} Think Following Penalty is unfair becouse {} \n
                        Penalty ID :- {} \nPenalty Type :- {} \nPlayer Name :- {} \n
                        Reason for Penalty :- {} \n
                        Admin Name :- {} \n
                        Expire Time :- {}'''.format(data[2],data[2],reason,data[0],data[1],data[2],data[3],data[4],data[5])
            msg.html = render_template('/emails/report_admin.html', data=data, reason=reason)
            mail.send(msg)
            flash('Your Appeal was successfully send to Responsible Persons')
        except:
            flash('There was errro while making the Appeal, Try Again later :(')
        return redirect(request.referrer)
    except:
        flash(str(e))
        flash('There was errro while making the Appeal, Try Again later :(')
        return redirect(request.referrer)


@app_cod4.route('/server/promod/')
def promod():
    try:
        items,clients,time,hostname = getstatus()
        return render_template("cod4/players.html", items=items ,clients = clients, time=time, hostname=hostname)
    except:
        flash("It's look like B3 is not working")
        return render_template("cod4/players.html", items={} ,clients = [], time='', hostname='')
