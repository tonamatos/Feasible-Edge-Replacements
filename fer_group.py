import Feasible_edge_replacement as Fer
from math import factorial

class FerGroup:
  '''
  Given a NetworkX colored_graph, it will generate the group of Fer objects as a generator object.
  It includes information that helps decide if the input is a colored amoeba or not.
  '''
  def __init__(self, colored_graph):
    self.fers      = {}   # Set of all Fer objects.
    self._order    = None # Order of group. None=unknown.
    self._isAmoeba = None # If it is a colored amoeba or not. None=unknown.

    # Count how many vertices of each color, and count the maximum possible size of a FerGroup: n1!n2!...nk!
    color_counts = {}
    for node, data in G.nodes(data=True):
      color = data.get('color')
      if color in color_counts:
        color_counts[color] += 1
      else:
        color_counts[color] = 1

    full_group = 1
    for color, count in color_counts.items():
      full_group *= factorial(count)
    self.color_count = full_group

  def __str__(self):
    table = 'Order = '+str(self._order)+'\tIs Amoeba='+str(self._isAmoeba)+'\t\n\n'
    for fer in self.fers:
      # per, seq = fer.seq_perm, fer.sequence
      table = table+str(fer)+'\t\n'
    return table

  def _find_new(self):
    '''
    If possible (self.fers has fewer than color_count), tries to find a new Fer object not
    already in self.fers. If it finds one, it gets outputted, else is returns None.
    '''
    



  def generate(self):


  def order(self):
    if not self._order is None:
      return self._order
    else:
      len(list(self.generate()))

  def isAmoeba(self):
    if self._isAmoeba is None:
      self._isAmoeba = self.order() == self.color_count
    return self._isAmoeba
    