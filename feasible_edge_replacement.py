from sympy.combinatorics.permutations import Permutation
import networkx as nx

class Feasible_edge_replacement:
  '''
  A sequence of Feasable Edge Replacements perm_seq::(permutation : old_edge -> new_edge)...()
  Can be concatenated with *, hashed, iterated, printed, and added individual replacements.
  '''
  class Individual_Fer:
    def __init__(self, old_edge, new_edge):
      self.old_edge = old_edge
      self.new_edge = new_edge

    def tex(self):
      if self.old_edge == self.new_edge:
        return '(\\emptyset \\to \\emptyset)'
      i, j = self.old_edge
      x, y = self.new_edge
      return f"({i}\\ {j} \\to {x}\\ {y})"

    def __add__(self, other):
      i, j = self.old_edge
      x, y = self.new_edge
      return Feasible_edge_replacement.Individual_Fer({i + other, j + other}, {x + other, y + other})

    def __str__(self):
      if self.old_edge == self.new_edge:
        return '(0 -> 0)'
      i, j = self.old_edge
      x, y = self.new_edge
      
      return f"({i} {j} -> {x} {y})"

    def update(self, permutation):
      '''
      Updates the labels of the edge replacement according to the given permutation.
      The intended use is when multiplying with a sequence on the left. Can also use
      conjugation with inverse, but this seems a little faster, since we only need
      to invert once (and conjugation would compute three inverses).
      '''
      old_i, old_j = self.old_edge
      old_x, old_y = self.new_edge

      # Make sure Permutation is the right size:
      m = max([old_i, old_j, old_x, old_y])
      permutation = Permutation(m)*permutation**(-1)

      # Update new values after permuting.
      p_list = permutation.list()

      new_i = p_list[old_i]
      new_j = p_list[old_j]
      new_x = p_list[old_x]
      new_y = p_list[old_y]
      return Feasible_edge_replacement.Individual_Fer({new_i, new_j}, {new_x, new_y})

  def __init__(self, old_edge=None, new_edge=None, permutation=None, sequence=None):
    if sequence:
      self.sequence = sequence
      self.seq_perm = permutation
    else:
      ind_fer_to_add = self.Individual_Fer(old_edge, new_edge)
      self.sequence = [ind_fer_to_add]
      self.seq_perm = permutation

  def __add__(self, other):
    new_seq = [fer + other for fer in self.sequence]
    old_per = self.seq_perm
    new_siz = old_per.size + other
    conj    = Permutation([im%new_siz for im in range(other, new_siz + other)])
    new_per = (Permutation(old_per, size=new_siz))^conj

    return Feasible_edge_replacement(permutation=new_per, sequence=new_seq)

  def tex(self):
    if not self.sequence:
      return '[]'
    string = ''
    for ind_fer in self.sequence:
      string = string + ind_fer.tex()
    return string

  def __str__(self):
    if not self.sequence:
      return '[]'
    string = ''
    for ind_fer in self.sequence:
      string = string + str(ind_fer)
    return str(self.seq_perm)+'::'+string

  def __len__(self):
    return len(self.sequence)

  def simplify(self):
    new_seq = [fer for fer in self.sequence]
    for i in range(len(new_seq)):
      # Don't add fers that cancel out.
      if i+1 < len(new_seq) and new_seq[i].new_edge == new_seq[i+1].old_edge and new_seq[i].old_edge == new_seq[i+1].new_edge:
        new_seq.pop(i)
        new_seq.pop(i)
      if i+1 < len(new_seq) and new_seq[i].new_edge == new_seq[i+1].old_edge:   # (e->f)(f->g)=(e->g)
        left_old  = new_seq[i].old_edge
        right_new = new_seq[i+1].new_edge
        new_seq.pop(i)
        new_seq.pop(i)
        new_seq.insert(i, self.Individual_Fer(left_old, right_new))
      if i+1 < len(new_seq) and new_seq[i].old_edge == new_seq[i+1].new_edge: # (f->g)(e->f)=(e->g)
        left_new  = new_seq[i].new_edge
        right_old = new_seq[i+1].old_edge
        new_seq.pop(i)
        new_seq.pop(i)
        new_seq.insert(i, self.Individual_Fer(right_old, left_new))
    
    # Trivial edge replacement doesn't get added.
    new_seq = [fer for fer in new_seq if fer.old_edge != fer.new_edge]

    if not new_seq:
      new_seq = [self.Individual_Fer({0,1}, {0,1})]
    return Feasible_edge_replacement(old_edge=None, new_edge=None, permutation=self.seq_perm, sequence=new_seq)

  def __mul__(self, other):
    left_perm  = self.seq_perm
    right_perm = other.seq_perm
    left_seq   = self.sequence
    right_seq  = [fer.update(left_perm) for fer in other.sequence]
    new_fer = Feasible_edge_replacement(old_edge=None, new_edge=None, permutation=left_perm*right_perm, sequence=left_seq+right_seq)
    new_fer = new_fer.simplify()
    return new_fer

  def __getitem__(self, index):
    return self.sequence[index]

  def __iter__(self):
    return iter(self.sequence)

  def is_of(self, graph): # Decides if fer is a fer of a graph.
    mapping = {}
    g_nodes = graph.nodes()
    m = max(g_nodes)
    perm = Permutation(m)*self.seq_perm**(-1)
    for node in g_nodes:
      mapping[node] = perm.list()[node]
    perm_G = nx.relabel_nodes(graph, mapping)
    perm_edges = set()
    for edge in perm_G.edges():
      i, j = edge
      if i < j:
        perm_edges.add((i,j))
      else:
        perm_edges.add((j,i))

    ferd_G = graph.copy()
    for fer in self.sequence:
      ferd_G.remove_edge(*fer.old_edge)
      ferd_G.add_edge(*fer.new_edge)

    ferd_edges = set()
    for edge in ferd_G.edges():
      i, j = edge
      if i < j:
        ferd_edges.add((i,j))
      else:
        ferd_edges.add((j,i))
    
    return ferd_edges == perm_edges

 # ================== OBSOLETE CODE ==================

  '''
  def print_all(self):
    if self.sequence:
      perm = str(self.seq_perm)
      string = ''
      for ind_fer in self.sequence:
        string = string + ind_fer.print_all()
      print(perm + '::' + string)
    else:
      print('()')

  def add(self, old_edge, new_edge, permutation=None):
    ind_fer_to_add = self.Individual_Fer(old_edge, new_edge, permutation)
    if self.sequence:
      # Update self.seq_perm to new sequence permutation.
      old_seq_perm = self.seq_perm
      self.seq_perm = self.seq_perm*permutation
      # Conjugate fer to be added to update labels.
      ind_fer_to_add.update(old_seq_perm)

      # Simplification rules:
      # Trivial edge replacement doesn't get added. NOTE: the labels were updated above.
      last_fer = self.sequence[-1]
      if ind_fer_to_add.old_edge == ind_fer_to_add.new_edge:
        return
      
      # Consecutive replacements that cancel each other get both removed. (e->f)(f->e)=?
      elif last_fer.new_edge == ind_fer_to_add.old_edge and
           last_fer.old_edge == ind_fer_to_add.new_edge:
        self.sequence.pop()
        return
      
      # Consecutive replacements that share an edge get conflated.
      if last_fer.new_edge == ind_fer_to_add.old_edge: # (e->f)(f->g)=(e->g)
        self.sequence[-1].new_edge = ind_fer_to_add.new_edge
        return
      elif last_fer.old_edge == ind_fer_to_add.new_edge: # (f->g)(e->f)=(e->g)
        self.sequence[-1].old_edge = ind_fer_to_add.old_edge
        return

    self.seq_perm = self.seq_perm*permutation
    self.sequence.append(ind_fer_to_add)

  def _add(self, old_edge, new_edge, permutation=None):
    ind_fer_to_add = self.Individual_Fer(old_edge, new_edge, permutation)
    if self.sequence:
      # We update the new edge replacement, according to the sequence's permutation.
      old_seq_perm = self.seq_perm 
      ind_fer_to_add.permute(old_seq_perm)

      # Update the sequence's permutation.
      self.seq_perm = old_seq_perm*permutation
      last_added_fer = self.sequence[-1]

      # If edge concatenation is simplifiable:
      if last_added_fer.new_edge == ind_fer_to_add.old_edge:
        replace_with = self.Individual_Fer(
            old_edge=last_added_fer.old_edge,
            new_edge=ind_fer_to_add.new_edge,
            permutation=permutation)
        self.sequence[-1] = replace_with
      elif last_added_fer.old_edge == ind_fer_to_add.new_edge:
        replace_with = self.Individual_Fer(
            old_edge=ind_fer_to_add.old_edge,
            new_edge=last_added_fer.new_edge,
            permutation=permutation)
        self.sequence[-1] = replace_with
      else:
        self.sequence.append(ind_fer_to_add)

    else:
      self.sequence.append(ind_fer_to_add)
      self.seq_perm = permutation
  '''