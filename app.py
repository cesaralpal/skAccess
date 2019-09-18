from flask import Flask
from flask_restful import Resource, reqparse, Api
import time
from datetime import datetime

app = Flask(__name__)
api = Api(app)
config_file='settings.py'
app.config.from_pyfile(config_file)


from base import Access, db
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
        fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(args['time']))
        temperatura = bytes.fromhex(args['data']).decode('utf-8')
        item = Access(args['deviceId'], temperatura, fecha)
        print("La temperatura es"+ temperatura)
        print("La fecha es" + fecha)
        item.save_to()
        
        return item.json()

    
class All_Movies(Resource):
    def get(self):
        return list(map(lambda x: x.json(), Access.query.all()))
    
api.add_resource(All_Movies, '/values')
api.add_resource(sigFoxGet,'/sigFoxGet')
if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)