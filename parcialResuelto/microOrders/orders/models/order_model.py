from db.db import db
from datetime import datetime

class Orders(db.Model):
    #__tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(255), nullable=False)
    userEmail  = db.Column(db.String(255), nullable=False)
    saleTotal = db.Column(db.Float(10,2), nullable=False)  # Equivalente a decimal(10,2) en SQL
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self,userName,userEmail,saleTotal,date):
        self.userName = userName
        self.userEmail = userEmail
        self.saleTotal = saleTotal
        self.date = date
