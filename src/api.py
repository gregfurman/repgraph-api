import base64
from flask_restful import Resource, reqparse
from flask import request, jsonify, session
from graphs import GraphManipulator
from werkzeug import datastructures as ds
import json

graphs = GraphManipulator()

class LoadGraphs(Resource):
   def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('graphs',type=ds.FileStorage,location="files")
      super(LoadGraphs, self).__init__()

   def post(self):

      args = self.reqparse.parse_args()
      errors = []
      counter = 0
      for graph in args['graphs']:
         counter += 1
         check = graphs.addGraph(json.loads(graph))


         if "error" in check:
            errors.append(check['error'])
         
      if counter == len(graphs):
         return {"status" : 200, "message" : f"Successfully uploaded all {len(graphs)} graphs."}

      return {"status" : 400, "error" : "Bad Request", "message" : f"Expected {counter} but found {len(graphs)} unique graphs.", "error_logs" : "\n".join(errors) }
         
class NodeNeighbours(Resource):

   def get(self,graph_id,node_id):

      result = graphs.getNodeNeighbours(graph_id,node_id)

      if "error" in result:
         result["status"] = 404
         result["message"] = f"The neighbours of node {node_id} in graph {graph_id} have not been successfully returned."
         return result

      result["status"] = 200
      result["message"] = f"The neighbours of node {node_id} in graph {graph_id} have been successfully returned."
      return result

class GraphComparison(Resource):

   def get(self,graph_id_1,graph_id_2):

      result = graphs.compare(graph_id_1,graph_id_2)

      if "error" in result:
         if result["status"] == 400:
            result["message"] = f"Bad request."
         elif result["status"] == 404:
            result["message"] = f"Graph {graph_id_1} and/or Graph {graph_id_2} do not exist."
         else:
            result["message"] = f"Internal server error."
            result["status"] = 500

      result["status"] = 200
      result["message"] = "Differences and similarities have been successfully returned."

      return result            
      
      


class GraphsBySubgraph(Resource):
   def get(self):
      subgraph = request.get_json(force=True)
      return graphs.checkSubgraph(subgraph)

class GraphProperties(Resource):
   def get(self,graph_id):

      result = graphs.checkProperties(graph_id)

      if result:
         result['status'] = 200
         result['message'] = f"Successfully found the properties of Graph {graph_id}."
         return result

      return {'status' : 404, 'message' : f"Error: Graph {graph_id} not found."}

class GraphsByNodes(Resource):
   def get(self):
      result =  {}

      try:
         args = request.get_json(force=True)
         graph_list = graphs.getGraphsByNode(args["node_labels"])

         if graph_list:
            result["output"] = graph_list
            result["message"] = "Successfully returned graphs"
            result["status"] = 200
         else:
            result["message"] = "No graphs returned."
            result["status"] = 404

      except:
         result["error"] = "Failed to decode JSON object."
         result["status"] = 400

      return result



class GraphsById(Resource):
 def get(self):

   result = {}

   try:
      args = request.get_json(force=True)
   except:
      result["error"] = "Failed to decode JSON object."
      result["status"] = 400
      return result

   graph_list = graphs.getGraphs(args["graph_id_list"])

   if graph_list:
      result["output"] = graph_list
      result["status"] = 202
      result["message"] = "Returned all graph ID present in graph collection."
   else:
      result["status"] = 404
      result["message"] = "No graphs found."


   return result

      


class GraphsByPage(Resource):
   def get(self,page_no):

      output = graphs.getGraphsByPage(page_no)

      if output:
         output["status"] = 200
         return output
      
      return {"status" : 404, "message": f"page {page_no} does not exist."}
      



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