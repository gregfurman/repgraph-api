from flask import Flask
from flask_restful import Api
from api import *


def create_app(config: dict = None) -> Flask:
   app = Flask(__name__)
   api=Api(app)
   create_routes(api)

   return app

def create_routes(api:Api):
   api.add_resource(LoadGraphs, '/load_graphs')
   api.add_resource(NodeNeighbours, '/display_node_neighbours/<int:graph_id>_<int:node_id>')
   api.add_resource(GraphProperties, '/graph_properties')
   api.add_resource(GraphsBySubgraph,'/search_subgraph')
   api.add_resource(GraphsByNodes,'/node_search')
   api.add_resource(GraphsById,'/get_graphs')
   api.add_resource(GraphsByPage,'/get_graphs/<int:page_no>')
   api.add_resource(GraphCount,'/graph_count')
   api.add_resource(GraphRD,'/graphs/<int:graph_id>')