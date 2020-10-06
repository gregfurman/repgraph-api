from flask_restful import HTTPException

custom_errors = {

   "UrlNotFound" : {
      "message" : "The requested URL does not exist.",
      "status" : 404
   },
      "InternalServerError" : {
      "message" : "Something went wrong and a resource could not be returned.",
      "status" : 500
   },
    "JsonParseError" : {
      "message" : "JSON data has failed to parse correctly.",
      "error" : "Bad request.", 
      "status" : 400
   }, "IncorrectFileType" : {
      "message" : "You must upload a valid file type.",
      "status" : 400
   },
   "EmptyFileUploaded" : {
      "message" : "Uploaded file is empty.",
      "status" : 400
   }, "GraphAlreadyExists"  : {
      "message" : "Graph id {graph_id} already exists but is being overwritten."
   }, 
   "GraphParseError" : {
      "message" : "Line {line} column {col} of file failed to be parsed succsessfully and is likely malformed."
   },
   "GraphIdNotInteger" :{
      "message" : "graph_id '{graph_id}' is not numeric."
   },
   "NodeNotFoundError" :{
      "message" : "node_id {node_id} of graph '{graph_id}' was not found."
   },
   "EdgeAddError" :{
      "message" : "Failed to add edge {edge}."
   },
   "PageOutOfBounds" :{
      "message" : "The page you requested is out of bounds. Valid pages range from [1-{total_pages}] whereas you requested {page_no}."
   },
   "GraphsNotFound" :{
      "message" : "No graphs with {valueType} matching {value} were found."
   },


}



class InternalServerError(HTTPException):
   pass

class IncorrectFileType(HTTPException):
   pass

class EmptyFileUploaded(HTTPException):
   pass

class GraphError(Exception):
   def __init__(self, error_msg: str):
      self.error_msg = error_msg

   def __str__(self):
      return self.error_msg

class GraphIdNotInteger(GraphError):
   def __init__(self,graph_id:int):
      super().__init__(custom_errors['GraphIdNotInteger']["message"].format(graph_id=graph_id))
   pass

class GraphAlreadyExists(GraphError):
   def __init__(self,graph_id):
      super().__init__(custom_errors['GraphAlreadyExists']["message"].format(graph_id=graph_id))
   pass

class PageOutOfBounds(GraphError):
   def __init__(self,page_no:int,total_pages:int):
      super().__init__(custom_errors[(str(self.__class__.__name__))]["message"].format(page_no=page_no,total_pages=total_pages))
   pass

class GraphParseError(GraphError):
   from json import decoder
   def __init__(self,decoder: decoder.JSONDecodeError ):
      super().__init__(custom_errors['GraphParseError']["message"].format(line=decoder.lineno,col=decoder.colno))
   pass

class GraphComparisonError(GraphError):
   pass

class NodeNotFoundError(GraphError):
   def __init__(self,node_id,graph_id):
      super().__init__(custom_errors['NodeNotFoundError']["message"].format(node_id=node_id,graph_id=graph_id))
   pass

class EdgeAddError(GraphError):
   def __init__(self,edge):
      super().__init__(custom_errors['EdgeAddError']["message"].format(edge=str(edge)))
   pass


class NoNodeLabelsSupplied(GraphError):
   pass


class GraphsNotFound(GraphError):
   def __init__(self,value,valueType):
      super().__init__(custom_errors[str(self.__class__.__name__)]["message"].format(value=value,valueType=valueType))



class UrlNotFound(Exception):
   pass

class JsonParseError(HTTPException):
   pass



