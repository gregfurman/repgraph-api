from errors import *
from .graph import Graph

class GraphManipulator:
   """The GraphManipulator class serves as a controller for the all graphs loaded via the API.

   :var Graphs: a dictionary created with the intention to store graph objects.
   :type Graphs: dict 
   """
   import json
   def __init__(self):
      self.Graphs = {}

   def clear(self):
      """Creates a clear dictionary for graph objects."""
      self.Graphs = {}

   def addGraph(self,graph):
      """Adds a graph to the GraphManipulators Graph dictionary.
      
      :param graph: JSON data in byte form that will be parsed to Graph format.
      :type graph: bytes
      :raises GraphParseError: if the input data fails to be parsed.
      :raises GraphAlreadyExists: if the graph id specified by 'graph' already exists.
      """
      
      try:
         graph_input = self.json.loads(graph)
      except (ValueError) as e:
         raise GraphParseError(e) 


      graph = Graph(graph_input)      
      
      graph_id = graph.id
      exists = graph_id in self.Graphs
      self.Graphs[graph_id] = graph

      
      if exists:
         raise GraphAlreadyExists(graph_id)



   def getGraph(self,graph_id):
      """Returns a graph object corresponding to a graph_id
      
      :param graph_id: The id of the graph that the user is attempting to fetch.
      :type graph_id: int
      :returns: A graph object that corresponds to the user specified graph_id.
      :rtype: Graph
      :raises GraphIdNotInteger: if the id of the graph is not in integer or numeric format.
      :raises GraphsNotFound: if the id of the graph is not found.
      """
      
      if not isinstance(graph_id, int):
         if graph_id.isnumeric():
            graph_id = int(graph_id)
         else:
            raise GraphIdNotInteger(graph_id)

      graph = self.Graphs.get(graph_id,None)
      if graph is not None:
         return graph

      raise GraphsNotFound(value=graph_id,valueType="a graph_id") 

   def delGraph(self,graph_id):
      """Function to delete a graph specified by graph_id. Returns a boolean indicating success."""
      if graph_id in self.Graphs:
         del self.Graphs[graph_id]
         return True

      return False

   def getGraphs(self,graph_id_list):
      """Returns a collection of graph objects from a list of ids. 
      
      :param graph_id_list: list of graph_ids, as strings, that a user would like returned to them.
      :type graph_id_list: list 
      :returns: A tuple consisting of three lists: a list of Graph objects, a list of those Graph object keys, and a list of error logs.
      :rtype: tuple
      :raises GraphsNotFound: if no graphs are found to match any input ids.
      """
      
      graphs = {}
      error_logs = []
      for graph_id in graph_id_list:
         try:
            graphs[str(graph_id)] = self.getGraph(graph_id).as_dict()
         except (GraphIdNotInteger,GraphsNotFound) as e:
            error_logs.append(str(e))


      if not graphs:
         raise GraphsNotFound(value=str(graph_id_list),valueType="graph_ids")


      return graphs,list(graphs.keys()),error_logs

   def getGraphsByPage(self, page_no,graphs_per_page=5):
      """Function to determine which graphs are to be displayed per page.
      
      :param page_no: The page number that a user is requesting.
      :type page_no: int
      :param graphs_per_page: The amount of graphs to be returned per page (default is 5).
      :type graphs_per_page: int
      :raises TypeError: If the specified page_no is not in int format.
      :raises PageOutofBounds: If the specified page_no is out of bounds.
      :returns: dictionary of a list of graph objects returned, list of the graph objects ids, the amount of graphs returned and a nested dictionary of total graphs and pages remaining.
      :rtype: dict
      """

      if not isinstance(page_no,int):
         raise TypeError

      total_pages = len(self.Graphs) // graphs_per_page + (1 if len(self.Graphs) % graphs_per_page else 0)

      if page_no < 1 or page_no > total_pages:
         raise PageOutOfBounds(page_no,total_pages)

      sorted_keys = list(self.Graphs.keys())
      sorted_keys.sort()
      sorted_keys = sorted_keys[graphs_per_page*(page_no-1):]

      if len(sorted_keys) >= graphs_per_page:
         sorted_keys = sorted_keys[:graphs_per_page]
         
      graph_list=[]


      for key in sorted_keys:
         graph_list.append(self.Graphs[key].as_dict())

      total_remaining = len(self.Graphs) - (len(graph_list)+ (page_no-1)*graphs_per_page )
      pages = total_remaining // graphs_per_page
      if total_remaining % graphs_per_page != 0:
         pages += 1

      if total_remaining >= 0:
         return {"graphs" : graph_list,"graph_ids":sorted_keys,"total_pages" : total_pages, "page_no" : page_no,"returned" : len(graph_list), "remaining" : {"graphs": total_remaining, "pages": pages } }
      
   def compare(self,graph_id_1,graph_id_2):
      """Method to compare 2 graphs and return all similarities and differences in dictionary format.
      
      :param graph_id_1: Graph id of a graph to be compared.
      :type graph_id_1: str
      :param graph_id_2: Graph id of the other graph to be compared.
      :type graph_id_2: str
      :raises GraphComparisonError: If the graphs being compared have different sentences.
      :returns: dictionary of graph differences and similarities between graphs corresponding to 'graph_id_1' and 'graph_id_2'.
      :rtype: dict
      """

      graph_1 = self.getGraph(graph_id_1)
      graph_2 = self.getGraph(graph_id_2)

      result = {}
      
      comparison = graph_1.compare(graph_2)

      if not(comparison):
         raise GraphComparisonError(f"Attempting to compare graphs with differing sentences.")
      
      result["comparison"] = comparison
      result["graphs"] =  [graph_1.as_dict(),  graph_2.as_dict()]  

      return result

   def getNodeNeighbours(self,graph_id,node_id):
      """Function to get a given nodes neighbours from a specified graph.
      
      :param graph_id: Graph id of specified graph in which node_id will be searched for.
      :type graph_id: int
      :param node_id: Node id whose neighbours will be searched for.
      :type node_id: int
      :raises NodeNotFoundError: if the node_id is not found within the Graph corresponding to graph_id.
      :returns: dictionary of node's incoming and outgoing neighbours.
      :rtype: dict
      """
      graph = self.getGraph(graph_id)

      node = graph.getNode(node_id)

      if node is None:
         raise NodeNotFoundError(node_id,graph_id)

      subgraph = node.get_neighbours(as_json=True)
      graph.from_subgraph(subgraph)

      return subgraph

   def sentences_from_list(self,graph_ids):

      return [{"graph_id" : graph_id, "sentence" : self.Graphs[graph_id].sentence} for graph_id in graph_ids]


   def getGraphsByNode(self,node_labels):
      """Returns a list of graphs that contain a list of node labels.
      
      :param node_labels: list of node labels as strings.
      :type node_labels: list
      :raises NoNodeLabelsSupplied: if no node labels are given.
      :raises GraphsNotFound: if no graphs are found containing any of the input node labels.
      :returns: tuple containing a list of Graph objects that have 1 or more matching node labels and a list of the Graph objects ids.
      :rtype: tuple
      """
      
      
      if not node_labels:
         raise NoNodeLabelsSupplied(f"No node labels were given.")
      
      graph_ids= []
      
      
      for key in self.Graphs.keys():
         node_ids = self.Graphs[key].has_labels(node_labels)
         if node_ids:
            graph_ids.append(key)
      
      if graph_ids:
         return graph_ids,self.sentences_from_list(graph_ids)

      raise GraphsNotFound(value=str(node_labels),valueType="node labels")


   def checkProperties(self, graph_id):
      """Returns the properties for a specified graph of id 'graph_id'.
      
      :param graph_id: the id of the graph whose properties will be returned.
      :type graph_id: int
      :returns: dictionary containing the graph ID, whether the graph is acyclic and connected, as well as the longest directed and undirected paths.
      :rtype: dict
      """

      graph = self.getGraph(graph_id)

      return {
         "id" : str(graph_id),
         "connected" : str(self.is_connected(graph)), 
         "acyclic" : str(self.is_cyclic(graph)),
         "planar" : str(self.is_planar(graph)), 
         "longest_directed_path" : (self.longest_path(graph)),
         "longest_undirected_path" : (self.longest_path(graph,directed=False))}
      
   def checkSubgraph(self,subgraph_list):
      """Function to find all graphs that contain a specified subgraph pattern.
      
      :param subgraph_list: A json object containing the subgraph to be searched for.
      :type subgraph_list: list
      :raises GraphsNotFound: if no graphs are found to match the input subgraph.
      :returns: A dictionary of edge lists with a graph's id as the key is returned.
      :rtype: tuple
      """
      import re
      
      graph_ids = []

      links = [re.split('--|/',link) for link in subgraph_list]
 
      for graph_id in self.Graphs:
         edge_list = self.Graphs[graph_id].subgraph_search(links)
         if edge_list:
            graph_ids.append(graph_id)
      
      if graph_ids:
         return graph_ids,self.sentences_from_list(graph_ids)
      
      raise GraphsNotFound(valueType="connections",value="the input subgraph")


   def is_cyclic(self, graph):
      """Function to determine whether a given graph, specified by 'graph', contains a cycle.
      
      :param graph: The graph object that will be checked for a cyclic.
      :type graph: Graph
      :returns: a boolean indicating whether a graph contains a cycle.
      :rtype: bool

      """
      return graph.is_cyclic()

   def longest_path(self, graph, directed=True):
      """Returns all the longest directed or undirected paths in a graph object.
      
      :param graph: The graph object that will be checked for a longest path.
      :type graph: Graph
      :param directed: a boolean that determines whether or not the longest path will be directed or undirected (default is True).
      :type directed: bool
      :returns: a dictionary containing a list and length of the longest paths.
      :rtype: dict
      
      """

      result = graph.findLongestPath(directed=directed,connected=graph.connected)
      return result

   def is_connected(self,graph):
      """Function to determine whether a given graph, specified by 'graph', is connected.
      
      :param graph: The graph object that will be checked for a longest path.
      :type graph: Graph
      :returns: a boolean indicating whether a graph is connected or disconnected.
      :rtype: bool
      """
      return graph.is_connected()

   def is_planar(self,graph):
      return graph.planarity_check()
   
   def filter_by_tokens(self,tokens:str)->list:
      """Method to return all graph IDs where the corresponding graph's sentence contains 'tokens'.

      :param tokens: a collection of tokens which is being searched for.
      :type tokens: str
      :returns: list of graph ids where the sentence matches, even partially, the corresponding graph id's sentence.
      :rtype: list
      """
      graph_ids =[graph_id for graph_id in self.Graphs.keys() if self.Graphs[graph_id].token_search(tokens)]


      
      if graph_ids:
         return graph_ids,self.sentences_from_list(graph_ids) 

      raise GraphsNotFound(str(tokens),"a sentence")

   def __len__(self):
      return len(self.Graphs.keys())