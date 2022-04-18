from flask import Flask, render_template, redirect
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
engine = create_engine('sqlite:///app.db', echo = True)
db = SQLAlchemy(app)

admin = Admin(app, name='Dashboard', template_mode='bootstrap3')

Base = declarative_base()
Session = sessionmaker(app)
session = Session()

# SQL Models
class Payers(db.Model):
    __tablename__ = 'Payers'
    id = Column('payer_id', db.Integer, primary_key=True)
    name = Column(db.String, unique=True)
    points = Column(db.Integer, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), default=func.now())
    
    def __init__(self, name, points, timestamp):
        self.name = name
        self.points = points
        self.timestamp = timestamp
        
db.create_all()
db.session.commit()
admin.add_view(ModelView(Payers, db.session))

# 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def adminView():
    return redirect('/admin')

if __name__ == '__main__':
    app.run()