from errors import *

class Node:
   """The Node class holds a node's id, label, a list of incoming and outgoing Edge objects and a list of Token objects with which it is anchored to. 
   
   :var id: The node's id. initial value:
   :param node_input: Contains information about a node such as the ID, label and a list of anchors.
   :type node_input: dict
   :param tokens: A dictionary of a tokens that a node is anchored to (default is None).
   :type tokens: dict
   """

   def __init__(self,node_input,tokens=None):
      self.id = node_input['id']
      self.label = node_input['label']
      self.incomingEdges = []
      self.outgoingEdges = []

      
      if tokens is not None:
         self.anchors = {token_id: tokens[token_id] for token_id in range(node_input['anchors'][0]["from"],node_input['anchors'][0]["end"]+1)}
      else:
         self.anchors = {}


   def __eq__(self, other):
      return other.label == self.label

   def __ne__(self, other):
      return not(other.label == self.label)

   def compare(self,other):
      min_key = self.min_token()
      other_min_key = other.min_token()
      if min_key > other_min_key:
         return 1
      elif min_key < other_min_key:
         return -1
      else:
         return 0
   
   def min_token(self):
      return min(self.anchors.keys())

   def max_token(self):
      return max(self.anchors.keys())

   def is_surface(self) -> bool:
      """Determines if a node is a surface node or not.
      
      :returns: if a node is a surface node then 'True' else a node is abstract therefore 'False'.
      :rtype: bool
      """
      return self.label[0] == "_" 

   def as_dict(self,include_neighbours=True,include_id=False) -> dict:
      """Returns a node as a dictionary object.
      
      :param include_neighbours: boolean to include a node's incoming and outgoing neighbours in the resulting dictionary (default is True).
      :type include_neighbours: bool
      :returns: node in dictionary format with a 'label' key, a list of incoming and outgoing connections to nodes by id, as well as a list of token id's with which the node is anchored.
      :rtype: dict
      """

      result = {"label" : self.label, 
      "anchors" : list(self.anchors.keys())}

      if include_neighbours:
         result["incoming"] = list({(edge.get_src().id) for edge in self.incomingEdges})
         result["outgoing"] = list({(edge.get_trg().id) for edge in self.outgoingEdges})
      
      if include_id:
         result["id"] = str(self.id)

      return result

   def get_neighbour_by_node(self,node_id,directed=True):
      """Returns an edge by node id. 
      
      """
      if directed:
         result= [edge for edge in self.outgoingEdges if edge.get_trg().id==node_id]
      else:
         result= [edge for edge in self.outgoingEdges+self.incomingEdges if edge.get_trg().id==node_id or edge.get_src().id==node_id]

      return result.pop()

   def __str__(self):
      return f"ID: {self.id}\nLabel: {self.label}\nIncoming edges: {self.incomingEdges}\nOutgoing Edges: {self.outgoingEdges}\nAnchored: {list(self.anchors.values())}"

   def __repr__(self):
      return str(self.id)

   # def __cmp__(self,other):
   #    if self.id > other.id:
   #       return 1
   #    elif self.id < other.id:
   #       return -1
      
   #    return 0

   def compare_labels(self,other):
      return other.label == self.label

   def get_neighbours(self,incoming=True,as_json=False):
      """Returns a dictionary containing a list of incoming and/or outgoing nodes from a specific node id.
      
      :param incoming: Boolean that determines whether the neighbours being returned are incoming (True) or outgoing (False).
      :type incoming: bool
      :param as_json: If true, the function returns both incoming and outgoing nodes in dictionary form.
      :returns: if as_json is True then return a dictionary of incoming and outgoing node ids as lists else return incoming or outgoing node ids.
      :rtype: list or dict
      """
      if as_json:
         subgraph = {}
         subgraph['edges'] = {edge.get_label():edge for edge in self.incomingEdges}
         subgraph['edges'].update({edge.get_label(): edge for edge in self.outgoingEdges})

         nodes = {self.id: self}
         nodes.update({edge.get_src().id: edge.get_src() for edge in self.incomingEdges})
         nodes.update({edge.get_trg().id: edge.get_trg() for edge in self.outgoingEdges}) 
         subgraph['a_nodes'] = {str(node): nodes[node].as_dict(False) for node in nodes if not(nodes[node].is_surface())}
         subgraph['s_nodes'] = {str(node): nodes[node].as_dict(False) for node in nodes if (nodes[node].is_surface())}

         subgraph['tokens'] = {key for x in [list(edge.get_src().anchors.keys()) for edge in self.incomingEdges]+[list(edge.get_trg().anchors.keys()) for edge in self.outgoingEdges] for key in x}
         subgraph['tops'] = str(self.id)
         
         return subgraph

      if incoming:
         return [edge.get_src().id for edge in self.incomingEdges]

      return [edge.get_trg().id for edge in self.outgoingEdges]



   def add_edge(self,edge):
      """Adds an Edge object to a nodes incoming or outgoing edges list.
      
      :param edge: The Edge object that is being added to an incoming or outgoing edge list.
      :type edge: Edge
      :raises EdgeAddError: if an Edge object fails to be added to an incoming or outgoing edge list. 
      """
      if (self.id == edge.node_source.id):
         self.outgoingEdges.append(edge)
      elif(self.id == edge.node_target.id):
         self.incomingEdges.append(edge)
      else:
         raise self.EdgeAddError() #error message or try catch
   