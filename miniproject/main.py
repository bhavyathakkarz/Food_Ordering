from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/food_order'
db = SQLAlchemy(app)
app.secret_key = 'make this hard to guess!'

class Menu(db.Model):
    menu_id=db.Column(db.Integer, primary_key=True)
    image=db.Column(db.String(120), unique=False, nullable=False)
    name=db.Column(db.String(80), unique=True, nullable=False)
    price=db.Column(db.Integer,unique=False, nullable=False)

class Contacts(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(80), unique=True, nullable=False)
    content=db.Column(db.Text(200), unique=True, nullable=False)

class Registers(db.Model):
    name=db.Column(db.String(80),  nullable=False)
    username=db.Column(db.String(80), unique=True, nullable=False,primary_key=True)
    password=db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(80),  nullable=False)
    mobile_no=db.Column(db.String(80), unique=True, nullable=False)
    address=db.Column(db.Text(200),  nullable=False)
    
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/registerNext', methods = ['GET','POST'])
def registerNext():
  if request.method == "GET":
    username = request.args.get("username")
    password = request.args.get("password")
  elif request.method == "POST":
    username= request.form['username']
    password = request.form['password']
    customercheck = Registers.query.filter((Registers.username == username) & (Registers.password == password)).first()
    if customercheck:
      return render_template('userregister.html',cmsg="Registration Failed, \n User Already Registered..!")
    else:
            # entry = Registers(name=request.form["name"],username=request.form["username"],password=request.form['password'],email=request.form["email"], mobile_no=request.form["mobile_no"], address=request.form["address"])
            name= request.form.get("name")
            username=request.form.get("username")
            password=request.form.get("password")
            email=request.form.get("email")
            mobile_no=request.form.get("mobile_no")
            address=request.form.get("address")
            entry=Registers(name=name,username=username,password=password,email=email,mobile_no=mobile_no,address=address)
            db.session.add(entry)
            db.session.commit()
            return render_template('userlogin.html',cusmsg="Registered Succcessfully...! \n Please Login To Continue")

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/loginNext',methods=['GET','POST'])
def loginNext():
	# if not session.get('cmail'):
	# 	return redirect(request.url_root)
	if request.method == "GET":
		username = request.args.get("username")
		password = request.args.get("password")
	
	elif request.method == "POST":
		username = request.form['username']
		password = request.form['password']		
		customer  = Registers.query.filter((Registers.username == username) & (Registers.password == password)).first()
		if customer :
			session['username'] = request.form['username']
			return redirect(url_for('userhome1'))
			# return render_template('userhome.html',cusname=customer.cname,restadmin = Restadmin.query.all())
			# return render_template('userhome.html',restadmin = Restadmin.query.all())
		return render_template('userlogin.html',cusname="Login failed...\n Please enter valid username and password!")


@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html")


@app.route('/userhome1',methods=['GET','POST'])
def userhome1():
    if not session.get('username'):
        return redirect(request.url_root)
    username=session['username']
    customer  = Registers.query.filter(Registers.username == username).first()
    menu=Menu.query.filter_by().all()[0:6]
    if(request.method=="POST"):
        name=request.form.get("name")
        email=request.form.get("email")
        content=request.form.get("content")
        entry=Contacts(name=name,email=email,content=content)
        db.session.add(entry)
        db.session.commit()
    return render_template('userhome.html',cusname=customer.name,menu=menu)

# @app.route("/cart")
# def usercart():
#     return render_template("cart.html",menu=menu)

@app.route("/cart/<int:id>",methods=['GET','POST'])
def cart(id):
    menu=Menu.query.filter_by(menu_id=id)
    return render_template("cart.html",menu=menu)

@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))

app.run(debug=True)