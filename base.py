from flask_sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.String(30), unique=False, nullable=False)
    temperatura = db.Column(db.String(30), unique=False, nullable=False)
    voltaje = db.Column(db.String(30), unique=False, nullable=False)
    corriente = db.Column(db.String(30), unique=False, nullable=False)
    puerta_abierta = db.Column(db.String(30), unique=False, nullable=False)
    time = db.Column(db.String(30), unique=False, nullable=False)
    
    def __init__(self, deviceId, temperatura, voltaje, corriente, time, puerta_abierta):
        self.deviceId = deviceId
        self.temperatura = temperatura
        self.voltaje = voltaje
        self.corriente = corriente
        self.puerta_abierta = puerta_abierta
        self.time = time
        
    def json(self):
        return {'DeviceID': self.deviceId, 'Temperatura': self.temperatura, 'Voltaje':self.voltaje, 'Corriente':self.corriente, 'Puerta_abierta':self.puerta_abierta,'Time': self.time}
    
    @classmethod
    def find_by_title(cls, deviceId):
        return cls.query.filter_by(deviceId=deviceId).first()
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_(self):
        db.session.delete(self)
        db.session.commit()

class AccessHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.String(30), unique=False, nullable=False)
    temperatura = db.Column(db.String(30), unique=False, nullable=False)
    voltaje = db.Column(db.String(30), unique=False, nullable=False)
    corriente = db.Column(db.String(30), unique=False, nullable=False)
    time = db.Column(db.String(30), unique=False, nullable=False)
    
    def __init__(self, deviceId, temperatura, voltaje, corriente, time):
        self.deviceId = deviceId
        self.temperatura = temperatura
        self.voltaje = voltaje
        self.corriente = corriente
        self.time = time
        
    def json(self):
        return {'DeviceID': self.deviceId, 'Temperatura': self.temperatura, 'Voltaje':self.voltaje, 'Corriente':self.corriente, 'Time': self.time}
    
class MessageDownlink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    deviceId = db.Column(db.String(30),unique=False, nullable = False)
    message = db.Column(db.String(30),unique=False, nullable = False)

    def __init__(self, deviceId, message):
        self.deviceId = deviceId
        self.message = message
        
    def json(self):
        return {'DeviceID': self.deviceId, 'Message': self.message}


    
    @classmethod
    def find_by_title(cls, deviceId):
        return cls.query.filter_by(deviceId=deviceId).first()
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_(self):
        db.session.delete(self)
        db.session.commit()