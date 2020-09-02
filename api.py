import base64
from flask_restful import Resource, reqparse
from flask import request, jsonify, session
from graphs import GraphManipulator

graphs = GraphManipulator()

class LoadGraphs(Resource):
   def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('graphs')
      super(LoadGraphs, self).__init__()

   def post(self):
      graph_list = request.get_json(force=True)

      for graph in graph_list:
         graphs.addGraph(graph)
         
      return {"graphs":len(graphs)}
         
class NodeNeighbours(Resource):

   def get(self,graph_id,node_id):

      return graphs.getNodeNeighbours(graph_id,node_id)

class GraphsBySubgraph(Resource):
   def get(self):
      subgraph = request.get_json(force=True)
      return graphs.checkSubgraph(subgraph)

class GraphProperties(Resource):
   def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('graphID',action="append")
      super(GraphProperties,self).__init__()

   def get(self):
      args = self.reqparse.parse_args()
      return graphs.checkProperties(args['graphID'])

class GraphsByNodes(Resource):
   def get(self):
      args = self.reqparse.parse_args()
      return graphs.getGraphsByNode(args["node_labels"])

class GraphsById(Resource):
 def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('graph_id_list')
      super(GraphsById, self).__init__()

 def get(self):
      args = self.reqparse.parse_args()
      return graphs.getGraphs(args["graph_id_list"])

class GraphCount(Resource):
   def get(self):
      return {"count":len(graphs)}

class GraphRD(Resource):
   def get(self,graph_id):
      graph = graphs.getGraph(graph_id)
      if graph is not None:
         return {"status": 204, "message": f"Graph {graph_id} has been returned.", "output":str(graph.as_dict())}

      return {"status": 404, "message": f"Graph {graph_id} not been found."}


   def delete(self,graph_id):
      if graphs.delGraph(graph_id):
         return {"status": 204, "message":f"Graph {graph_id} deleted"}

      return {"status": 404, "message": f"Graph {graph_id} not found."}
