class Node:
   """The Node class holds a node's id, label, a list of incoming and outgoing Edge objects and a list of Token objects with which it is anchored to. 
   
   :var id: The node's id. initial value:
   :param node_input: Contains information about a node such as the ID, label and a list of anchors.
   :type node_input: dict
   :param tokens: A dictionary of a tokens that a node is anchored to (default is None).
   :type tokens: dict
   """
   from errors import EdgeAddError

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

   def is_surface(self) -> bool:
      """Determines if a node is a surface node or not.
      
      :returns: if a node is a surface node then 'True' else a node is abstract therefore 'False'.
      :rtype: bool
      """
      return self.label[0] == "_"

   def as_dict(self) -> dict:
      """Returns a node as a dictionary object.
      
      :returns: node in dictionary format with a 'label' key, a list of incoming and outgoing connections to nodes by id, as well as a list of token id's with which the node is anchored.
      :rtype: dict
      """
      return {"label" : self.label, 
      "incoming" : [(edge.get_src().id) for edge in self.incomingEdges], 
      "outgoing" : [(edge.get_trg().id) for edge in self.outgoingEdges], 
      "anchors" : list(self.anchors.keys())}


   def __str__(self):
      return f"ID: {self.id}\nLabel: {self.label}\nIncoming edges: {self.incomingEdges}\nOutgoing Edges: {self.outgoingEdges}\nAnchored: {list(self.anchors.values())}"

   def __repr__(self):
      return str(self.id)

   def __cmp__(self,other):
      if self.id > other.id:
         return 1
      elif self.id < other.id:
         return -1
      
      return 0

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
         return {"incoming":[edge.get_src().id for edge in self.incomingEdges], "outgoing" :[edge.get_trg().id for edge in self.outgoingEdges]}

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
         raise self.EdgeAddError("Error adding edges") #error message or try catch
      
class Edge:

   """
   The Edge class is a directional connection between 2 nodes, having a node source (node_src) and node target (node target). 
   Each Edge also has a label and post-label.
   """
   def __init__(self,node_src,node_trg,label,post_label,add_edge=True):
      self.node_source = node_src
      self.node_target = node_trg
      self.label = label
      self.post_label = post_label

      if add_edge:
         node_src.add_edge(self)
         node_trg.add_edge(self)

   
   def get_trg(self) -> Node:
      """:returns: An edge's target node."""
      return self.node_target

   def get_src(self) -> Node:
      """:returns: An edge's source node."""
      return self.node_source

   def as_dict(self) -> dict:
      """Function that returns an edge's labels and target & source nodes in dictionary format."""
      edge_dict = {}

      if self.node_source:
         edge_dict["src"] = self.node_source.id

      if self.node_target:
         edge_dict["trg"] = self.node_target.id

      edge_dict["label"] = f"{self.label}/{ self.post_label}" 

      return edge_dict

   def __repr__(self):
      return f"src: {self.node_source.label} -{self.label}/{self.post_label}-> trg: {self.node_target.label}"

   def __str__(self):
      return f"src: {self.node_source.label} -{self.label}/{self.post_label}-> trg: {self.node_target.label}"

   def __eq__(self,other):
      return self.node_target.label == other.node_target.label and self.node_source.label == other.node_source.label and (f"{self.label}/{self.post_label}"==f"{other.label}/{other.post_label}")

class Token:
   """
   A Token object has an index, form, lemma and an optional carg.
   """
   def __init__(self,token_input):
      self.index = token_input['index']
      self.form = token_input['form']
      self.lemma = token_input['lemma']

      if 'carg' in token_input:
         self.carg = token_input['carg']
      else:
         self.carg = None

   def __repr__(self):
      if self.form != self.lemma:
         return f"[Form: {self.form} -> Lemma: {self.lemma}]"

      return f"[Form: {self.form}]"

   def as_dict(self) -> dict:
      """:returns: Token as a dictionary with the keys as ['form','lemma', (if 'carg' is not none) 'carg']"""
      
      token_dict = {}
      token_dict["form"] = self.form
      token_dict["lemma"] = self.lemma

      if self.carg is not None:
         token_dict["carg"] = self.carg

      return token_dict

