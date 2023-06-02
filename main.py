from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import csv
app = Flask(__name__)
import subprocess
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create SQLAlchemy instance
import calendar
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    DOB = db.Column(db.String(10))
    gender = db.Column(db.String(1))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __init__(self, id, firstname, lastname, dob, gender, username, password, email):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob
        self.gender = gender
        self.username = username
        self.password = password
        self.email = email

class Attendances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String)
    date = db.Column(db.String)
    subjectname = db.Column(db.String)
    classname = db.Column(db.String)
    name = db.Column(db.String)

# Create database tables
with app.app_context():

   db.create_all()
# db.create_all()

# Insert a new user
# new_user = User(id=287, firstname='Tharani', lastname='T', DOB='30-01-2003', gender='M', username='tharani', password='tharani@123', email='tharani3001@gmail.com')
# db.session.add(new_user)
# db.session.commit()

@app.route('/')
def hello_world():
    # return render_template("index.html")

    return render_template("Login.html")

@app.route('/login')
def login():
    return render_template("mainlogin.html")

@app.route('/t')
def t():
    from datetime import datetime
    users_query = User.query
    num_users = users_query.count()
    # print("Number of rows in User table:", num_users)
    now = datetime.now()
    date=now.date()
    attendances_query = Attendances.query
    attendance = Attendances.query.all()  # Fetch all the Attendance model objects from the database
    userss = User.query.all()
    
    p=[]
    for i in attendance:
        if i.classname not in p:p+=[i.classname]
        
    # Filter the query to get only today's attendances
    today_attendances_query = attendances_query.filter(Attendances.date == date)
    pp=[i.name.upper() for i in today_attendances_query]
    uu= [i.username.upper() for i in userss]
    c=0
    for i in uu:
        if i not in pp:
            c+=1


    # Use the distinct() method to get the unique subjects
    unique_subjects_query = today_attendances_query.distinct(Attendances.subjectname)
    t=[]
    for i in unique_subjects_query:
        t+=[i.subjectname]
    
    return render_template("index.html",total=num_users,sub = len(set(t)),cl=len(p),cou=c)


@app.route('/stu')
def stu():
    attendance_records = Attendances.query.all()
    
    # Render the template and pass the attendance_records data to it
    return render_template('students.html', attendance_records=attendance_records)
    # return render_template("students.html")

@app.route('/sub')
def student():
    
    return render_template("subatt.html",attendance="",q="")

@app.route('/abs')
def abs():
    from datetime import datetime
    users_query = User.query
    num_users = users_query.count()
    # print("Number of rows in User table:", num_users)
    now = datetime.now()
    date=now.date()
    attendances_query = Attendances.query
    attendance = Attendances.query.all()  # Fetch all the Attendance model objects from the database
    userss = User.query.all()
    
    p=[]
    for i in attendance:
        if i.classname not in p:p+=[i.classname]
        
    # Filter the query to get only today's attendances
    today_attendances_query = attendances_query.filter(Attendances.date == date)
    pp=[i.name.upper() for i in today_attendances_query]
    uu= [i.username.upper() for i in userss]
    c=0
    t=[]
    for i in uu:
        if i not in pp:
            t+=[i]
    return render_template("absdet.html",t=t)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    attendance = Attendances.query.all()  # Fetch all the Attendance model objects from the database
    print(attendance)
    search_input = request.form.get('search_input')
    # Access the form data using the name attribute of the input field
    # You can perform any processing or validation with the form data here
    # Return a response to the client or redirect to another page as needed
    return render_template("subatt.html",attendance=attendance,q=search_input)

