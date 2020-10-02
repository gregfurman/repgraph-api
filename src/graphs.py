class Node:
   """
   The Node class holds a node's id, label, a list of incoming and outgoing Edge objects and a list of Token objects with which it is anchored to. 
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

   def is_surface(self):
      return self.label[0] == "_"

   def as_dict(self) -> dict:
      """Returns a node as a dictionary object."""
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
      """Returns a dictionary containing a list of incoming and/or outgoing nodes from a specific node id."""
      if as_json:
         return {"incoming":[edge.get_src().id for edge in self.incomingEdges], "outgoing" :[edge.get_trg().id for edge in self.outgoingEdges]}

      if incoming:
         return [edge.get_src().id for edge in self.incomingEdges]

      return [edge.get_trg().id for edge in self.outgoingEdges]

   def add_edge(self,edge):
      if (self.id == edge.node_source.id):
         self.outgoingEdges.append(edge)
      elif(self.id == edge.node_target.id):
         self.incomingEdges.append(edge)
      else:
         raise Exception("Error adding edges") #error message or try catch
      

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
      """Returns an edge's target node."""
      return self.node_target

   def get_src(self) -> Node:
      """Returns an edge's source node."""
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

   def __hash__(self):
      return hash(f"{self.node_source.label}-{self.label}/{self.post_label}-{self.node_target.label}")

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
      token_dict = {}
      token_dict["form"] = self.form
      token_dict["lemma"] = self.lemma

      if self.carg is not None:
         token_dict["carg"] = self.carg

      return token_dict

