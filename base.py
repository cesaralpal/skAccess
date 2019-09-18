from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
db = SQLAlchemy()
db_string = 'postgres://rtbparnxbzpkfj:7af491d615adeaf621cfcbe7f47c79348ffaa7f9c0da4bf438612c77c43762c4@ec2-54-235-104-136.compute-1.amazonaws.com:5432/daovsp0ht67uql'
db = create_engine(db_string)

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
        
    

