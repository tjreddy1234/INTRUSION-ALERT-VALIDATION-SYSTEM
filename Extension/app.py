import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,9999)
    print(otp)
    msg = EmailMessage()
    msg.set_content(f"Dear {name},\n\n"
                "Thank you for signing up for Intrusion Alert Validation System! "
                "To complete your registration and secure your account, please verify your email using the OTP below:\n\n"
                f"OTP: {otp}\n\n"
                "If you didn’t sign up for an account, you can ignore this email. "
                "The link will expire in 1 hours for security reasons.\n\n"
                "If you have any questions, feel free to reach out to our support team.\n\n"
                "Best regards,\n"
                "Intrusion Alert Validation System Team")
    msg['Subject'] = 'Confirm Your Email for INAVS'
    msg['From'] = "myprojectstp@gmail.com"
    msg['To'] = email
    
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("myprojectstp@gmail.com", "paxgxdrhifmqcrzn")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")

@app.route('/predict1', methods=['POST'])
def predict1():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")

@app.route("/notebook")
def notebook1():
    return render_template("Notebook.html")



@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model.sav')
    predict = model.predict(final4)

    if predict==1:
        output='This Packet Shows Suspicious Behavious!'
   
    elif predict == 0:
        output = 'It is False Alert!'
    
    
    

    return render_template('prediction.html', output=output)


if __name__ == "__main__":
    app.run(debug=True)