@app.route('/view')
def view():
    attendance = Attendances.query.all()  # Fetch all the Attendance model objects from the database
    print(attendance)
    with open('Attendance.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header ro
        k=[]
        for row in reader:
            # print(row)
            k+=[row]

    return render_template('viewatt.html', attendance=k)
    # return render_template("view.html")



@app.route('/attendence')
def attendence():
    from datetime import datetime
    users_query = User.query
    num_users = users_query.count()
    # print("Number of rows in User table:", num_users)
    now = datetime.now()
    date=now.date()
    attendances_query = Attendances.query
    attendance = Attendances.query.all()  # Fetch all the Attendance model objects from the database
    userss = User.query.all()
    
    p=[]
    for i in attendance:
        if i.classname not in p:p+=[i.classname]
        
    # Filter the query to get only today's attendances
    today_attendances_query = attendances_query.filter(Attendances.date == date)
    pp=[i.name.upper() for i in today_attendances_query]
    uu= [i.username.upper() for i in userss]
    c=0
    for i in uu:
        if i not in pp:
            c+=1


    # Use the distinct() method to get the unique subjects
    unique_subjects_query = today_attendances_query.distinct(Attendances.subjectname)
    t=[]
    for i in unique_subjects_query:
        t+=[i.subjectname]
    
    return render_template("takeattendence.html",total=num_users,sub = len(set(t)),cl=len(p),cou=c)
    

@app.route('/calendar')
def display_calendar():
    # Get the current month and year
    import datetime
    now = datetime.datetime.now()
    current_month = now.strftime("%B %Y")

    # Generate the days of the current month using calendar module
    cal = calendar.Calendar()
    days = []
    for week in cal.monthdatescalendar(now.year, now.month):
        week_days = []
        for day in week:
            if day.month != now.month:
                week_days.append('')
            else:
                week_days.append(day.day)
        days.append(week_days)

    # Render the template with the current month and days
    return render_template('cal.html', current_month=current_month, days=days)




@app.route('/take',methods=["GET","POST"])
def take():
    subjectName=request.form.get("subjectName")
    className=request.form.get("className")
    print(subjectName,className)
    # Define the command to run in the CMD
    cmd_command = 'python attendanceproject.py {} {}'.format(subjectName,className)  # Replace with your desired command

    # Run the command and capture the output
    result = subprocess.run(cmd_command, shell=True, check=True, stdout=subprocess.PIPE, text=True)

    # Get the output of the command
    output = result.stdout

    # Display the output to the user
    print(f"Output: \n{output}")
    # subprocess.run("python attendanceProject.py "+subjectName+" "+className)
    with open('Attendance.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
       
    attendances = Attendances.query.all()

    # Print the retrieved data
    for attendance in attendances:
        print("ID: ", attendance.id)
        print("Time: ", attendance.time)
        print("Date: ", attendance.date)
        print("Subject Name: ", attendance.subjectname)
        print("Class Name: ", attendance.classname)
        print("==============================")
    return render_template("takeattendence.html")



@app.route('/staff',methods=["GET","POST"])
def staff():
    user_name=request.form.get("username")
    password=request.form.get("password")
    mode=request.form.get("mode")
    print(user_name,password,mode)
    if mode == "Student":
        return render_template("student.html")
    elif mode !="Student" and user_name=="admin" and password=="admin@123":
        from datetime import datetime
        users_query = User.query
        num_users = users_query.count()
        # print("Number of rows in User table:", num_users)
        now = datetime.now()
        date=now.date()
        attendances_query = Attendances.query
        attendance = Attendances.query.all()  # Fetch all the Attendance model objects from the database
        userss = User.query.all()
        
        p=[]
        for i in attendance:
            if i.classname not in p:p+=[i.classname]
            
        # Filter the query to get only today's attendances
        today_attendances_query = attendances_query.filter(Attendances.date == date)
        pp=[i.name.upper() for i in today_attendances_query]
        uu= [i.username.upper() for i in userss]
        c=0
        for i in uu:
            if i not in pp:
                c+=1


        # Use the distinct() method to get the unique subjects
        unique_subjects_query = today_attendances_query.distinct(Attendances.subjectname)
        t=[]
        for i in unique_subjects_query:
            t+=[i.subjectname]
        
        return render_template("index.html",total=num_users,sub = len(set(t)),cl=len(p),cou=c)
        # return render_template("staff.html")
    return render_template("staff.html")



@app.route('/panel')
def panel():
    users = User.query.all()
    t=[]
    for user in users:
        t+=[[user.firstname,user.id,user.email, user.gender, user.DOB, user.username, user.password]]
    return render_template("studentdetails.html",data=t)


@app.route("/admin",methods=["GET","POST"])
def admin():
    return render_template("Pass.html",msg="")


@app.route('/execute', methods=["GET",'POST'])
def execute():
    user_name=request.form.get("name")
    regNo=request.form.get("regNo")
    gender=request.form.get("gender")
    dob=request.form.get("dob")
    email=request.form.get("email")
    username=request.form.get("username")
    password=request.form.get("password")
    subprocess.run("python enroll.py "+user_name)
    # Create a new User instance
    new_user = User(id=regNo, firstname=user_name, lastname='NULL', dob=dob, gender=gender,
                    username=username, password=password, email=email)

    # Add the new user to the session
    db.session.add(new_user)

    # Commit the session to persist the changes to the database
    db.session.commit()

    return render_template("detail.html",img="ImagesAttendance/{}.jpg".format(user_name))


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    user_name=request.form.get("username")
    password = request.form.get("password")
    if user_name=="admin" and password=="admin":
        return render_template("detail.html",img="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/1200px-Elon_Musk_Royal_Society_%28crop2%29.jpg")
    else:
        return render_template("Pass.html",msg="invalid password/username")



app.run(debug=1)



