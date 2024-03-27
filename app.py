import re
from flask import Flask, render_template, request, redirect, url_for,session,current_app
import config
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key="himanipriyaomdhrudiya"

app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_HOST
app.config['MYSQL_DATABASE_USER'] = config.MYSQL_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DB
app.config["MYSQL_DATABASE_PORT"] = 3306

mysql_app = MySQL(app)


#  con=mysql_app.connect()
#     cur=con.cursor()
#     cur.execute("select * from neev_members")
#     data=cur.fetchall()


@app.context_processor
def inject_global():
    return {'session_set': 0}


@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.route('/home')
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('member_type', None)
    session.pop('email', None)
    session.pop('password', None)

    return redirect(url_for('login'))

@app.route('/login_auth',methods=['POST'])
def login_auth():
    if request.method == 'POST':
        con=mysql_app.connect()
        cur=con.cursor()
        cur.execute("select * from admin where Email=%s and Password=%s",(request.form['email'],request.form['password']))
        data_admin=cur.fetchall()
        
        cur.execute("select * from neev_members where Email=%s and Password=%s",(request.form['email'],request.form['password']))
        data_member=cur.fetchall()

        cur.close()
        con.close()

        if len(data_member) == 0 and len(data_admin) == 0:
            return render_template('login.html',error=1)
        elif len(data_admin) == 1:
            session['member_type']='admin'
        else:
            session['member_type']='member'
            
        # current_app.jinja_env.globals['session_set'] = 1

        session['email']=request.form['email']
        session['password']=request.form['password']
        return render_template('dashboard.html',session=session)  #1=> member and 2=>admin
    else:
        return redirect(url_for('/'))


@app.route('/profile')
def display_profile():
    con=mysql_app.connect()
    cur=con.cursor()
    if  session['member_type'] == 'admin':
        cur.execute("select * from admin where Email=%s and Password=%s",(session['email'],session['password']))
    else:
        cur.execute("select * from neev_members where Email=%s and Password=%s",(session['email'],session['password']))
    data=cur.fetchone()
    cur.close()
    con.close()

    return render_template('profile.html',data=data,type=session['member_type'])

@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':    
        name = request.form['name']
        email = request.form['email']
        app.logger.info('Received POST request to add student: Name - %s, Email - %s', name, email)
     
        con = mysql_app.connect()
        cur=con.cursor()

        try:
            cur.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
            con.commit()
            app.logger.info('Student added successfully: Name - %s, Email - %s', name, email)
        except Exception as e:
            app.logger.error('Error adding student to database: %s', str(e))
        finally:
            con.connect()
            cur.close()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)