from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/food_order'
db = SQLAlchemy(app)


class Menu(db.Model):
    menu_id=db.Column(db.Integer, primary_key=True)
    image=db.Column(db.String(120), unique=False, nullable=False)
    name=db.Column(db.String(80), unique=True, nullable=False)
    price=db.Column(db.Integer,unique=False, nullable=False)
    
@app.route("/")
def index():
    menu=Menu.query.filter_by().all()[0:6]
    return render_template("index.html",menu=menu)

@app.route("/cart/<int:id>",methods=['GET','POST'])
def cart(id):
    menu=Menu.query.filter_by(menu_id=id)
    return render_template("cart.html",menu=menu)

app.run(debug=True)