class Graph:
   """A Graph object keeps a list of all the Nodes, Edges, Tokens, the original sentence being parsed and a single variable for a top node. There are multiple functions within the Graph class that allow for checking formal graph properties and longest directional & non-directional paths. 
   
   :var sentence: The original sentence being represented in DMRS format.
   :type sentence: str
   :var id: ID of a graph.
   :type id: int
   :var nodes: Dictionary of all node objects in a graph.
   :type nodes: dict
   :var edges: Dictionary of all edge objects in a graph.
   :type edges: dict
   :var tokens: initial value: dictionary of tokens parsed from graph_input['tokens']
   :type tokens: dict
   :var top: The 'top' node of the graph.
   :type top: Node
   :var connected: boolean indicating whether or not a graph is connected.
   :type connected: bool
   :raises GraphIdNotInteger: if the id of the parsed graph is not in integer or numeric form.
   """

   from collections import deque
   from errors import GraphIdNotInteger

   def __init__(self,graph_input):
      self.sentence = graph_input['input']
      try:
         self.id = int(graph_input['id'])
      except ValueError as e:
         raise self.GraphIdNotInteger(graph_input['id'])

      self.tokens = {token['index']: Token(token_input=token) for token in graph_input['tokens']}
      self.nodes = {node['id']: Node(node_input=node,tokens=self.tokens) for node in graph_input['nodes']}
      self.edges = {f"{self.nodes[edge['source']].label}-{edge['label']}/{edge['post-label']}-{self.nodes[edge['target']].label}":   Edge(self.nodes[edge['source']],self.nodes[edge['target']],edge['label'],edge['post-label']) for edge in graph_input['edges']}
      self.top = self.nodes[graph_input['tops'][0]]

      self.connected = None



   def __iter__(self,other):
      return self.id < other.id

   def __eq__(self,other):
      return self.id == other.id

   def compare(self,other):
      """Method to compare 2 graphs and return similarities and differences.
      
      :param other: A dictionary of Graph edges that is being compared with the current graph.
      :type other: dict
      :returns: A dictionary of matching and differing edges between two graphs.
      :rtype: dict
      """

      if self.sentence != other.sentence:
         return {}

      result = {}

      matching_edges = self.edges.keys() & other.edges.keys()
      different_edges = self.edges.keys() ^ other.edges.keys()

      result["matching"] = list(matching_edges)
      
      result["graph_1"] = list(self.edges.keys() & different_edges)
      result["graph_2"] = list(other.edges.keys() & different_edges)

      return result


   def display(self):
      """Displays all nodes and edges in a graph in string format."""
      [print(node) for node in self.nodes.values()]

   def getNode(self,node_id:int) -> Node:
      """Function to fetch node from 'nodes' dictionary.

      :returns: a node from the 'nodes' dictionary that correspond to graph_id.
      :param node_id: The node_id of a node being returned.
      """
      return self.nodes.get(node_id,None)
      

   def getNodes(self) -> list:
      """Function to get all nodes in the 'nodes' dictionary in list format.

      :returns: all nodes in a graph in a list.
      """
      return list(self.nodes.values)

   def has_labels(self,labels:list) -> list:
      """Function to return a list of node.ids a node's label is an element of an input list.
      
      :param labels: A list of node labels that are being searched for.
      :returns: the ids of all nodes that have their labels within the input 'labels' list.
      :rtype: list
      """
      node_ids = [str(node.id) for node in self.nodes.values() if node.label in labels]
      if len(node_ids) == len(labels):
         return node_ids

      return []
   
   def __str__(self):
       return " ".join([str(node) for node in self.nodes.values()])

   def BFS_cycle(self,transpose=False) -> bool:
      """Does a Breadth First Search in order to ascertain whether a graph is cyclic.
      
      :param transpose: Determines whether the graph being searched on is transposed (default is False).
      :returns: Whether or not a graph is cyclic.
      :rtype: bool
      """
      if transpose:
         nodes = {node.id: len(node.outgoingEdges) for node in self.nodes.values()}
      else:
         nodes = {node.id: len(node.incomingEdges) for node in self.nodes.values()}

      queue = self.deque()
      for key in nodes.keys():
         if nodes[key] == 0:
            queue.append(key)

      visited = 0

      while queue:

         s = queue.popleft()

         visited += 1

         for node_id in self.nodes[s].get_neighbours(incoming=transpose):
            nodes[node_id] -= 1
            if (nodes[node_id] == 0):
               queue.append(node_id)

      
      return len(nodes.keys()) == visited

   def BFS_connected(self,s_node:int) -> bool:
      """Does a Breadth First Search in order to determine whether a graph is connected.

      :param s_node: The id of the starting node with which the BFS will begin.      
      :returns: A boolean indicating whether or not a graph is connected.
      :rtype: bool
      """
      visited = [False]*len(self.nodes)
      queue = self.deque([s_node])

      while queue:

         s = queue.popleft()

         for node_id in self.nodes[s].get_neighbours(incoming=False) + self.nodes[s].get_neighbours(incoming=True):
            if visited[node_id] == False:
               queue.append(node_id)
               visited[node_id]=True
            
      return visited.count(visited[0]) == len(visited)


   def is_connected(self) -> bool:
      """Function to determine whether a graph is connected or not.
      
      :returns: boolean indicating if a graph is connected. The :var connected: will be changed accordingly.
      :rtype: bool
      """
      for key in self.nodes.keys():
         if not(self.BFS_connected(s_node=key)):
            self.connected = False
            return False

      self.connected = True
      return True

   def is_cyclic(self) -> bool:
      """Function for determining if a graph is cyclic.
      
      :returns: boolean indicating if a graph is cyclic.
      :rtype: bool
      """
      if not(self.BFS_cycle()):
         return False

      return True


   def DFS(self,v,directed=False,visited=None,path=None) -> list:
      """Does a Depth First Search to find the longest directed or undirected path in a graph.
      
      :param v: Each search begins at the specified node id 'v'.
      :type v: int
      :param directed: Specifies if the DFS will be done on a directed (True) or undirected (False) graph (default is False).
      :type directed: bool
      :param visited: A list of node ids that were visited in the DFS (default is None).
      :type visited: list
      :param path: An ordered list of node ids that make up the longest path (default is None).
      :type path: list
      :returns: list of longest paths with each path in as a tuple of node ids (int).
      :rtype: list 
      """

      if visited is None: visited = []
      if path is None: path = [v]
      
      visited.append(v)
   
      paths = []

      if directed:
         neighbours = self.nodes[v].get_neighbours(incoming=not(directed))
      else:
         neighbours = self.nodes[v].get_neighbours(incoming=directed) + self.nodes[v].get_neighbours(incoming=not(directed))

      for t in neighbours:
         if t not in visited:
               t_path = path + [t]
               paths.append(tuple(t_path))
               paths.extend(self.DFS(t,directed, visited[:], t_path))
         
      return paths


   def findLongestPath(self,directed=True,connected=True) -> dict:
      """Function to calculate and return the longest directed or undirected path in connected or non-connected graph.

      :param directed: boolean indicating whether the longest path being searched for is directed (True) or undirected (False) (default is True).
      :type directed: bool
      :param connected: boolean indicating whether the graph is connected (True) or disconnected (False) (default is True).
      :type connected: bool
      :returns: Dictionary of all the longest paths of a graph in list form as well as the length of the longest path.
      :rtype: list
      """
      paths = self.findAllPaths(directed=directed,connected=connected)
      max_len   = max(len(p) for p in paths)
      max_paths = [p for p in paths if len(p) == max_len]

      return {"max_paths":max_paths,"length":max_len}

   def findAllPaths(self,directed=True,connected=True) -> list:
      """Function to find all paths in the graph. 
      
      :param directed: boolean that determines whether the graph being searched through is directed (True) or undirected (False) (default is True).
      :type directed: boolean
      :param connected: boolean that determines whether the graph being searched through is connected (True) or disconnected (False) (default is True).
      :type directed: boolean
      :returns: all directed or undirected paths in a connected or non-connected graph.
      :rtype: list
      """
      paths = []

      if (directed):
         for i in range(len(self.nodes)):
            paths.extend(self.DFS(i,directed=True))
      elif not(connected):
         unseen = set(range(len(self.nodes)))
         
         while unseen:
            node = unseen.pop()
            paths_temp = self.DFS(node)
            paths.extend(paths_temp)
            for path in paths:
               unseen -= set(path)
      else:
         paths= self.DFS(0)

      return paths


   def subgraph_search(self,subgraph:dict) -> dict:
      """Returns all edges that a subgraph shares with a graph.
      
      :param subgraph: The subgraph that will be searched for within the graph.
      :type subgraph: dict
      :returns: dictionary of matching connections if the subgraph exists else an empty dictionary is returned.
      :rtype: dict
      """
      edges = []

      for node_src in subgraph.keys():
         for args in subgraph[node_src]:
            key = f"{node_src}-{args[1].upper()}/{args[2].upper()}-{args[0]}"
            if key in self.edges.keys():
               edges.append(self.edges[key].as_dict())


      if len(edges) > 0:
         return {"links" :edges}

      return {}

   def adj_nodes(self,node_id:int) -> list:
      """Function to return a list of nodes that are adjacent to a specified node of id 'node_id'.
      
      :param node_id: The node id whose neighbours are attempting to be returned.
      :type node_id: int
      :returns: a list of adjacent nodes.
      :rtype: list
      """
      node = self.nodes[node_id]
      return node.get_neighbours(True) + node.get_neighbours(False)

   def as_dict(self) -> dict:
      """Function that returns a Graph object in dictionary format. Created with the intention of sending modified graph objects to the front-end that are easier to present using the javascript D3 library.
      
      :returns: the graph in a dictionary format.
      :rtype: dict   
      """

      graph_dict = {}

      graph_dict["id"] = str(self.id)
      graph_dict["a_nodes"] = {str(node): self.nodes[node].as_dict() for node in self.nodes if not(self.nodes[node].is_surface())}
      graph_dict["s_nodes"] = {str(node): self.nodes[node].as_dict() for node in self.nodes if self.nodes[node].is_surface()}
      graph_dict["edges"] = [edge.as_dict() for edge in self.edges.values()]
      graph_dict["tokens"] = {str(token): self.tokens[token].as_dict() for token in self.tokens.keys()}
      graph_dict["tops"] = {str(self.top.id) : self.top.as_dict()}
      graph_dict["sentence"] = [token.form for token in self.tokens.values()]

      return graph_dict

