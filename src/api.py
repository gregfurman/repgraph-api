import base64
from errors import *
from flask_restful import Resource, reqparse
from flask import request, jsonify, session, make_response
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
      graphs.clear()
      args = self.reqparse.parse_args()
      errors = []
      counter = 0
      for graph in args['graphs']:
         counter += 1
         try:
            graphs.addGraph(json.loads(graph))
         except GraphAlreadyExists as e:
            errors.append(str(e))
         except GraphParseError as e:
            errors.append(str(e))
      
      if not(errors):
         return {"status" : 200, "message" : f"Successfully uploaded all {len(graphs)} graphs."}

      return {"status" : 400, "error" : "Bad Request", "message" : f"Expected {counter} but found {len(graphs)} unique graphs.", "error_logs" : "\n".join(errors) },400
         
class NodeNeighbours(Resource):

   def get(self,graph_id,node_id):
      
      result = {}
      
      try:
         result = graphs.getNodeNeighbours(graph_id,node_id)
         result["status"] = 200
         result["message"] = f"The neighbours of node {node_id} in graph {graph_id} have been successfully returned."
         return result,result["status"] 
      except (GraphNotFoundError,NodeNotFoundError) as e:
         return {"message" : str(e) ,"status":404},404
      except Exception as e:
         raise InternalServerError
   

class GraphComparison(Resource):

   def get(self,graph_id_1,graph_id_2):

      try:
         result = graphs.compare(graph_id_1,graph_id_2)
         result["status"] = 200
         result["message"] = "Differences and similarities have been successfully returned."
         return result,result["status"]             
         
      except (GraphNotFoundError,GraphComparisonError) as e:
         return {"message" :str(e) ,"status" : 404},404
      except Exception as e:
         raise InternalServerError

class GraphsBySubgraph(Resource):
   def get(self):

      try:
         subgraph = request.get_json(force=True)
         result = graphs.checkSubgraph(subgraph)

         if result:
            result['status'] = 200
            result['message'] = "Graphs that contain the input subset have been successfully returned."
            return result 

         # return {"status": 204, "message" : "No graph was found that matched the input subgraph.", "error" : "No matching subgraphs found." },204
         return 204
      except:
         raise JsonParseError
      



class GraphProperties(Resource):
   def get(self,graph_id):
      
      try:
         result = graphs.checkProperties(graph_id)
         result['status'] = 200
         result['message'] = f"Successfully found the properties of Graph {graph_id}."
         return result
      except GraphNotFoundError as e:
         return {'status' : 404, 'message' : str(e)},404
      except Exception as e:
         raise InternalServerError
         
class GraphsByNodes(Resource):
   def get(self):
      result =  {}

      try:
         args = request.get_json(force=True)
         graph_list = graphs.getGraphsByNode(args["node_labels"])
         result["output"] = graph_list
         result["message"] = "Successfully returned graphs"
         result["status"] = 200
         return result,result["status"]

      except GraphsNotFound as e:
         return {"message" : str(e), "status" : 404}
      except:
         raise JsonParseError

      
class GraphsById(Resource):
 def get(self):

   result = {}

   try:
      args = request.get_json(force=True)
      graph_list = graphs.getGraphs(args["graph_id_list"])

      if graph_list:
         result["output"] = graph_list
         result["status"] = 200
         result["message"] = "Returned all graph ID present in graph collection."
         return result,result["status"] 

      return 204

   except:
      raise JsonParseError

class GraphsByPage(Resource):
   def get(self,page_no):

      result = graphs.getGraphsByPage(page_no)

      if result:
         result["status"] = 200
         return result,result["status"] 
      
      return 204
      
class GraphCount(Resource):
   def get(self):
      return {"count":len(graphs)}

class GraphRD(Resource):
   def get(self,graph_id):
      try:
         graph = graphs.getGraph(graph_id)
         if graph is not None:
            return {"status": 200, "message": f"Graph {graph_id} has been returned.", "output":str(graph.as_dict())}
      except GraphNotFoundError as e:
         return {"status" : 404, "message" : str(e)}, 404
      except Exception as e:
         raise InternalServerError

   def delete(self,graph_id):
      if graphs.delGraph(graph_id):
         return {"status": 200, "message":f"Graph {graph_id} deleted"}

      return {"status": 203, "message": f"Graph {graph_id} not found."},404