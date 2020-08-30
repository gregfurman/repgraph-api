class Node:

   """
   The Node class holds a node's id, label, a list of incoming and outgoing Edge objects and a list of Token objects with which it is anchored to. 
   """

   def __init__(self,node_input,tokens):
      self.id = node_input['id']
      self.label = node_input['label']
      self.incomingEdges = []
      self.outgoingEdges = []
      self.anchors = {token_id: tokens[token_id] for token_id in range(node_input['anchors'][0]["from"],node_input['anchors'][0]["end"]+1)}

   def __eq__(self, other):
      return other.label == self.label

   def __ne__(self, other):
      return not(other.label == self.label)

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
   def __init__(self,node_src,node_trg,label,post_label):
      self.node_source = node_src
      self.node_target = node_trg
      self.label = label
      self.post_label = post_label

      node_src.add_edge(self)
      node_trg.add_edge(self)


   def get_trg(self):
      return self.node_target

   def get_src(self):
      return self.node_source

   def get_nodes(self):
      return {"src":self.get_src().id, "labels": f"{self.label}/{self.post_label}", "trg" : self.get_trg().id}

   def __repr__(self):
      return f"src: {self.node_source.id} -{self.label}/{self.post_label}-> trg: {self.node_target.id}"

   def __eq__(self,other):
      return self.node_target.compare_labels(other.node_target) and self.node_source.compare_labels(other.node_source) and (f"{self.label}/{self.post_label}"==f"{other.label}/{other.post_label}")


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

   def __repr__(self):
      if self.form != self.lemma:
         return f"[Form: {self.form} -> Lemma: {self.lemma}]"

      return f"[Form: {self.form}]"

class Graph:
   """
   A Graph object keeps a list of all the Nodes, Edges, Tokens, the original sentence being parsed and a single variable for a top node.
   There are multiple functions within the Graph class that allow for checking formal graph properties and longest directional & non-directional paths. 
   """
   def __init__(self,graph_input):
      self.sentence = graph_input['input']

      self.id = graph_input['id']

      self.tokens = {token['index']: Token(token_input=token) for token in graph_input['tokens']}
      self.nodes = {node['id']: Node(node_input=node,tokens=self.tokens) for node in graph_input['nodes']}
      self.edges = [Edge(self.nodes[edge['source']],self.nodes[edge['target']],edge['label'],edge['post-label']) for edge in graph_input['edges']]
      self.json_input = graph_input
      self.top = self.nodes[graph_input['tops'][0]]

   def display(self):
      [print(node) for node in self.nodes.values()]

   def getNode(self,node_id):
      return self.nodes[node_id]

   def getNodes(self):
      return list(self.nodes.values)

   def has_labels(self,labels):
      return set(labels).issubset(set([node.label for node in self.nodes.values()]))
   
   def __str__(self):
       return " ".join([str(node) for node in self.nodes.values()])


   def BFS_cycle(self,transpose=False):

     
      if transpose:
         nodes = {node.id: len(node.outgoingEdges) for node in self.nodes.values()}
      else:
         nodes = {node.id: len(node.incomingEdges) for node in self.nodes.values()}
      queue = [key for key in nodes.keys() if nodes[key] ==0]


      visited = 0

      while queue:

         s = queue.pop(0)

         visited += 1

         for node_id in self.nodes[s].get_neighbours(incoming=transpose):
            nodes[node_id] -= 1
            if (nodes[node_id] == 0):
               queue.append(node_id)

      
      return len(nodes.keys()) == visited

   def BFS_connected(self,s_node):
      visited = [False]*len(self.nodes)
      queue = [s_node]

      while queue:

         s = queue.pop(0)

         for node_id in self.nodes[s].get_neighbours(incoming=False) + self.nodes[s].get_neighbours(incoming=True):
            if visited[node_id] == False:
               queue.append(node_id)
               visited[node_id]=True
            
      return visited.count(visited[0]) == len(visited)



   def is_connected(self):

      for key in self.nodes.keys():
         if not(self.BFS_connected(s_node=key)):
            return False
            
      return True

   def is_cyclic(self):

      if not(self.BFS_cycle()):
         return False

      return True


   def DFS(self,v,directed=False,visited=None,path=None):
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


   def findLongestPath(self,directed=True):

      paths = self.findAllPaths(directed=directed)
      max_len   = max(len(p) for p in paths)
      max_paths = [p for p in paths if len(p) == max_len]

      return {"max_paths":max_paths,"length":max_len}

   def findAllPaths(self,directed=True):

      paths = []

      if (directed):
         for i in range(len(self.nodes)):
            paths.extend(self.DFS(i,directed=True))

      else:
         paths= self.DFS(0)

      return paths


   def subgraph_search(self,subgraph):

      edges = []
      for edge in self.edges:
         for subgraph_edge in subgraph.edges[3:5]:
            if (subgraph_edge==edge):
               edges.append(edge)


      if len(edges) > 1:
         return True, edges

      return False

   def adj_nodes(self,node_id):

      node = self.nodes[node_id]
      return node.get_neighbours(True) + node.get_neighbours(False) #remove node_id from get_nodes

class GraphManipulator:
   """
   The GraphManipulator class serves as a controller for the all graphs loaded via the API.
   """
   def __init__(self):
      self.Graphs = {}

   def addGraph(self,graph_input):
      self.Graphs[graph_input['id']] = Graph(graph_input)

   def getGraph(self,graph_id):
      return self.Graphs.get(graph_id,None)

   def getNodeNeighbours(self,graph_id,node_id):
      graph = self.getGraph(graph_id)

      if graph is not None:
         return graph.getNode(int(node_id)).get_neighbours(as_json=True)
      
      return '{"error":"graph id does not exist"}'

   def getGraphs(self,node_labels):
         return [graph for graph in self.Graphs.keys() if self.Graphs[graph].has_labels(node_labels)]

   def is_cyclic(self, graph_id):
      return self.Graphs[graph_id].is_cyclic()

   def longest_path(self, graph_id, directed=False):
      return self.Graphs[graph_id].findLongestPath()

   def is_connected(self,graph_id):
      return self.Graphs[graph_id].is_connected()