class Graph:
   from collections import deque
   from errors import GraphParseError, NodeNotFoundError, GraphIdNotInteger
   """
   A Graph object keeps a list of all the Nodes, Edges, Tokens, the original sentence being parsed and a single variable for a top node.
   There are multiple functions within the Graph class that allow for checking formal graph properties and longest directional & non-directional paths. 
   
   Attributes
   ----------
   sentence : str
      The original sentence being represented in DMRS format.
   id : str
      ID of a graph.
   nodes : dict
      Dictionary of all node objects in a graph.
   edges : dict
      Dictionary of all edge objects in a graph.
   top : Node
      The top node in a graph.
   
   Methods
   ---------
   """
   def __init__(self,graph_input):
      """ 
      Parameters
      ----------
      graph_input : dict
         The graph represented by DMRS in json format. 
      """
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
      """Method to compare 2 graphs and return similarities and differences."""

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
      """Returns a node from the 'nodes' dictionary that correspond to graph_id."""
      node = self.nodes.get(node_id,None)
      
      if node is not None:
         return node

      raise self.NodeNotFoundError(f"node_id {node_id} of graph {self.id} does not exist.")

   def getNodes(self) -> list:
      """Returns all nodes in a graph in a list."""
      return list(self.nodes.values)

   def has_labels(self,labels:list) -> list:
      """Returns the ID of all nodes that have their labels within the input 'labels' list."""
      node_ids = [str(node.id) for node in self.nodes.values() if node.label in labels]
      if len(node_ids) == len(labels):
         return node_ids

      return []
   
   def __str__(self):
       return " ".join([str(node) for node in self.nodes.values()])

   def BFS_cycle(self,transpose=False) -> bool:
      """Does a Breadth First Search in order to ascertain whether a graph is cyclic."""
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
      """Does a Breadth First Search in order to determine whether a graph is connected."""
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
      """Returns if a graph is connected."""
      for key in self.nodes.keys():
         if not(self.BFS_connected(s_node=key)):
            self.connected = False
            return False

      self.connected = True
      return True

   def is_cyclic(self) -> bool:
      """Returns if a graph is cyclic."""
      if not(self.BFS_cycle()):
         return False

      return True


   def DFS(self,v,directed=False,visited=None,path=None) -> list:
      """Does a Depth First Search to find the longest directed or undirected path in a graph.
      
      Each search begins at the specified node id 'v'.
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
      """Returns the longest directed or undirected path in connected or non-connected graph."""
      paths = self.findAllPaths(directed=directed,connected=connected)
      max_len   = max(len(p) for p in paths)
      max_paths = [p for p in paths if len(p) == max_len]

      return {"max_paths":max_paths,"length":max_len}

   def findAllPaths(self,directed=True,connected=True) -> list:
      """Returns the longest connected or undirected paths in a connected or non-connected graph."""
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
      """Returns all edges that a subgraph shares with a graph."""
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
      """Returns a list of adjacent nodes"""
      node = self.nodes[node_id]
      return node.get_neighbours(True) + node.get_neighbours(False)

   def as_dict(self) -> dict:
      """Returns the graph in a dictionary format.   
      Created with the intention of sending modified graph objects to the front-end that are easier to present using the javascript D3 library"""

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
   """
   The GraphManipulator class serves as a controller for the all graphs loaded via the API.
   """
   from errors import GraphNotFoundError,NodeNotFoundError, GraphComparisonError, GraphParseError, GraphAlreadyExists, GraphsNotFound,GraphIdNotInteger,NoNodeLabelsSupplied
   import json
   def __init__(self):
      self.Graphs = {}

   def clear(self):
      """Creates a clear dictionary for graph objects."""
      self.Graphs = {}

   def addGraph(self,graph) -> dict:
      """Adds a graph to the GraphManipulators Graph dictionary."""
      
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



   def getGraph(self,graph_id:int) -> Graph:
      """Returns a graph object corresponding to a graph_id"""
      
      if not isinstance(graph_id, int):
         if graph_id.isnumeric():
            graph_id = int(graph_id)
         else:
            raise self.GraphIdNotInteger(graph_id)

      graph = self.Graphs.get(graph_id,None)
      if graph is not None:
         return graph

      raise self.GraphNotFoundError(f"graph_id {graph_id} does not exist.") 

   def delGraph(self,graph_id:int) -> bool:
      """Function to delete a graph specified by graph_id. Returns a boolean indicating success."""
      if graph_id in self.Graphs:
         del self.Graphs[graph_id]
         return True

      return False

   def getGraphs(self,graph_id_list:list) -> tuple:
      """Returns a collection of graph objects from a list of ids. """
      
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

   def getGraphsByPage(self, page_no:int,graphs_per_page=5) -> dict:
      """Function to determine which graphs are to be displayed per page."""
      
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
      
   def compare(self,graph_id_1:str,graph_id_2:str) -> dict:
      """Method to compare 2 graphs and return all similarities and differences in dictionary format."""

      graph_1 = self.getGraph(graph_id_1)
      graph_2 = self.getGraph(graph_id_2)

      result = graph_1.compare(graph_2)

      if not(result):
         raise self.GraphComparisonError(f"Attempting to compare graphs with differing sentences.")

      return result

   def getNodeNeighbours(self,graph_id:int,node_id:int) -> dict:
      """Function to get a given nodes neighbours from a specified graph"""
      graph = self.getGraph(graph_id)

      node = graph.getNode(node_id)

      if node is None:
         raise self.NodeNotFoundError

      return node.get_neighbours(as_json=True)


   def getGraphsByNode(self,node_labels:list) -> dict:
      """Returns a list of graphs that contain a list of node labels."""
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


   def checkProperties(self, graph_id:int)-> dict:
      """Returns the properties for a specified graph of id 'graph_id'."""

      graph = self.getGraph(graph_id)

      return {
         "id" : str(graph_id),
         "connected" : str(self.is_connected(graph)), 
         "acyclic" : str(self.is_cyclic(graph)), 
         "longest_directed_path" : (self.longest_path(graph)),
         "longest_undirected_path" : (self.longest_path(graph,directed=False))}
      
   def checkSubgraph(self,json_subgraph:dict) -> dict:
      """Function to find all graphs that contain a specified subgraph pattern.
      
      A dictionary of edge lists with a graph's id as the key is returned."""

      graph_dict = {}

      for graph_id in self.Graphs:
         edge_list = self.Graphs[graph_id].subgraph_search(json_subgraph)
         if edge_list:
            graph_dict[graph_id] = edge_list
      
      if not graph_dict:
         raise self.GraphNotFoundError("No graphs found with matching subgraph.")

      return graph_dict

   def is_cyclic(self, graph:Graph) -> bool:
      """Function to determine whether a given graph, specified by 'graph', contains a cycle."""
      return graph.is_cyclic()

   def longest_path(self, graph:Graph, directed=True)->list:
      """Returns all the longest directed or undirected paths in a graph object"""
      return graph.findLongestPath(directed=directed,connected=graph.connected)

   def is_connected(self,graph:Graph) -> bool:
      """Function to determine whether a given graph, specified by 'graph', is connected."""
      return graph.is_connected()

   def __len__(self):
      return len(self.Graphs.keys())