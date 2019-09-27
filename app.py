from flask import Flask
from flask_restful import Resource, reqparse, Api
import time
import struct
from datetime import datetime

app = Flask(__name__)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tequnzjdwbbtfc:bd46fbe1c5e8333076e8df866026fd41551853145dd50c66316f5a11ebf4d7e5@ec2-54-235-167-210.compute-1.amazonaws.com:5432/derhr019c671ph'
#app.config['SECRET_KEY'] = 'bd46fbe1c5e8333076e8df866026fd41551853145dd50c66316f5a11ebf4d7e5'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['PROPAGATE_EXCEPTIONS'] = True

#Setting the location for the sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
#Adding the configurations for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

from base import Access,AccessHistory,db
db.init_app(app)
app.app_context().push()
db.create_all()
parser = reqparse.RequestParser()

#dic_mensajes = {
  #"Sigma": "0000",
  #"La": "0001",
  #"Villita": "0010",
  #"Noche": "0011",
  #"Buena": "0000",
  #"|": "0101",
  #"Encantados": "0110",
  #"de": "0111",
  #"ayudarte": "1100",
  #"Creemos": "1001",
  #"en": "1010",
  #"ti": "1011",
  #"Promociones": "1000",
  #"": "1101",
  #"|": "1110",
  #"#": "1111",
#}

class home(Resource):
    def get(self):
        return "Bienvenido a Global Access a donde quiera que estes te comunicamos con el mundo."


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
        #itemb2 = AccessHistory(args['deviceId'], temperatura, voltaje, corriente, fecha)
        #itemb2.save_to()
        item = Access.find_by_title(args['deviceId'])        
        if item:            
            item.temperatura = temperatura
            item.voltaje = voltaje
            item.corriente = corriente
            item.time = fecha            
            item.save_to()        
            return item.json()
        else:
           # item = Access(args['deviceId'], temperatura, voltaje, corriente, fecha)
           # item.save_to()        
            return item.json()
        
class sigFoxGetDemo(Resource):
    def get(self):
        parser.add_argument('deviceId', type=str)
        parser.add_argument('time', type=int)
        parser.add_argument('data', type=str)
        args = parser.parse_args()
        a = struct.unpack('iii',bytes.fromhex(args['data']))
        print("este es el contenido",a)
        datoBajo = a[0]
        datoMedio = a[1]
        datoAlto = a[2]

        print(datoBajo)

        print(datoMedio)
        print(datoAlto)
        datoBajo = format(datoBajo,"b")
        print("binario dato bajo",datoBajo,len(datoBajo))

        if(datoBajo=="0"):
            temperatura = 0
            corriente = 0
        else:
            corriente = datoBajo[len(datoBajo)-7:len(datoBajo)]
            corriente = int(corriente,2)
            corriente = corriente/10
            temperatura = datoBajo[0:len(datoBajo)-8]
            temperatura = int(temperatura,2)
            temperatura = temperatura/10
        
        print("temperatura y corriente",temperatura,corriente)


        datoMedio = format(datoMedio,"b")
        print(datoMedio)
        print(len(datoMedio))
        if(len(datoMedio)==1):
            voltaje = 0.0
            signo="0"
        else:
            voltaje = datoMedio[0:len(datoMedio)-1]
            voltaje = int(voltaje,2)
            voltaje = voltaje/10

        print(voltaje)
        signo = datoMedio[len(datoMedio)-1]
        if(signo=="0"):
            temperatura = temperatura
        if(signo=="1"):
            temperatura = temperatura*-1    
        print(signo)
        datoAlto = format(datoAlto,"b")
        print(datoAlto)
        alerta_puerta_abierta = datoAlto[1:3]
        fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(args['time']))
        print(temperatura,voltaje,corriente,alerta_puerta_abierta,fecha)

    
        #itemb2 = AccessHistory(args['deviceId'], str(temperatura),str(voltaje),str(corriente), fecha)
        #itemb2.save_to()
        item = Access.find_by_title(args['deviceId'])        
        if item:            
            item.temperatura = temperatura
            item.voltaje = voltaje
            item.corriente = corriente 
            item.puerta_abierta = alerta_puerta_abierta
            item.time = fecha            
            item.save_to()        
            return item.json()
        else:
            item = Access(args['deviceId'], temperatura,voltaje,corriente,alerta_puerta_abierta,fecha)
            item.save_to()        
            return item.json()       


class downlink(Resource):
    def get(self):
        parser.add_argument('mensaje', type=str)
        args = parser.parse_args()
        mensaje_a_enviar = args['mensaje']
        valor_cadena = len(args['mensaje'])
        #for valor_cadena in dic_mensajes
           # mensaje_a_enviar[valor_cadena]
        return {"4D5B99" :{ "downlinkData" : "deadbeefcafebabe"}}

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
api.add_resource(sigFoxGetDemo,'/sigFoxGetDemo')
api.add_resource(AllRegister, '/history')
api.add_resource(home, '/')
api.add_resource(downlink, '/downlink')


if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)