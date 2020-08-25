from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import json
from graphs import Graph

def create_app(app_name='GRAPH_API'):
   app = Flask(app_name)
   return app

app = create_app()
api = Api(app)
graphs = {}


parser = reqparse.RequestParser()
parser.add_argument('graphs')

class GraphAPI(Resource):
   def get(self,graph_id):
      return {graphs: graphs[graph_id]}

   def post(self):
      args = parser.parse_args()
      graph_list = [json.loads(graph) for graph in args['graphs'].split("\n")]
      
      for graph in graph_list:
         graphs[graph['id']] = Graph(graph)
         graphs[graph['id']].display()

      return {"graphs":len(graph_list)}
      

api.add_resource(GraphAPI, '/', endpoint="graphs")


if __name__ == "__main__":
   app.run(debug=True,threaded=True)