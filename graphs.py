from collections import Counter

class Node:
   def __init__(self,node_input,tokens):
      self.id = node_input['id']
      self.label = node_input['label']
      self.incomingEdges = []
      self.outgoingEdges = []
      self.anchors = {token_id: tokens[token_id] for token_id in range(node_input['anchors'][0]["from"],node_input['anchors'][0]["end"])}

   def __eq__(self, other):
      return other.id == self.id

   def __ne__(self, other):
      return not(other.id == self.id)

   def __str__(self):
      return f"ID: {self.id}\nLabel: {self.label}\nIncoming edges: {self.incomingEdges}\nOutgoing Edges: {self.outgoingEdges}\nAnchored: {list(self.anchors.values())}"

   def __cmp__(self,other):
      if self.id > other.id:
         return 1
      elif self.id < other.id:
         return -1
      
      return 0

   def add_edge(self,edge):
      if (self == edge.node_source):
         self.outgoingEdges.append(edge)
      elif(self == edge.node_target):
         self.incomingEdges.append(edge)
      else:
         raise Exception("Error adding edges") #error message or try catch
      

class Edge:
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

   def __repr__(self):
      return f"src: {self.node_source.id} -{self.label}/{self.post_label}-> trg: {self.node_target.id}"


class Token:
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
   def __init__(self,graph_input):
      self.sentence = graph_input['input']

      self.tokens = {token['index']: Token(token_input=token) for token in graph_input['tokens']}
      self.nodes = {node['id']: Node(node_input=node,tokens=self.tokens) for node in graph_input['nodes']}
      self.edges = [Edge(self.nodes[edge['source']],self.nodes[edge['target']],edge['label'],edge['post-label']) for edge in graph_input['edges']]
      self.json_input = graph_input
      self.top = self.nodes[graph_input['tops'][0]]

   def display(self):
      [print(node) for node in self.nodes.values()]

   def as_adjacency_list(self,transpose=False,directed=True):
      
      if directed:

         if transpose:      
            adj_list = {node.id: [edge.get_trg().id for edge in node.outgoingEdges] for node in self.nodes.values()}
         else:
            adj_list = {node.id: [edge.get_src().id for edge in node.incomingEdges] for node in self.nodes.values()}
      else:
         
         adj_list = {node.id: [edge.get_src().id for edge in node.incomingEdges] for node in self.nodes.values()}
         adj_list_T = {node.id: [edge.get_trg().id for edge in node.outgoingEdges] for node in self.nodes.values()}

         for key in adj_list.keys():
            adj_list[key].extend(adj_list_T[key])

      return adj_list


   def BFS(self, s, graph):    

      visited = [False] * (len(graph)) 
      queue = [] 
      queue.extend(graph[s]) 
      visited[s] = True

      while queue: 

         s = queue.pop(0) 

         for i in graph[s]: 
               if visited[i] == False: 
                  queue.append(i) 
                  visited[i] = True

      return visited.count(True) == len(visited)

   def is_connected(self):

      # visited_list = self.BFS(self.top) == [not i for i in self.BFS(self.top,True)]
      adj_list = self.as_adjacency_list()
      adj_list_T = self.as_adjacency_list(transpose=True)

      for key in adj_list.keys():
         if not(self.BFS(key,adj_list) and self.BFS(key,adj_list_T)):
            return False

      return True


   def DFS(self,G,v,seen=None,path=None):
      if seen is None: seen = []
      if path is None: path = [v]

      seen.append(v)

      paths = []
      for t in G[v]:
         if t not in seen:
               t_path = path + [t]
               paths.append(tuple(t_path))
               paths.extend(self.DFS(G, t, seen[:], t_path))
      return paths

   def findLongestPath(self,directed=True):

      paths = self.DFS(self.as_adjacency_list(directed=directed),1)

      max_len   = max(len(p) for p in paths)
      max_paths = [list(p) for p in paths if len(p) == max_len]

      return {"max_paths":max_paths,"length":max_len}

