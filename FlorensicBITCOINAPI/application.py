from flask import Flask, request
import os
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import getpass



app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\emaildatabase.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

class user(db.Model):
    userid = db.Column(db.Integer,primary_key=True)
    usersecret = db.Column(db.String(32), nullable = False) 
    username = db.Column(db.String(32), nullable = False)
    useremail = db.Column(db.String(80), nullable = False)

    def __repr__(self):
        return f"{self.userid} - {self.usersecret} - {self.username} - {self.useremail}"
class alert(db.Model):
    a_id = db.Column(db.Integer,primary_key=True)
    u_id = db.Column(db.Integer, nullable = False) 
    a_target = db.Column(db.Integer, nullable = False)
    a_status = db.Column(db.String(80), nullable = False)

    def __repr__(self):
        return f"{self.a_id} - {self.u_id} - {self.a_target} - {self.a_status}"        

@app.route('/')
def indef():
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false')
    for coins in response.json():
        if(coins["symbol"]=="btc"):
            return str(coins["current_price"])

@app.route('/alerts/create', methods=['POST'])
def add_alert():
    a = alert(u_id=request.json["u_id"],a_target=request.json["a_target"],a_status="created")
    db.session.add(a)
    db.session.commit()
    return {"aid":a.a_id}

@app.route('/alerts/delete', methods=['PUT'])
def remove_alert():
    r_aid=request.json["a_id"]
    row = alert.query.filter_by(aid=r_aid).first()
    row.astatus = "deleted"
    db.session.commit()
    return "Deleted Successfully"

@app.route('/alerts',methods=['GET'])
def view_alerts():
    qf=request.json["queryfilter"]
    if qf=='null':
        alerts = alert.query.filter_by(uid=request.json["u_id"]).all()
    else:
        alerts = alert.query.filter_by(uid=request.json["u_id"]).filter_by(astatus=qf).all()
    response=[]
    for a in alerts:
        response.append({'a_id':a.a_id, 'u_id':a.u_id, 'a_target':a.a_target, 'a_status':a.a_status})
    return {'Alerts':response}

def send_email(send_email_to,your_name):
    msg = MIMEMultipart()
    password = your_password
    msg['From'] = your_email
    msg['To']=send_email_to
    msg['Subject'] = "BTC Price has crossed the limit you fixed. Check It Out."

    message = "Dear customer" + your_name + "\nBitcoin price has crossed: " + str(bitcoin_rate) + ". Want To Sell \nHave A great Day\ncopyrights crypto alert API"
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'],msg['To'], message)
    server.quit()

    print("Alert has successfully been triggered, changing status now.")

your_name="florensicBITCOIN API"
your_email="sandhyabhuvana1@gmail.com"
your_password="florensic.api"
#can use getpass for security i guess, hardcoding here for now

send_email_to="sandhya.s2019@vitstudent.ac.in"
alert_amount="23400"
bitcoin_rate=24504
while True:
    url= "https://api.coindesk.com/v1/bpi/currentprice.json"
    response1 = requests.get(
        url,headers={"Accept":"application/json"},)
    data = response1.json()    
    bpi=data['bpi']
    USD=bpi['USD']
    bitcoin_rate=int(USD['rate_float'])
    targetList = alert.query.filter(alert.a_target <= bitcoin_rate).filter(alert.a_status=="created").all()
    for targetRow in targetList:
        userRow = user.query.filter_by(userid=targetRow.u_id).first()
        send_email_to=userRow.useremail
        your_name=userRow.username
        send_email()
        targetRow.a_status = "triggered"
        db.session.commit()
        print("Ctrl + C to quit, come back later.")        
    
    print('Price is ' + str(bitcoin_rate) + '. Check again later. Ctrl + C to exit.')
    time.sleep(300)
    