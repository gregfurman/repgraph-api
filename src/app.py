from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api import api as endpoints
from errors import custom_errors


def create_app(config: dict = None) -> Flask:
   """Application factory method to create and initialise Flask web app"""
   
   app = Flask(__name__)
   cors = CORS(app)
   api=Api(app,errors=custom_errors)

   @app.errorhandler(404)
   def page_not_found(e):
      return {"message" : "page not found"}, 404
   
   @app.errorhandler(400)
   def page_not_found(e):
      return {"message" : "Bad request"}, 400

   create_routes(api)

   return app

def create_routes(api:Api):
   
   api.add_resource(endpoints.LoadGraphs, '/load_graphs')
   api.add_resource(endpoints.NodeNeighbours, '/display_node_neighbours/<string:graph_id>_<int:node_id>')
   api.add_resource(endpoints.GraphProperties, '/graph_properties/<int:graph_id>')
   api.add_resource(endpoints.GraphsBySubgraph,'/search_subgraph')
   api.add_resource(endpoints.GraphsByNodes,'/node_search')
   api.add_resource(endpoints.GraphsById,'/get_graphs')
   api.add_resource(endpoints.GraphsBySentence,'/sentence') 
   api.add_resource(endpoints.GraphsByPage,'/get_graphs/<int:page_no>')
   api.add_resource(endpoints.GraphCount,'/graph_count')
   api.add_resource(endpoints.GraphRD,'/graphs/<string:graph_id>') 
   api.add_resource(endpoints.GraphComparison,'/compare/<string:graph_id_1>_<string:graph_id_2>')