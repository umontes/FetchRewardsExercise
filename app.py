from flask import Flask, render_template, redirect, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session, sessionmaker, declarative_base
from sqlalchemy import String, Integer, DateTime, Column, create_engine
from sqlalchemy.sql import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
app.secret_key = 'vivian'
engine = create_engine('sqlite:///app.db')
db = SQLAlchemy(app)

admin = Admin(app, name='Dashboard', template_mode='bootstrap3')

Base = declarative_base()
Session = sessionmaker(app)
session = Session()

# /////////////////////////////////////////////////////////

# PAYERS AND USERS TABLE CREATION
class Payers(db.Model):
    __tablename__ = 'Payers'
    id = Column('payer_id',db.Integer , primary_key=True)
    user_payer_id = Column('user_payer_id', db.Integer, nullable=False) #id connecting user and payer
    name = Column(db.String, nullable=False)
    points = Column(db.Integer, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), default=func.now())
    def __init__(self, user_payer_id, name, points, timestamp):
        self.user_payer_id = user_payer_id
        self.name = name
        self.points = points
        self.timestamp = timestamp
        
class Users(db.Model):
    __tablename__ = 'Users'
    id = Column('user_id', db.Integer, primary_key=True)
    user_payer_id = Column('user_payer_id', db.Integer, nullable=False, unique=True) #id connecting user and payer
    name = Column(db.String, nullable=False, unique=True)
    points = Column(db.Integer, nullable=False)
    def __init__(self, user_payer_id, name, points):
        self. user_payer_id = user_payer_id
        self.name = name
        self. points = points
        
db.create_all()
db.session.commit()
admin.add_view(ModelView(Payers, db.session))
admin.add_view(ModelView(Users, db.session))

# /////////////////////////////////////////////////////////

# HELPER FUNCTIONS
def getBalance(all_payers):
    dic = {}
    point_add = 0
    for payer in all_payers:
        if payer.name in dic:
            for i in Payers.query.filter_by(name=payer.name):
                point_add = i.points + point_add
            dic.update({i.name:point_add})
        else:
            dic.update({payer.name:payer.points})
        same = 0
    return dic

def point_add(new_points, payer_name):
    existing = Users.query.filter_by(name='Uriel').first()
    points_sum = int(new_points) + existing.points
    
    user = Users.query.filter(Users.name=='Uriel').first()
    user.points = points_sum
    
    payer_new = Payers(user_payer_id=user.user_payer_id, name=payer_name, points=int(new_points), timestamp=func.now())
    db.session.add(payer_new)
    
    db.session.commit()
    return "Hello"

# /////////////////////
    # Adding a new user into the table
    # new_user = Users(user_payer_id=2, name='Montes', points=100)
    # db.session.add(new_user)
    # db.session.commit()
    # ////////////////////

# /////////////////////////////////////////////////////////

#ROUTES
# renders the home.html page
@app.route('/')
def home():
    return render_template('home.html')

# Redirects to the admin page
@app.route('/admin')
def adminView():
    return redirect('/admin')

# shows the amount that the user wants to spend
@app.route('/spend', methods=["GET", "POST"])
def user_spend():
    if request.method == "POST":
        amount = request.form.get("amount")
        return "The amount that will be spent is [" + amount + "]"
        
# returns the balance of all the payers in the payers table
@app.route('/balance', methods=['GET', 'POST'])
def point_bal():
    return getBalance(Payers.query.all())

# adds points to the user 
@app.route('/adding_points/<new_points>/<payer_name>', methods=["GET"])
def add_points(new_points, payer_name):
    return point_add(new_points, payer_name)

if __name__ == '__main__':
    app.run()