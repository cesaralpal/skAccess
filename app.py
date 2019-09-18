from flask import Flask
from flask_restful import Resource, reqparse, Api
import time
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

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

class Movies_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('deviceId', type=str, required=False, help='identificador del dispositivo')
    parser.add_argument('data', type=str, required=False, help='datos en tiempo real')
    parser.add_argument('Time', type=int, required=True, help='Fecha')
    
    def get(self, movie):
        item = Movies.find_by_title(movie)
        if item:
            return item.json()
        return {'Message': 'Movie is not found'}
    
    def post(self, movie):
        if Movies.find_by_title(movie):
            return {' Message': 'Movie with the  title {} already exists'.format(movie)}
        args = Movies_List.parser.parse_args()
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()
        
    def put(self, movie):
        args = Movies_List.parser.parse_args()
        item = Movies.find_by_title(movie)
        if item:
            item.collection = args['collection']
            item.save_to()
            return {'Movie': item.json()}
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()
            
    def delete(self, movie):
        item  = Movies.find_by_title(movie)
        if item:
            item.delete_()
            return {'Message': '{} has been deleted from records'.format(movie)}
        return {'Message': '{} is already not on the list'.format()}
    
class All_Movies(Resource):
    def get(self):
        return list(map(lambda x: x.json(), Access.query.all()))
    
api.add_resource(All_Movies, '/values')
api.add_resource(Movies_List, '/<string:movie>')
api.add_resource(sigFoxGet,'/sigFoxGet')
if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)