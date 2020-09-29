from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api import *
from errors import custom_errors


def create_app(config: dict = None) -> Flask:
   app = Flask(__name__)
   cors = CORS(app)
   api=Api(app,errors=custom_errors)

   @app.errorhandler(404)
   def page_not_found(e):
      return {"message" : "page not found"}, 404


   create_routes(api)

   return app

def create_routes(api:Api):
   api.add_resource(LoadGraphs, '/load_graphs')
   api.add_resource(NodeNeighbours, '/display_node_neighbours/<string:graph_id>_<int:node_id>')
   api.add_resource(GraphProperties, '/graph_properties/<int:graph_id>')
   api.add_resource(GraphsBySubgraph,'/search_subgraph') #
   api.add_resource(GraphsByNodes,'/node_search')
   api.add_resource(GraphsById,'/get_graphs') 
   api.add_resource(GraphsByPage,'/get_graphs/<int:page_no>')
   api.add_resource(GraphCount,'/graph_count')
   api.add_resource(GraphRD,'/graphs/<string:graph_id>') 
   api.add_resource(GraphComparison,'/compare/<string:graph_id_1>_<string:graph_id_2>')