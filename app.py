from flask import Flask, render_template, redirect, json, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session, sessionmaker, declarative_base
from sqlalchemy import String, Integer, DateTime, Column, create_engine
from sqlalchemy.sql import func, select
import json

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

# PAYERS AND USERS TABLE CREATION
class Payers(db.Model):
    __tablename__ = 'Payers'
    id = Column('payer_id',db.Integer , primary_key=True)
    user_payer_id = Column('user_payer_id', db.Integer, nullable=False) #id connecting user and payer
    name = Column(db.String, nullable=False)
    points = Column(db.Integer, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), default=func.now())
        
class Users(db.Model):
    __tablename__ = 'Users'
    id = Column('user_id', db.Integer, primary_key=True)
    user_payer_id = Column('user_payer_id', db.Integer, nullable=False, unique=True) #id connecting user and payer
    name = Column(db.String, nullable=False, unique=True)
    points = Column(db.Integer, nullable=False)
        
db.create_all()
db.session.commit()
admin.add_view(ModelView(Payers, db.session))
admin.add_view(ModelView(Users, db.session))

# HELPER FUNCTIONS
def dictionary(all_payers):
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

#ROUTES
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def adminView():
    return redirect('/admin')

@app.route('/spend', methods=["GET", "POST"])
def user_spend():
    if request.method == "POST":
        amount = request.form.get("amount")
        return "The amount that will be spent is [" + amount + "]"
        
@app.route('/balance', methods=['GET', 'POST'])
def point_bal():
    return dictionary(Payers.query.all())

if __name__ == '__main__':
    app.run()