class GraphManipulator:
   """The GraphManipulator class serves as a controller for the all graphs loaded via the API.

   :var Graphs: a dictionary created with the intention to store graph objects.
   :type Graphs: dict 
   """
   from errors import GraphNotFoundError,NodeNotFoundError, GraphComparisonError, GraphParseError, GraphAlreadyExists, GraphsNotFound,GraphIdNotInteger,NoNodeLabelsSupplied
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
      except ValueError as e:
         raise self.GraphParseError(e) 

      graph = Graph(graph_input)      
      
      graph_id = graph.id
      exists = graph_id in self.Graphs
      self.Graphs[graph_id] = graph

      
      if exists:
         raise self.GraphAlreadyExists(graph_id)



   def getGraph(self,graph_id):
      """Returns a graph object corresponding to a graph_id
      
      :param graph_id: The id of the graph that the user is attempting to fetch.
      :type graph_id: int
      :returns: A graph object that corresponds to the user specified graph_id.
      :rtype: Graph
      :raises GraphIdNotInteger: if the id of the graph is not in integer or numeric format.
      :raises GraphNotFoundError: if the id of the graph is not found.
      """
      
      if not isinstance(graph_id, int):
         if graph_id.isnumeric():
            graph_id = int(graph_id)
         else:
            raise self.GraphIdNotInteger(graph_id)

      graph = self.Graphs.get(graph_id,None)
      if graph is not None:
         return graph

      raise self.GraphNotFoundError(f"graph_id {graph_id} does not exist.") 

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
      :raises GraphNotFoundError: if no graphs are found to match any input ids.
      """
      
      graphs = {}
      error_logs = []
      for graph_id in graph_id_list:
         try:
            graphs[str(graph_id)] = self.getGraph(graph_id).as_dict()
         except (self.GraphIdNotInteger,self.GraphNotFoundError) as e:
            error_logs.append(str(e))


      if not graphs:
         raise self.GraphNotFoundError("None of the listed graph ids were found.")


      return graphs,list(graphs.keys()),error_logs

   def getGraphsByPage(self, page_no,graphs_per_page=5):
      """Function to determine which graphs are to be displayed per page.
      
      :param page_no: The page number that a user is requesting.
      :type page_no: int
      :param graphs_per_page: The amount of graphs to be returned per page (default is 5).
      :type graphs_per_page: int
      :raises TypeError: If the specified page_no is not in int format.
      :returns: dictionary of a list of graph objects returned, list of the graph objects ids, the amount of graphs returned and a nested dictionary of total graphs and pages remaining.
      :rtype: dict
      """
      
      if not isinstance(page_no,int):
         raise TypeError

      if page_no < 1:
         page_no=1
      else:
         total_pages = len(self.Graphs) // graphs_per_page + (1 if len(self.Graphs) % graphs_per_page else 0)

         if page_no > total_pages:
            page_no = total_pages

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
         return {"graphs" : graph_list,"graph_ids":sorted_keys, "page_no" : page_no,"returned" : len(graph_list), "remaining" : {"graphs": total_remaining, "pages": pages } }
      
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

      result = graph_1.compare(graph_2)

      if not(result):
         raise self.GraphComparisonError(f"Attempting to compare graphs with differing sentences.")

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
         raise self.NodeNotFoundError(node_id,graph_id)

      return node.get_neighbours(as_json=True)


   def getGraphsByNode(self,node_labels):
      """Returns a list of graphs that contain a list of node labels.
      
      :param node_labels: list of node labels as strings.
      :type node_labels: list
      :raises NoNodeLabelsSupplied: if no node labels are given.
      :raises GraphsNotFound: if no graphs are found containing any of the input node labels.
      :returns: tuple containing a list of Graph objects that have 1 or more matching node labels and a list of the Graph objects ids.
      :rtype: tuple
      """
      graphs = {}
      
      if not node_labels:
         raise self.NoNodeLabelsSupplied(f"No node labels were given.")
      
      graph_ids= []
      
      for key in self.Graphs.keys():
         node_ids = self.Graphs[key].has_labels(node_labels)
         if node_ids:
            graphs[key]=node_ids
            graph_ids.append(key)
      
      if graphs:
         return graphs,graph_ids

      raise self.GraphsNotFound(f"No graphs with labels matching {str(node_labels)} were found.")


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
         "longest_directed_path" : (self.longest_path(graph)),
         "longest_undirected_path" : (self.longest_path(graph,directed=False))}
      
   def checkSubgraph(self,json_subgraph):
      """Function to find all graphs that contain a specified subgraph pattern.
      
      :param json_subgraph: A json object containing the subgraph to be searched for.
      :type json_subgraph: json
      :raises GraphNotFoundError: 
      :returns: A dictionary of edge lists with a graph's id as the key is returned.
      :rtype: dict
      """
      
      graph_dict = {}

      for graph_id in self.Graphs:
         edge_list = self.Graphs[graph_id].subgraph_search(json_subgraph)
         if edge_list:
            graph_dict[graph_id] = edge_list
      
      if not graph_dict:
         raise self.GraphNotFoundError("No graphs found with matching subgraph.")

      return graph_dict

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
      return graph.findLongestPath(directed=directed,connected=graph.connected)

   def is_connected(self,graph):
      """Function to determine whether a given graph, specified by 'graph', is connected.
      
      :param graph: The graph object that will be checked for a longest path.
      :type graph: Graph
      :returns: a boolean indicating whether a graph is connected or disconnected.
      :rtype: bool
      """
      return graph.is_connected()

   def __len__(self):
      return len(self.Graphs.keys())