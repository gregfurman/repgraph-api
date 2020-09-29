from flask_restful import HTTPException

custom_errors = {

   "UrlNotFound" : {
      "message" : "The requested URL does not exist.",
      "status" : 404
   },
      "InternalServerError" : {
      "message" : "Something went wrong and a resource could not be returned.",
      "status" : 500

   }, "JsonParseError" : {
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
   pass

class GraphAlreadyExists(GraphError):
   pass

class GraphNotFoundError(GraphError):
   pass

class GraphParseError(GraphError):
   pass

class GraphComparisonError(GraphError):
   pass

class NodeNotFoundError(GraphError):
   pass

class NoNodeLabelsSupplied(GraphError):
   pass

class PageOutOfBounds(GraphError):
   pass

class GraphsNotFound(GraphError):
   pass

class UrlNotFound(Exception):
   pass

class JsonParseError(HTTPException):
   pass


