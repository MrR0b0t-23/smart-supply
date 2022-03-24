# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 22:19:32 2022

@author: Ashwin
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import Flask, render_template, request,  redirect, url_for, make_response
import datetime
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://uvkukyhdltxaky:c58d5eb2b0196d5d6ea63bf95da9b9800ad656a9f2610ff36f98772318b2bcc8@ec2-44-194-92-192.compute-1.amazonaws.com:5432/ddg2soij34vd15"
db = SQLAlchemy(app)
     
class userData(db.Model):
    __tablename__ = 'User Database'

    UserId = db.Column(db.Integer, primary_key=True)
    EmailId = db.Column(db.String(80), nullable=False)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

    def __init__ (self, EmailId, Username, Password):
        self.Username= Username
        self.EmailId = EmailId
        self.Password = Password   
        
class apiData(db.Model):
    __tablename__ = 'API Database'
    
    DeviceId = db.Column(db.String(10), primary_key = True, nullable = False)
    ApiCode = db.Column(db.String(10), nullable = False)
    
    def __init__ (self, ApiCode):
        self.ApiCode = ApiCode
   
class supplyData(db.Model):
    __tablename__ = 'Supply Chain Database'

    Id = db.Column(db.Integer, primary_key = True)
    DateTime = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())
    DeviceId = db.Column(db.String(10), nullable = False)
    ShipmentId = db.Column(db.String(10), nullable = False)
    FromLocation = db.Column(db.String(10), nullable = False)
    ToLocation = db.Column(db.String(10), nullable = False)
    SupplierId = db.Column(db.String(10), nullable = False)
    ShipmentWeight = db.Column(db.Integer, nullable = False)
    
    def __init__ (self, DeviceId, ShipmentId, FromLocation, ToLocation, SupplierId, ShipmentWeight):
        self.DeviceId = DeviceId
        self.ShipmentId = ShipmentId
        self.FromLocation = FromLocation
        self.ToLocation = ToLocation
        self.SupplierId = SupplierId
        self.ShipmentWeight = ShipmentWeight
        
def __authLogin__(emailId_, password_):
   emailId_ = str(emailId_)
   password_ = str(password_)
   token = userData.query.filter(userData.EmailId.like(emailId_)).filter(userData.Password.like(password_)).first()
   if token:
      return True
   return False

def __geoSpatialPlot__():
    pass

def __linePlot__():
    pass

def __histPlot__():
    pass

def __countPara__():
    pass

@app.route('/', methods = ['POST', 'GET'])
def signin_page():
    if request.method == 'POST':
       emailId_ = request.form.get("email")
       password_ = request.form.get("password")
       print(emailId_, password_)
       resp = make_response(redirect(url_for('dashboard_page')))
       
       if __authLogin__(emailId_, password_):
          resp.set_cookie('Authentication', 'True')
          return resp 
      
       resp.set_cookie('Authentication', 'False') 
       return render_template('signin.html')

    return render_template('signin.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup_page():
    if request.method == 'POST':
       username_ = request.form.get("username")
       emailId_ = request.form.get("emailId")
       password_ = request.form.get("password")

       print(username_, emailId_, password_)
       if emailId_:
            newUser = userData(Username = username_, EmailId = emailId_,
                                        Password = password_)
            db.session.add(newUser)
            db.session.commit()
            return render_template('signin.html')
    return render_template('signup.html')

@app.route('/table')
def table_page():
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":
        supplyResult = supplyData.query.all()
        return render_template('table.html', tableData = supplyResult)
    else:
        return redirect(url_for('signin_page'))

@app.route('/dashboard')
def dashboard_page():
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":
        supplyResult = supplyData.query.all()
        shipment = supplyData.query.count()
        tot_weight = supplyData.query.with_entities(func.sum(supplyData.ShipmentWeight)).first()[0]
        frequent_from = db.select([db.func.max(supplyData.FromLocation)]).group_by(supplyData.FromLocation)
        frequent_from = db.session.execute(frequent_from).first()[0]
        frequent_to = db.select([db.func.max(supplyData.ToLocation)]).group_by(supplyData.ToLocation)
        frequent_to = db.session.execute(frequent_to).first()[0]
        #print(tot_shipment, tot_weight, frequent_from, frequent_to)
        statData = {'tot_shipment':tot_shipment, "tot_weight": tot_weight, "frequent_from": frequent_from, "frequent_to": frequent_to}
        return render_template('dashboard.html', tableData = supplyResult, Data = statData)
 
    else:
        return redirect(url_for('signin_page'))

@app.route('/variables', methods = ['POST', 'GET'])
def variable_page():
    ApiCode_ = request.args.get('Api', default = '000000', type = str)
    DeviceId_ = request.args.get('DeviceId', default = '000000', type = str)
    ShipmentId_ = request.args.get('ShipmentId', default = '000000', type = str)
    FromLocation_ = request.args.get('FromLocation', default = '000000', type = str)
    ToLocation_ = request.args.get('ToLocation', default = '000000', type = str)
    SupplierId_ = request.args.get('SupplierId', default = '000000', type = str)
    ShipmentWeight_ = request.args.get('ShipmentWeight', default = '000000', type = str)
     
    ApiCode_ = str(ApiCode_)
    DeviceId_ = str(DeviceId_)
    ShipmentId_ = str(ShipmentId_)
    FromLocation_ = str(FromLocation_)
    ToLocation_ = str(ToLocation_)
    SupplierId_ = str(SupplierId_)
    ShipmentWeight_  = int(ShipmentWeight_)

    apiResult = apiData.query.filter(apiData.ApiCode.like(ApiCode_)).first()
    if apiResult:
        print("API AUTHENTICATION SUCCESSFULL, TIME: ", datetime.datetime.now())
        resp = make_response(redirect(url_for('dashboard_page')), 201)
        supplyResult = supplyData(DeviceId = DeviceId_, ShipmentId = ShipmentId_,
                                  FromLocation = FromLocation_, ToLocation = ToLocation_,
                                  SupplierId = SupplierId_, ShipmentWeight = ShipmentWeight_)
        db.session.add(supplyResult)
        db.session.commit()
        return resp

@app.route('/logout')
def logout_page(): 
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":  
        resp = make_response(redirect(url_for('login_page')))
        resp.set_cookie('Authentication', 'False')
        return resp
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
