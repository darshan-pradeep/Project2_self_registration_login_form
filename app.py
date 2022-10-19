from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector as conn
import os
mydb=conn.connect(host='localhost',user='root',passwd='kartikeya',database='user_details')
cursor=mydb.cursor()

app=Flask(__name__)

app.secret_key=os.urandom(24) # creating a key which stays as a cookie inside the logged in person's browser,
# for some time so that once logged in, he can access the dashboard even from the homepage. When the app starts
# running, this key will get connected with the session method of flask.

@app.route('/') #this is the homepage endpoint
def registration():
    return render_template('registration.html') #whenever, hompepage  endpoint is hit, show registration.html

@app.route('/thankyoupage',methods=['POST']) # once user provides the details for registration, say thank you and
# details inside the db and show thankyoupage.html
def thankyoupage():
    name=request.form.get('name')
    emailid=request.form.get('emailid')
    password=request.form.get('password')
    insert_query=f"INSERT INTO registration_details values(Sno,'{name}','{emailid}','{password}')"
    cursor.execute(insert_query)
    mydb.commit()
    return render_template('/thankyoupage.html',name=name,emailid=emailid,password=password)


@app.route('/login')
def login():
    if 'user_id' in session: #if the user has already logged in, it'll take directly to the dashboard
        select_name_query=f"SELECT Name FROM registration_details WHERE Sno='{session['user_id']}'"
        cursor.execute(select_name_query)
        name=cursor.fetchall()
        return redirect(url_for('dashboard',name=name[0][0]))
    else:
        return render_template('login.html')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    emailid=request.form.get('emailid')
    password=request.form.get('password')
    select_query=f"SELECT * FROM registration_details WHERE `email_id`='{emailid}' AND `password`='{password}'"
    cursor.execute(select_query)
    result=cursor.fetchall()
    print(result)
    select_name_query=f"SELECT Name FROM registration_details WHERE email_id='{emailid}'"
    cursor.execute(select_name_query)
    name=cursor.fetchall()
    if len(result)>0:
        session['user_id']=result[0][0]
        #if the login details are present inside the db, create a session dictionary with a key element which is the
        # primary key  in our database. Thhis is done so as to access individual entries uniquely
        return redirect(url_for('dashboard',name=name[0][0])) #if user has already logged in, show him the dashboard
    else:
        return redirect('/') #else, take him to registration page so that he can register

@app.route('/dashboard/<string:name>') #whenever we redirect from one function to another and if we are passing any
# parmeter, ensure that the 2nd function has something to cathc the incoming parameter. That's why we have created an
# endpoint in this way.  So for every user, the endpoint will be with their name.ex- -> /dashboard/darshan
def dashboard(name):
    if 'user_id' in session: #this is useful when we try to access dashboard directly from the homepage. So we are
        # checcking whether the user has already logged in or not. If logged in, show the dashboard directly. else,
        # make him register first
        fit_data=cursor.execute('SELECT ActivityDate,TotalSteps,TotalDistance,TrackerDistance from fit.fitbit_data')
        results=cursor.fetchall()
        print(results[0][0],results[0][1],results[0][2],results[0][3])
        return render_template('dashboard.html',name=name,results=results)
    else:
        return redirect(url_for('registration'))
    
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('registration'))

if __name__=='__main__':
    app.run(debug=True)
    

    