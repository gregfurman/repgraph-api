class Token:
   """A Token object has an index, form, lemma and an optional carg.

   :var index: The index of the token.
   :type index: int
   :var form: The original representation of a word.
   :type form: str
   :var lemma: The normalised form of a word.
   :type lemma: str
   :var carg: for named entities i.e numbers, abbreviations, proper nouns.
   :type carg: int
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
