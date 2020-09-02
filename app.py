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
   api.add_resource(NodeNeighbours, '/display_node_neighbours/<string:graph_id>_<string:node_id>')
   api.add_resource(GraphProperties, '/graph_properties')
   api.add_resource(GraphsBySubgraph,'/search_subgraph')
   api.add_resource(GraphsByNodes,'/node_search')
   api.add_resource(GraphsById,'/get_graphs')
   api.add_resource(GraphCount,'/graph_count')
   api.add_resource(GraphRD,'/graphs/<string:graph_id>')

if __name__ == "__main__":
   app=create_app()
   app.run(debug=True)