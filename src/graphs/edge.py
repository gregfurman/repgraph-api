from errors import *
from .node import Node

class Edge:

   """
   The Edge class is a directional connection between 2 nodes, having a node source (node_src) and node target (node target). 
   Each Edge also has a label and post-label.
   
   :var node_source: The source node from which an edge originates.
   :type node_source: Node
   :var node_target: The target node that is connected from the source node via an edge.
   :type node_target: Node
   :var label: An edge relationship consisting of a label and a post-label (in the format '[label]/[post-label]').
   :type label: Node
   :param node_src: The input source node.
   :type node_src: Node
   :param node_trg: The input target node.
   :type node_trg: Node
   :param label: The input edge label.
   :type label: str
   :param post_label: The input edge post_label.
   :type post_label: str
   :param add_edge: determines whether an edge will be added to a node's incoming or outgoing edge list (default is True).
   :type add_edge: bool
   """
   def __init__(self,node_src,node_trg,label,post_label,add_edge=True):
      self.node_source = node_src
      self.node_target = node_trg
      self.label = f"{label}/{post_label}"

      self.pre_label = label
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

   def get_label(self):
      return f"{self.node_source.label}-{self.label}-{self.node_target.label}"

   def as_dict(self,label_as_id=False) -> dict:
      """Function that returns an edge's labels and target & source nodes in dictionary format.
      :returns: an edge object represented as a dictionary.
      :rtype: dict:
      """
      edge_dict = {}

      if label_as_id:
         if self.node_source:
            edge_dict["src"] = self.node_source.label

         if self.node_target:
            edge_dict["trg"] = self.node_target.label
      else:
         if self.node_source:
            edge_dict["src"] = self.node_source.id

         if self.node_target:
            edge_dict["trg"] = self.node_target.id

      edge_dict["label"] = self.label 

      return edge_dict

   def __repr__(self):
      return f"src: {self.node_source.label} -{self.label}-> trg: {self.node_target.label}"

   def __str__(self):
      return f"src: {self.node_source.label} -{self.label}-> trg: {self.node_target.label}"

   def __eq__(self,other):
      return self.node_target.label == other.node_target.label and self.node_source.label == other.node_source.label and self.label == other.label

   def __hash__(self):
      return self.get_label()
