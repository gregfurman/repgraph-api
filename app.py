from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import json
from graphs import GraphManipulator

# def create_app(app_name='GRAPH_API'):
#    app = Flask(app_name)
#    return app

app = Flask(__name__)
api = Api(app)
graphs = GraphManipulator()

class LoadGraphs(Resource):
   def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('graphs')
      super(LoadGraphs, self).__init__()


   def get(self):
      args = self.reqparse.parse_args()

      graph_ids = json.loads(args['graphs'])

      if "graph_id" in graph_ids:
         graph_id = graph_ids["graph_id"]
      else:
         graph_id = 0
         
      return {"graph": str(graphs.getGraph(graph_id))}

   def post(self):
      args = self.reqparse.parse_args()
      graph_list = json.loads("[" + args['graphs'].replace("}{", "},{")  + "]")

      for graph in graph_list:
         graphs.addGraph(graph)
         
         # graphs[graph['id']].display()
         print(graph['source'])
         print("Connected:",graphs.is_connected(graph['id']))
         print("Acyclic:",graphs.is_cyclic(graph['id']))
         print(graphs.longest_path(graph['id']))
         print("************************")



         #########
#        If you would like to test out graph methods you can do the following:
#        graphs[graph['id']].function(parameters)
         #########
      return {"graphs":len(graph_list)}
      
# class GetGraph(Resource):
#    def __init__(self):
#       self.reqparse = reqparse.RequestParser()
#       self.reqparse.add_argument('check_graphs')
#       super(CheckGraphsAPI,self).__init__()

#    def get(self,graph_id):
#        return str(graphs.getGraph(graph_id))


class checkGraphs(Resource):
   def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('args')
      super(checkGraphs,self).__init__()

   def get(self):
      args = self.reqparse.parse_args()
      json_args = json.loads(args['args'])

      keys = json_args.keys()

      if set(["graph_id","node_id"]) == keys:
         return graphs.getNodeNeighbours(json_args["graph_id"],json_args["node_id"])
      elif set(["node_labels"]) == keys:
         return graphs.getGraphs(json_args["node_labels"])
      elif set(["graph_id_list"]) == keys:
         return graphs.checkProperties(json_args["graph_id_list"])
      elif set(["subgraph"]) == keys:
         return graphs.checkSubgraph(json_args['subgraph'])
      

# class graphProperties(Resource):

#    def __init__(self):
#       self.reqparse = reqparse.RequestParser()
#       self.reqparse.add_argument('args')
#       super(graphProperties,self).__init__()

#    def get(self)


api.add_resource(LoadGraphs, '/',endpoint="load")
api.add_resource(checkGraphs, '/graphs',endpoint="graphs")



if __name__ == "__main__":
   app.run(debug=True,threaded=True)