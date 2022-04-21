# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 22:19:32 2022

@author: Ashwin
"""
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request,  redirect, url_for, make_response
import datetime
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)

class superUserData(db.Model):
    __tablename__ = 'SuperUser Database'

    UserId = db.Column(db.Integer, primary_key=True)
    EmailId = db.Column(db.String(80), nullable=False)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

    def __init__ (self, EmailId, Username, Password):
        self.Username= Username
        self.EmailId = EmailId
        self.Password = Password   

class customerUserData(db.Model):
    __tablename__ = 'CustomerUser Database'

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
   
class ProductData(db.Model):
    __tablename__ = 'Product Database'

    Id = db.Column(db.Integer, primary_key = True)
    DateTime = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())
    DeviceId = db.Column(db.String(10), nullable = False)
    ProductId = db.Column(db.String(10), nullable = False)
    FromLocation = db.Column(db.String(10), nullable = False)
    Quantity = db.Column(db.String(10), nullable = False)
    SupplierId = db.Column(db.String(10), nullable = False)
    ExpireDate = db.Column(db.String(10), nullable = False)
    ManufactureDate = db.Column(db.String(10), nullable = False)
    ProductWeight = db.Column(db.Integer, nullable = False)
    
    def __init__ (self, DateTime, DeviceId, ProductId, FromLocation, Quantity, SupplierId, ExpireDate, ManufactureDate, ProductWeight):
        self.DateTime = DateTime
        self.DeviceId = DeviceId
        self.ProductId = ProductId
        self.FromLocation = FromLocation
        self.Quantity = Quantity
        self.SupplierId = SupplierId
        self.ExpireDate = ExpireDate
        self.ManufactureDate = ManufactureDate
        self.ProductWeight = ProductWeight

class ProductLocationData(db.Model):
    __tablename__ = 'ProductLocation Database'

    Id = db.Column(db.Integer, primary_key = True)
    DateTime = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())
    DeviceId = db.Column(db.String(10), nullable = False)
    ProductId = db.Column(db.String(10), nullable = False)
    Location = db.Column(db.String(10), nullable = False)
    
    def __init__ (self, DateTime, DeviceId, ProductId, Location):
        self.DateTime = DateTime
        self.DeviceId = DeviceId
        self.ProductId = ProductId
        self.Location = Location

def __SuperUserauthLogin__(emailId_, password_):
   emailId_ = str(emailId_)
   password_ = str(password_)
   token = superUserData.query.filter(superUserData.EmailId.like(emailId_)).filter(superUserData.Password.like(password_)).first()
   if token:
      return True
   return False

def __CustomerUserauthLogin__(emailId_, password_):
   emailId_ = str(emailId_)
   password_ = str(password_)
   token = customerUserData.query.filter(customerUserData.EmailId.like(emailId_)).filter(customerUserData.Password.like(password_)).first()
   if token:
      return True
   return False

def __ProductId_Plot__():
    productResult = ProductData.query.all()
    productId = []
    for product in productResult:
        productId.append(product.ProductId)
    productId = pd.Series(productId).value_counts()
    palette_color = sb.color_palette('muted')
    plt.pie(productId, labels=productId.index, colors=palette_color, autopct='%.0f%%')
    plt.savefig('static/img/ProductId_image.png')
    plt.close()

def __DateQty_Plot__():
    productResult = ProductData.query.all()
    dates = []
    product_qty = []
    for product in productResult:
        dates.append(product.DateTime)
        product_qty.append(int(product.Quantity))
    plt.plot(dates,product_qty, color= 'dodgerblue')
    plt.xticks(rotation = 30)
    plt.savefig('static/img/DateQty_image.png')
    plt.close()

def __Hist_Plot__():
    productResult = ProductData.query.all()
    histo = []
    for product in productResult:
        histo.append(int(product.Quantity))
    plt.hist(histo, color= 'dodgerblue')
    plt.xticks(rotation = 30)
    plt.savefig('static/img/Histogram_image.png')
    plt.close()  

def __ExpireDate_plot__():
    productResult = ProductData.query.all()
    expire = []
    for product in productResult:
        expire.append(product.ExpireDate)
    expire = pd.Series(expire).value_counts()
    palette_color = sb.color_palette('muted')
    plt.pie(expire, labels=expire.index, colors=palette_color, autopct='%.0f%%')
    plt.savefig('static/img/ExpireDate_image.png')
    plt.close()

@app.route('/', methods = ['POST', 'GET'])
def signin_page():
    if request.method == 'POST':
       emailId_ = request.form.get("email")
       password_ = request.form.get("password")
       print(emailId_, password_)
       resp = make_response(redirect(url_for('dashboard_page')))
       
       if __SuperUserauthLogin__(emailId_, password_):
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
            newUser = superUserData(Username = username_, EmailId = emailId_, Password = password_)
            db.session.add(newUser)
            db.session.commit()
            return render_template('signin.html')
    return render_template('signup.html')

@app.route('/customersignin', methods = ['POST', 'GET'])
def customersignin_page():
    if request.method == 'POST':
       emailId_ = request.form.get("email")
       password_ = request.form.get("password")
       productId_ = request.form.get("ProductId")
       productId_ = int(productId_) 

       productResult = ProductData.query.filter(ProductData.ProductId.like(productId_)).first()
       productLocationResult = ProductLocationData.query.filter(ProductLocationData.ProductId.like(productId_)).first()
       print(productResult)
       data = {'ProductId': productLocationResult.ProductId, 'FromLocation': productResult.FromLocation, 'Quantity': productResult.Quantity,
                'SupplierId': productResult.SupplierId, 'ExpireDate': productResult.ExpireDate, 'ManufactureDate': productResult.ManufactureDate,
                'ProductWeight' : productResult.ProductWeight, 'Location': productLocationResult.Location}
       resp = make_response(render_template('table.html', data= data))
       
       if __SuperUserauthLogin__(emailId_, password_):
          resp.set_cookie('Authentication', 'True')
          return resp
      
       resp.set_cookie('Authentication', 'False') 
       return render_template('customer-signin.html')

    return render_template('customer-signin.html')
  
@app.route('/dashboard')
def dashboard_page():
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":
        productResult = ProductData.query.all()
        tot_order = ProductData.query.count()
        tot_quantity = ProductData.query.with_entities(func.sum(ProductData.Quantity)).first()[0]
        
        freq_supplier = db.select([db.func.max(ProductData.SupplierId)]).group_by(ProductData.SupplierId)
        freq_supplier = db.session.execute(freq_supplier).first()[0]

        freq_product = db.select([db.func.max(ProductData.ProductId)]).group_by(ProductData.ProductId)
        freq_product = db.session.execute(freq_product).first()[0]

        #print(tot_order, tot_quantity, frequent_from, freq_product)
        __DateQty_Plot__()
        __ProductId_Plot__()
        __Hist_Plot__()
        __ExpireDate_plot__()
        statData = {'tot_order':tot_order, "tot_quantity": tot_quantity, "freq_supplier": freq_supplier, "freq_product": freq_product}
        return render_template('dashboard.html', tableData = productResult, Data = statData)
    else:
        return redirect(url_for('signin_page'))

#https://smartsup.herokuapp.com/variable?Api=&DeviceId=&ShipmentId=&FromLocation=&,ToLocation=&SupplierId=

@app.route('/variables')
def variable_page():
    ApiCode_ = request.args.get('Api', default = '000000', type = str)
    DeviceId_ = request.args.get('DeviceId', default = '000000', type = str)
    ProductId_ = request.args.get('ProductId', default = '000000', type = str)
    FromLocation_ = request.args.get('FromLocation', default = '000000', type = str)
    Quantity_ = request.args.get('Quantity', default = '000000', type = str)
    SupplierId_ = request.args.get('SupplierId', default = '000000', type = str)
    ExpireDate_ = request.args.get('ExpireDate', default = '000000', type = str)
    ManufactureDate_ = request.args.get('ManufactureDate', default = '000000', type = str)
    ProductWeight_ = request.args.get('ProductWeight', default = '000000', type = str)

    ApiCode_ = str(ApiCode_)
    DeviceId_= str(DeviceId_)
    ProductId_ = str(ProductId_)
    FromLocation_ = str(FromLocation_)
    Quantity_ = str(Quantity_)
    SupplierId_ = str(SupplierId_)
    ExpireDate_ =str(ExpireDate_)
    ManufactureDate_ = str(ManufactureDate_)
    ProductWeight_ = str(ProductWeight_)

    apiResult = apiData.query.filter(apiData.ApiCode.like(ApiCode_)).first()
    if apiResult:
        ProductResult = ProductData(DeviceId = DeviceId_, ProductId = ProductId_,
                                  FromLocation = FromLocation_, Quantity = Quantity_,
                                  SupplierId = SupplierId_, ExpireDate = ExpireDate_,
                                  ManufactureDate = ManufactureDate_, ProductWeight = ProductWeight_)
        db.session.add(ProductResult)
        db.session.commit()
        return None

@app.route('/logout')
def logout_page(): 
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":  
        resp = make_response(redirect(url_for('login_page')))
        resp.set_cookie('Authentication', 'False')
        return resp
    return redirect(url_for('login_page'))

@app.errorhandler(404) 
def not_found(e):
  return render_template("404.html")

if __name__ == "__main__":
    if not os.path.exists("db.sqlite3"):
        db.create_all()
    app.run()
       