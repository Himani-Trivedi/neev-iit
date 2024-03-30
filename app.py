
import re
from flask import Flask, render_template, request, redirect, url_for,session
import config
from flaskext.mysql import MySQL
from datetime import date

app = Flask(__name__)
app.secret_key="himanipriyaomdhrudiya"

app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_HOST
app.config['MYSQL_DATABASE_USER'] = config.MYSQL_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DB
app.config["MYSQL_DATABASE_PORT"] = 3306

mysql_app = MySQL(app)
session_Set=0

def isSessionSet():
    if session.get('set') == 1:
        return True
    else:
        return False

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.route('/home')
@app.route('/')
def home():
    if isSessionSet():
        return redirect(url_for('dashboard'))
    else:
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
    session.pop('set',0)

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

        global session_Set 
        session_Set=1
        session['set']=1
        session['email']=request.form['email']
        session['password']=request.form['password']
        return render_template('dashboard.html',session=session)  #1=> member and 2=>admin
    else:
        return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if isSessionSet():
        return render_template('dashboard.html',session=session)
    else :
        return redirect(url_for('home'))


@app.route('/profile')
def display_profile():
    if isSessionSet():
        con=mysql_app.connect()
        cur=con.cursor()
        if  session['member_type'] == 'admin':
            cur.execute("select * from admin where Email=%s and Password=%s",(session['email'],session['password']))
        else:
            cur.execute("select * from neev_members where Email=%s and Password=%s",(session['email'],session['password']))
        data=cur.fetchone()
        cur.close()
        con.close()
    else :
        return redirect(url_for('home'))

    return render_template('profile.html',data=data,type=session['member_type'])

@app.route('/courses')
def courses():
    if isSessionSet():   
        con=mysql_app.connect()
        cur=con.cursor()
        cur.execute("select * from course")
        data=cur.fetchall()

        cur.close()
        con.close()
        return render_template('courses.html',data=data)
    else:
        return redirect(url_for('home'))

# tuple(item for subtuple in active_courses for item in subtuple)

@app.route('/activate_course/<id>')
def activate_course(id):
    if isSessionSet(): 
        con=mysql_app.connect()
        cur=con.cursor()
        cur.execute("select * from course where C_ID=%s",id)
        data=cur.fetchall()

        cur.execute("select * from instructors")
        instructors=cur.fetchall()

        cur.close()
        con.close()
        current_date = date.today().isoformat()

        return render_template('activate_course.html',data=data[0],ins=instructors,date=current_date)
    else:
        return redirect(url_for('home'))


@app.route('/activate_course/done_activate',methods=['POST'])
def done_activate():
    if request.method == 'POST':
        con=mysql_app.connect()
        cur=con.cursor()

        cur.execute("INSERT INTO active_courses (I_ID, C_ID, start_date, end_date) VALUES (%s,%s,%s,%s)",(request.form['instructor'],request.form['courseId'],request.form['startDate'],request.form['endDate'],))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses'))
    else:
        return redirect(url_for('home'))


@app.route('/course_details/<id>')
def course_details(id):
    if isSessionSet(): 
        con=mysql_app.connect()
        cur=con.cursor()
        cur.execute("select * from course where C_ID=%s",(id))
        course_data=cur.fetchall()

        cur.execute("select name from active_courses natural join instructors where C_ID=%s",(id))
        inst=cur.fetchall()  
        inst=tuple(item for subtuple in inst for item in subtuple)

        cur.execute("select * from active_courses where C_ID=%s",(id))
        active_part=cur.fetchall()  

        stu=[]
        stu_len=[]
        vol=[]
        vol_len=[]
        all_stu=[]
        all_vol=[]
        for i in active_part:
            cur.execute("select s_id,name,email  from students where s_id in (select s_id from active_courses NATURAL join student_course where active_id=%s)",(i[4]))
            rel=cur.fetchall()
            stu.append(rel)
            stu_len.append(len(rel))

            cur.execute("select v_id,name  from volunteer where v_id in ( select v_id  from active_courses NATURAL join volunteer_course where active_id=%s)",(i[4]))
            rel_vol=cur.fetchall()
            vol.append(rel_vol)
            vol_len.append(len(rel_vol))

            cur.execute("select S_ID,name from students where S_ID NOT IN (select S_ID from active_courses NATURAL join student_course where active_id=%s)",(i[4]))
            all_stu.append(cur.fetchall())

            cur.execute("select v_id,name,email from volunteer where v_id not in ( select v_id  from active_courses NATURAL join volunteer_course where active_id=%s)",(i[4]))
            all_vol.append(cur.fetchall())

        cur.close()
        con.close()

        return render_template('course_details.html',course=course_data, instructors=inst, stud_not_in_course=all_stu,
        vol_not_in_course=all_vol, active_course=active_part,students=stu,stu_count=stu_len,volunteers=vol,vol_count=vol_len)
    else:
        return redirect(url_for('home'))


@app.route('/en_stu',methods=['POST'])
def en_stu():
    if request.method == 'POST':
        con=mysql_app.connect()
        cur=con.cursor()

        cur.execute("INSERT INTO student_course(S_ID, C_id) VALUES (%s,%s)",
        (request.form['student_enr'],request.form['course_id_hidden']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses_details'))
    else:
        return redirect(url_for('home'))

@app.route('/en_vol',methods=['POST'])
def en_vol():
    if request.method == 'POST':
        con=mysql_app.connect()
        cur=con.cursor()

        cur.execute("INSERT INTO volunteer_course (V_ID, C_ID) VALUES (%s,%s)",
        (request.form['vol_en'],request.form['course_id_hidden']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses_details'))
    else:
        return redirect(url_for('home'))


@app.route('/courses_details')
def courses_details():
    return render_template('demo.html')


#for adding new course

@app.route('/add_course')
def add_course():
    return render_template('add_course.html')

@app.route('/add_course_detail',methods=['POST','GET'])
def add_course_detail():
    if request.method == 'POST':
        con=mysql_app.connect()
        cur=con.cursor()

        cur.execute("insert into course (C_ID,Course_name,Details,Venue) values (%s,%s,%s,%s)",(request.form['id'],request.form['name'],request.form['Details'],request.form['Venue'],))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses'))
    else:
        return redirect(url_for('home'))


@app.route('/demo')
def demo():
    return render_template('demo.html')




#just for demo
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
        
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)