from flask import Flask
from flask_restful import Resource, reqparse, Api
import time
import struct
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rtbparnxbzpkfj:7af491d615adeaf621cfcbe7f47c79348ffaa7f9c0da4bf438612c77c43762c4@ec2-54-235-104-136.compute-1.amazonaws.com:5432/daovsp0ht67uql'
app.config['SECRET_KEY'] = '7af491d615adeaf621cfcbe7f47c79348ffaa7f9c0da4bf438612c77c43762c4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

#Setting the location for the sqlite database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
#Adding the configurations for the database
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['PROPAGATE_EXCEPTIONS'] = True

from base import Access,AccessHistory,db
db.init_app(app)
app.app_context().push()
db.create_all()
parser = reqparse.RequestParser()


class sigFoxGet(Resource):
    def get(self):
        parser.add_argument('deviceId', type=str)
        parser.add_argument('time', type=int)
        parser.add_argument('data', type=str)
        args = parser.parse_args()
        a = struct.unpack('iii',bytes.fromhex(args['data']))
        print("este es el contenido",a)
        print(a[0])
        print(a[1])
        print(a[2])
        temperatura = float(a[0])
        temperatura = temperatura/10
        voltaje = float(a[1])
        voltaje = voltaje/10
        corriente = float(a[2])
        corriente = corriente/10
        fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(args['time']))
        #temperatura = bytes.fromhex(args['data']).decode('utf-8')
        print("La temperatura es", temperatura)
        print("La fecha es", fecha)
        itemb2 = AccessHistory(args['deviceId'], temperatura, voltaje, corriente, fecha)
        itemb2.save_to()
        item = Access.find_by_title(args['deviceId'])        
        if item:            
            item.temperatura = temperatura
            item.voltaje = voltaje
            item.corriente = corriente
            item.time = fecha            
            item.save_to()        
            return item.json()
        else:
            item = Access(args['deviceId'], temperatura, voltaje, corriente, fecha)
            item.save_to()        
            return item.json()
        
    
  #def get(self):
        #parser.add_argument('deviceId', type=str)
        #parser.add_argument('time', type=int)
        #parser.add_argument('data', type=str)


        #args = parser.parse_args()
        #fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(args['time']))
        #temperatura = bytes.fromhex(args['data']).decode('utf-8')
        #item = Access(args['deviceId'], temperatura, fecha)
        #print("La temperatura es"+ temperatura)
        #print("La fecha es" + fecha)
        #item.save_to()
        #return item.json()


        
class All_Movies(Resource):
    def get(self):
        return list(map(lambda x: x.json(), Access.query.all()))
class DeviceHistory(Resource):
    def get(self):
        args = parser.parse_args()
        return list(map(lambda x: x.json(), Access.find_by_title(args['deviceId']).all()))

class AllRegister(Resource):
    def get(self):
        return list(map(lambda x: x.json(), AccessHistory.query.all()))
    
api.add_resource(All_Movies, '/values')
api.add_resource(sigFoxGet,'/sigFoxGet')
api.add_resource(AllRegister, '/history')

if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)