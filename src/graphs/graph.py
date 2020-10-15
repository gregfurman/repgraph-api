from errors import *
from .node import Node
from .edge import Edge
from .token import Token


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

   def __init__(self,graph_input):
      self.sentence = graph_input['input']
      try:
         self.id = int(graph_input['id'])
      except ValueError as e:
         raise GraphIdNotInteger(graph_input['id'])

      self.tokens = {token['index']: Token(token_input=token) for token in graph_input['tokens']}
      self.nodes = {node['id']: Node(node_input=node,tokens=self.tokens) for node in graph_input['nodes']}

      self.edges = dict()

      for edge in graph_input['edges']:
         key = f"{self.nodes[edge['source']].label}--{edge['label']}/{edge['post-label']}--{self.nodes[edge['target']].label}"
         self.edges.setdefault(key, []).append(Edge(self.nodes[edge['source']],self.nodes[edge['target']],edge['label'],edge['post-label'])) 

      if sum([len(edges) for edges in self.edges.values()]) != len(graph_input['edges']):
         raise GraphError(f"Expected {len(graph_input['edges'])} edges but found {sum([len(edges) for edges in self.edges.values()])}.")

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

      graph_1_nodes = {node.label for node in self.nodes.values()}
      graph_2_nodes = {node.label for node in other.nodes.values()}

      matching_nodes = list(graph_1_nodes & graph_2_nodes)
      excl_graph_1_nodes = list(graph_1_nodes - graph_2_nodes)
      excl_graph_2_nodes = list(graph_2_nodes - graph_1_nodes)

      result["matching"] = self.graphs_to_lists(list(matching_edges),matching_nodes)
      
      result["graph_1"] = {str(self.id) : self.graphs_to_lists(list(self.edges.keys() & different_edges),excl_graph_1_nodes)}
      result["graph_2"] = {str(other.id) : other.graphs_to_lists(list(other.edges.keys() & different_edges),excl_graph_2_nodes)}

      return result

   def graphs_to_lists(self,edge_keys,nodes):
      """Converts a list of edge keys to a dictonary of edges. """
      edges = [edge.as_dict(label_as_id=True) for key in edge_keys for edge in self.edges[key]]
      # edges = [self.edges[edge].as_dict(label_as_id=True) for edge in self.edges[key] for key in edge_keys]
      return {"edges" : edges, "nodes" : nodes}

   

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
      node_ids = [node.label for node in self.nodes.values() if node.label in labels]
      if set(node_ids) == set(labels):
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
               paths.append((t_path))
               paths.extend(self.DFS(t,directed, visited[:], t_path))
         
      return paths

   def path_to_graph(self,node_ids:list,directed=True) -> dict:
      """ Takes a path of node ids and converts it to an edge list.
      
      :param node_ids: The id of nodes in order of traversal.
      :type node_id: list
      :param directed: indicated whether the path being parsed is directed or undirected (default is True).
      :type directed: bool
      :returns: A dictionary of edges that have been converted to dictionary format.
      :rtype: dict
      """
      edges = [self.nodes[node_ids[i]].get_neighbour_by_node(node_ids[i+1],directed=directed).as_dict(label_as_id=True) for i in range(len(node_ids)-1)]
      
      if not directed:

         for index in range(len(edges)-1):
            if edges[index]["trg"] != edges[index+1]["src"]:
               if edges[index]["src"] == edges[index+1]["src"]:
                  edges[index]["trg"],edges[index]["src"] = edges[index]["src"],edges[index]["trg"]
               else:
                  edges[index+1]["trg"],edges[index+1]["src"] = edges[index+1]["src"],edges[index+1]["trg"]
               
      return {"edges" : edges}

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

      return {str(path): self.path_to_graph(list(path),directed=directed) for path in max_paths}
      


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


   def subgraph_search(self,subgraph:list) -> dict:
      """Returns all edges that a subgraph shares with a graph.
      
      :param subgraph: The subgraph that will be searched for within the graph.
      :type subgraph: list
      :returns: dictionary of matching connections if the subgraph exists else an empty dictionary is returned.
      :rtype: dict
      """
      import re

      wildcard_edges = []
      subgraph_edges = set()

      for link in subgraph:

         link[1]= link[1].upper()
         link[2]= link[2].upper()

         if "*" in link:
            wildcard_edges.append([e for e in link if "*" not in e])
         else:
            subgraph_edges.add("%s--%s/%s--%s" % tuple(link))

      matches = self.edges.keys() & subgraph_edges

      if len(matches) != len(subgraph_edges):
         return {}
      elif wildcard_edges:
         matches = matches.union({edge for edge in self.edges.keys() if len(wildcard_edges) == len([wc for wc in wildcard_edges if wc in re.split("--|/",edge)])})

      return {"links" : [edges.as_dict() for key in matches for edges in self.edges[key]]}


   def adj_nodes(self,node_id:int) -> list:
      """Function to return a list of nodes that are adjacent to a specified node of id 'node_id'.
      
      :param node_id: The node id whose neighbours are attempting to be returned.
      :type node_id: int
      :returns: a list of adjacent nodes.
      :rtype: list
      """
      node = self.nodes[node_id]
      return node.get_neighbours(True) + node.get_neighbours(False)

   def merge_edge_labels(self,edges) -> dict:
      """
      :returns: dictionary of edge labels where 2 nodes having 'n' connections are represented as having a label = '[label_1] || [label_2] || ... || [label_n]'
      :rtype: dict
      """
      edges_dict = {}
      
      if isinstance(edges,dict):
         edges = edges.values()

      for edge in edges:
         key = f"{edge.get_src().label}/{edge.get_src().id}-{edge.get_trg().label}/{edge.get_trg().id}"

         if key not in edges_dict:
            edges_dict[key] = edge.as_dict()   
         else:
            edges_dict[key]['label'] += f" || { edge.as_dict()['label']}"

      return list(edges_dict.values())


   def from_subgraph(self,subgraph:dict):
      """Adds in all nodes tokens for subgraph and merges edge labels where a node A has 2 or more connections to a node B.
      
      :param subgraph: dictionary of subgraph.
      :type subgraph: dict
      """
      subgraph["edges"] = self.merge_edge_labels(edges=subgraph["edges"])
      subgraph["tokens"] = {key: self.tokens[key].as_dict() for key in self.tokens.keys() & subgraph["tokens"]}


   def planarity_check(self):
      """Checks whether a graph is planar.
      
      :returns: a boolean indicating whether a graph is planar.
      :rtype: bool
      """ 
      sorted_nodes = {k: v for k,v in sorted(self.nodes.items(), key= lambda item:item[1].min_token())}

      edges = []

      for edge in [edge for edges in self.edges.values() for edge in edges]:
         edges.append(Edge(sorted_nodes[edge.get_src().id],sorted_nodes[edge.get_trg().id],edge.pre_label,edge.post_label,add_edge=False))

      for i in range(len(edges)):
         edge = edges[i]
         for j in range(i+1,len(edges)):
            other = edges[j]
            if min(edge.get_src().min_token(),edge.get_trg().min_token()) < min(other.get_src().min_token(),other.get_trg().min_token()) and min(other.get_src().min_token(),other.get_trg().min_token()) < max(edge.get_src().max_token(),edge.get_trg().max_token()) and max(edge.get_src().max_token(),edge.get_trg().max_token()) < max(other.get_src().max_token(),other.get_trg().max_token()):
               return False
            
      return True


   def sentence_search(self,sentence:str)->bool:
      """Determines whether a given input string is in a graph's sentence.

      :param sentence: the sub-sentence that is being searched for in a graphs sentence.
      :type sentence: str
      :returns: boolean indicating whether a string is in a sentence.
      :rtype: bool
      """
      
      sentence = ' '.join(sentence.split())
      sub_sentence =   ''.join(x for x in sentence.strip() if x.isalnum() or x==' ').lower().split(" ")
      targ_sentence = ''.join(x for x in self.sentence.strip() if x.isalnum() or x==' ').lower().split(" ")
      
      if sub_sentence == [""]:
         return False
      elif sub_sentence == targ_sentence:
         return True
      elif len(sub_sentence) > len(targ_sentence):
         return False

      for index in range(len(targ_sentence)-len(sub_sentence)):
         window = targ_sentence[index:len(sub_sentence)+index]

         if window == sub_sentence:
            return True

      return False


   def as_dict(self) -> dict:
      """Function that returns a Graph object in dictionary format. Created with the intention of sending modified graph objects to the front-end that are easier to present using the javascript D3 library.
      
      :returns: the graph in a dictionary format.
      :rtype: dict   
      """

      graph_dict = {}

      graph_dict["id"] = str(self.id)
      graph_dict["a_nodes"] = {str(node): self.nodes[node].as_dict() for node in self.nodes if not(self.nodes[node].is_surface())}
      graph_dict["s_nodes"] = {str(node): self.nodes[node].as_dict() for node in self.nodes if self.nodes[node].is_surface()}
      graph_dict["edges"] = self.merge_edge_labels([edge for edges in self.edges.values() for edge in edges])
      graph_dict["tokens"] = {str(token): self.tokens[token].as_dict() for token in self.tokens.keys()}
      graph_dict["tops"] = {str(self.top.id) : self.top.as_dict()}
      graph_dict["sentence"] = [token.form for token in self.tokens.values()]

      return graph_dict
