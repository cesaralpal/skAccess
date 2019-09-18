from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.String(30), unique=False, nullable=False)
    data = db.Column(db.String(30), unique=False, nullable=False)
    time = db.Column(db.String(30), unique=False, nullable=False)
    
    def __init__(self, deviceId, data, time):
        self.deviceId = deviceId
        self.data = data
        self.time = time
        
    def json(self):
        return {'DeviceID': self.deviceId, 'Data': self.data, 'Time': self.time}
    
    @classmethod
    def find_by_title(cls, deviceId):
        return cls.query.filter_by(deviceId=deviceId).first()
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_(self):
        db.session.delete(self)
        db.session.commit()
        
    

