import base64
import errors
from flask_restful import Resource, reqparse
from flask import request, jsonify, session, make_response
from graphs import GraphManipulator
from werkzeug import datastructures as ds

import json

graphs = GraphManipulator()
ALLOWED_EXTENSIONS = {"dmrs","txt"}

class LoadGraphs(Resource):
   """Flask-RESTful Resource that allows a user to upload graphs. """

   def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('graphs',type=ds.FileStorage,location="files")
      super(LoadGraphs, self).__init__()

   def invalid_file_type(self,file):
      
      if file is None:
         raise errors.IncorrectFileType

      filename=file.filename
      if not('.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            raise errors.IncorrectFileType
      
   def file_empty_check(self,graph_data):
      
      size=0
      try:
         pos = graph_data.tell()
         graph_data.seek(0, 2)
         size = graph_data.tell()
         graph_data.seek(pos)  
      except (AttributeError, IOError):
         pass

      if size == 0:
         raise errors.EmptyFileUploaded
   
   def file_validity(self,file):
      
      try:
         self.invalid_file_type(file)
         self.file_empty_check(file)
      except (errors.EmptyFileUploaded, errors.IncorrectFileType) as e:
         raise e


   def post(self):
      graphs.clear()
      args = self.reqparse.parse_args()

      self.file_validity(args['graphs'])

      warnings = []
      for graph in args['graphs']:
         
         try:  
            graphs.addGraph(graph)
         except (errors.GraphIdNotInteger,errors.GraphAlreadyExists,errors.GraphParseError) as e:
            warnings.append(str(e))

      if len(graphs) > 0:
         response = {"status" : 200, "message" : f"Successfully uploaded all {len(graphs)} graphs."}
         if warnings:
            response['warnings'] = warnings #"\n".join(errors)
      else:
         response = {"status" : 400, "error" : "Bad Request", "message" : f"No graphs were uploaded.", "error_logs" : "\n".join(warnings) }
         
      return response, response['status']

class NodeNeighbours(Resource):
   """Flask-RESTful Resource that allows a user to get a node's neigbours.
   Neighbours are defined by incoming and outgoing edges."""

   def get(self,graph_id,node_id):
      
      result = {}
      
      try:
         result["output"] = {graph_id : graphs.getNodeNeighbours(graph_id,node_id)}
         result["status"] = 200
         result["message"] = f"The neighbours of node {node_id} in graph {graph_id} have been successfully returned."
         return result,result["status"] 
      except (errors.GraphsNotFound,errors.NodeNotFoundError) as e:
         return {"message" : str(e) ,"status":404},404
      except:
         raise errors.InternalServerError
   
class GraphComparison(Resource):
   """Flask-RESTful Resource that allows a user to compare 2 graphs for similarities and differences.
   The graphs are specified by their graph ids. """

   def get(self,graph_id_1,graph_id_2):

      try:
         result = {}
         result["output"] = graphs.compare(graph_id_1,graph_id_2)
         result["status"] = 200
         result["message"] = "Differences and similarities have been successfully returned."
         return result,result["status"]             
         
      except errors.GraphsNotFound as e:
         return {"message" :str(e) ,"status" : 404},404
      except (errors.GraphIdNotInteger,errors.GraphComparisonError) as e:
         return {"status" : 400, "message" : str(e)}, 400
      # except Exception as e:
      #    raise errors.InternalServerError

class GraphsBySubgraph(Resource):
   """Flask-RESTful Resource that allows a user to get a list of graph objects that contain a subgraph. """


   def post(self):

      try:
         subgraph = request.get_json(force=True)
         result = {}
         result["output"] = graphs.checkSubgraph(subgraph)
         result["graph_ids"] = list(result["output"].keys())
         result['status'] = 200
         result['message'] = "Graphs that contain the input subset have been successfully returned."
         return result 
      except errors.GraphsNotFound as e:
         return {"message" : str(e), "status" : 404},404
      except:
         raise errors.JsonParseError
      
class GraphProperties(Resource):
   """Flask-RESTful Resource that allows a user to get a graphs properties based on its ID. """

   def get(self,graph_id):
      
      try:
         result = {}
         result["output"] = graphs.checkProperties(graph_id)
         result['status'] = 200
         result['message'] = f"Successfully found the properties of Graph {graph_id}."
         return result
      except errors.GraphsNotFound as e:
         return {'status' : 404, 'message' : str(e)},404
      except Exception as e:
         raise errors.InternalServerError
         
class GraphsByNodes(Resource):
   """Flask-RESTful Resource that allows a user to get a list of graph objects that contain a list of node labels. """

   def get(self,label):
      result =  {}

      try:
         # args = request.get_json(force=True)
         graph_list = graphs.getGraphsByNode([label])
         result["output"] = graph_list[0]
         result["graph_ids"] = graph_list[1]
         result["message"] = "Successfully returned graphs"
         result["status"] = 200
         return result,result["status"]

      except errors.GraphsNotFound as e:
         return {"message" : str(e), "status" : 404},404
      except errors.NoNodeLabelsSupplied as e:
         return {"message" : str(e), "status" : 400},400
      except:
         raise errors.JsonParseError
    
class GraphsById(Resource):
   """Flask-RESTful Resource that allows a user to get a list of graph objects based on a list of graph_ids. """

   def get(self):

      result = {}

      try:
         args = request.get_json(force=True)
         graph_list = graphs.getGraphs(args["graph_id_list"])

         result["output"] = graph_list[0]
         result["graph_ids"] = graph_list[1]
         if len(graph_list) > 2:
            result["error_logs"] = graph_list[2]
         result["status"] = 200
         result["message"] = "Returned all graph ids present in graph collection."
         return result,result["status"] 

      except errors.GraphsNotFound as e:
         return {"message" : str(e), "status" : 404},404
      except Exception:
         raise errors.JsonParseError

class GraphsByPage(Resource):
   """Flask-RESTful Resource that allows a user to get a list of graphs based on pagination principles. """

   def get(self,page_no):
      
      try:
         result = graphs.getGraphsByPage(page_no)
         result["status"] = 200
         return result,result["status"] 
      except errors.PageOutOfBounds as e:         
         return {"message" : str(e), "status":404},404
      except (errors.HTTPException,Exception, TypeError) as e:
         raise errors.InternalServerError
      
class GraphCount(Resource):
   def get(self):
      return {"count":len(graphs)}

class GraphRD(Resource):
   """Flask-RESTful Resource that allows a user to get or delete a graph based on a graph_id """

   def get(self,graph_id):
      try:
         graph = graphs.getGraph(graph_id)
         return {"status": 200, "message": f"Graph {graph_id} has been returned.", "output":(graph.as_dict())}
      except errors.GraphsNotFound as e:
         return {"status" : 404, "message" : str(e)}, 404
      except errors.GraphIdNotInteger as e:
         return {"status" : 400, "message" : str(e)}, 400
      except errors.HTTPException as e:
         raise errors.InternalServerError

   def delete(self,graph_id):
      if graphs.delGraph(graph_id):
         return {"status": 200, "message":f"Graph {graph_id} deleted"}

      return {"status": 203, "message": f"Graph {graph_id} not found."},404