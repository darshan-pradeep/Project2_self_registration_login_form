from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector as conn
import os
mydb=conn.connect(host='localhost',user='root',passwd='kartikeya',database='user_details')
cursor=mydb.cursor()

app=Flask(__name__)

app.secret_key=os.urandom(24)

@app.route('/')
def registration():
    return render_template('registration.html')

@app.route('/thankyoupage',methods=['POST'])
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
    if 'user_id' in session:
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
        return redirect(url_for('dashboard',name=name[0][0]))
    else:
        return redirect('/')

@app.route('/dashboard/<string:name>')
def dashboard(name):
    if 'user_id' in session:
        fit_data=cursor.execute('SELECT ActivityDate,TotalSteps,TotalDistance,TrackerDistance from fit.fitbit_data')
        results=cursor.fetchall()
        print(results[0][0],results[0][1],results[0][2],results[0][3])
        return render_template('dashboard.html',name=name,results=results)
    
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('registration'))

if __name__=='__main__':
    app.run(debug=True)
    

    