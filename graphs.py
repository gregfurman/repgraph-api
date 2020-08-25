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

   def add_edge(self,edge):
      if (self == edge.node_source):
         self.outgoingEdges.append(edge)
      elif(self != edge.node_source):
         self.incomingEdges.append(edge)
      else:
         raise Exception("Error adding edges")
      

class Edge:
   def __init__(self,node_src,node_trg,label,post_label):
      self.node_source = node_src
      self.node_target = node_trg
      self.label = label
      self.post_label = post_label

      node_src.add_edge(self)
      node_trg.add_edge(self)


   def __repr__(self):
      return f"src: {self.node_source.id} -{self.label}/{self.post_label}-> trg: {self.node_target.id}"


class Token:
   def __init__(self,token_input):
      self.index = token_input['index']
      self.form = token_input['form']
      self.lemma = token_input['lemma']

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

      # self.edges = [Edge(edge_input=edge)]
      self.json_input = graph_input

   def display(self):
      [print(node) for node in self.nodes.values()]