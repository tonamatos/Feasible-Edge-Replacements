# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 12:42:46 2023

@author: Tonatiuh
"""
from feasible_edge_replacement import Feasible_edge_replacement as Fer

import networkx as nx
from networkx.algorithms import isomorphism
from math import factorial
from time import time
from sympy.combinatorics.permutations import Permutation as Per
from sympy.combinatorics.perm_groups import PermutationGroup
import matplotlib.pyplot as plt
from itertools import product, combinations, permutations
#from functools import cache

# DECISION ALGORITHMS

def change_edge(g, e, ne):
  g1 = g.copy()
  g1.remove_edge(*e)
  g1.add_edge(*ne)
  return g1

def is_feasible_edge_replacement(g, e, ne):
  if nx.is_isomorphic(g, change_edge(g, e, ne), node_match=lambda x, y: x['color'] == y['color']):
    GM = isomorphism.GraphMatcher(g, change_edge(g, e, ne))
    return list(GM.subgraph_isomorphisms_iter())
  else:
    return False

def dict_to_perm(d):
  """Change a dict d to a list the_list so that d[i] becomes the same as the_list[i]"""
  the_list = []
  for i in range(len(d)):
    the_list.append(d[i])
  return the_list

def perms_all_feasible_edge_replacements(graph):
  n = graph.order()
  perms = []
  edges = graph.edges()
  nonedges = combinations(graph.nodes(), 2)
  nonedges = [(x, y) for (x, y) in nonedges if not (x, y) in edges and not (y, x) in edges]
  for e in edges:
    for ne in nonedges+[e]:
      isos = is_feasible_edge_replacement(graph, e, ne)
      if isos:
        perms.extend([Per(dict_to_perm(x)) for x in isos])
  return PermutationGroup(perms)

def isLocalColoredAmoeba(colored_graph):
  '''
  Given a networkX object colored_graph, decides if it is a local amoeba.
  colored_graph must have a vertex coloring of the form [1,...,k].
  '''
  print("Warning: algorithm implemented in brute force, extremely inefficient!")
  time0 = time()
  G = colored_graph.copy()
  for node in G.nodes():
    G.nodes[node]['label'] = G.nodes[node]['color']
  nf = factorial(G.order())
  count = perms_all_feasible_edge_replacements(G).order()
  print("Time taken:",time()-time0)
  return count == nf

# GENERATORS

def cayley_graph_maker(group, generators):
  cayley_graph = nx.DiGraph()

  # Add nodes and edges
  for g in group.generate():
    for s in generators:
      cayley_graph.add_edge(g, s*g, label=str(s))
  return cayley_graph

def cayley_graph_update(cayley_graph, group, more_generators):
  for g in group.generate():
    for s in more_generators:
      if not cayley_graph.has_edge(g, s*g):
        cayley_graph.add_edge(g, s*g)

def perms_factorization(perms, generators, update=False, draw=False):
  '''
  Given list of sympy.Permutation objects perms, factors them into generators,
  assuming these generate the full group. generators must have the same size!
  update allows the Cayley graph to add known generators, so these can be factored
  in order of 'perms', by plugging in the previously known factorizations!
  update=False will factor elements into the original generators.
  '''
  t0 = time()
  size = generators[0].size - 1

  # Close generators under inverses.
  #generators = generators + [a**(-1) for a in generators if a**(-1) not in generators]
  
  # Create Cayley graph and find shortest path
  cayley_graph = cayley_graph_maker(PermutationGroup(generators), generators)
  factorizations = {tuple(Per(size)) : [Per(size)]}
  
  if draw:
    fig, ax = plt.subplots()
    fig.set_size_inches(16, 14)
    pos = nx.circular_layout(cayley_graph)
    labels = nx.get_edge_attributes(cayley_graph, 'label')
    
    ax.set_title("Creating Cayley graph")
    nx.draw_networkx_nodes(cayley_graph, pos, node_color='teal')
    nx.draw_networkx_edges(cayley_graph, pos, edge_color='blue')
    nx.draw_networkx_labels(cayley_graph, pos)
    nx.draw_networkx_edge_labels(cayley_graph, pos, edge_labels=labels)
    plt.pause(1)

  for perm in perms:
    if perm == Per(size):
      continue
      
    path = nx.shortest_path(cayley_graph, Per(size), perm)
    # Get back the edges as generators
    genterms = [path[i+1] * path[i]**(-1) for i in range(len(path)-1)]
    genterms.reverse() # Reverse to multiply left-to-right
    
    factorizations[tuple(perm)] = genterms
    gent_printable = str()
    for term in genterms:
      gent_printable = gent_printable + str(term)
    
    if draw:
      ax.clear()
      ax.set_title(f"Factoring {perm} as {gent_printable}")
      nx.draw_networkx_nodes(cayley_graph, pos, node_color='teal')
      nx.draw_networkx_edges(cayley_graph, pos, edge_color='blue')
      path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
      nx.draw_networkx_nodes(cayley_graph, pos, nodelist=path, node_color='red')
      nx.draw_networkx_edges(cayley_graph, pos, edgelist=path_edges, edge_color='red', width=4)
      nx.draw_networkx_labels(cayley_graph, pos)
      nx.draw_networkx_edge_labels(cayley_graph, pos, edge_labels=labels)
      plt.pause(0.05)
        
    if update:
      cayley_graph_update(cayley_graph, PermutationGroup(generators), [perm, perm**(-1)])
  #print("Time to factor all permutations:",time()-t0)
  return(factorizations)

def perm_fact_into_trans(perm, y0):
  '''
  Given perm=Per(), returns l=[transpositions of the form (y0,a)
  where a in perm and whose product is perm]
  '''
  l = []
  for cycle in perm.cyclic_form:
    for x in cycle:
      if x != y0: l.append(Per(y0, x))
    last = cycle[0]
    if last != y0: l.append(Per(y0, last))
  return l

def fact_to_fer(fact, known_fers):
  '''
  Given fact=[p1,...,pn], fact_to_fer finds a Fer for p1*...*pn
  assuming the Fers for pi are all known in known_fers.
  '''
  fers = [known_fers[tuple(p)] for p in fact]
  sought_fer = fers[0]
  for i in range(len(fers)-1):
    sought_fer = sought_fer*fers[i+1]
  return sought_fer

def fer_verifier(graph, known_fers):
  '''
  Applies all known_fers to graph and checks if they are correct.
  Prints any wrong ones.

  '''
  t0 = time()
  how_many = len(known_fers)
  for perm, fer in known_fers.items():
    if not fer.is_of(graph):
      raise ValueError("Wrong fer found!",fer.seq_perm,':',str(fer))
  print(f"All {how_many} fers verified in time:",time()-t0)

def add_pairs_prod(hash_fers):
  '''
  Given a hash of fers, updates it with all pairs multiplied.
  '''
  tuples_of_perms = hash_fers.keys()
  for g, h in product(tuples_of_perms,repeat=2):
    fer_g  = hash_fers[g]
    fer_h  = hash_fers[h]
    fer_gh = fer_g*fer_h
    gh = tuple(fer_gh.seq_perm)
    if gh not in tuples_of_perms:
      hash_fers[gh] = fer_gh

def brute_force_populate(hash_gen, k):
  generators = [Per(per) for per in hash_gen.keys()]
  target = PermutationGroup(*generators).order()
  count = 0
  while count < target:
    add_pairs_prod(hash_gen)
    count = len(hash_gen.keys())
  hash_gen[tuple(Per(k))] = Fer({0,1}, {0,1}, Per(k))

def updating_Cayley_populate(hash_gen):
  '''
  Uses the modified Cayley factorization to compute the fers of a list of permutations,
  based on given generators. The permutations of the hash_gen must generate the
  permutations in to_find_fers.
  INPUT hash_gen = {tuple(Per()) : Fer}
  OUTPUT {tuple(Per()) : Fer}

  '''
  hash_keys = hash_gen.keys()
  size = len(list(hash_keys)[0])-1
  hash_gen[tuple(Per(size))] = Fer({0,1}, {0,1}, Per(size))
  generators = [Per(key) for key in hash_keys]
  perms = list(PermutationGroup(*generators).generate())
  all_fact = perms_factorization(perms, generators, update=False, draw=False)
  
  for perm in perms:
    if tuple(perm) not in hash_keys:
      fact = all_fact[tuple(perm)]
      hash_gen[tuple(perm)] = fact_to_fer(fact, hash_gen)

 # ================== OBSOLETE CODE ==================
'''
def _perm_invert(perm):
  return perm**(perm.order()-1)

def _perm_factorization(perm, generators, draw=False):
  
  Given sympy.Permutation object perm, factors it into members of generators,
  assuming these generate the full group. generators must have the same size!

  USE perms_factorization For many factorizations over the same set of generators, it will
  be more efficient to use the same Cayley graph and add new edges with
  previously found factorizations before finding the shortest_path, instead
  of regenerating the entire graph each time.
  
  # First check if generators in fact generate the correct size of permutation.

  size = generators[0].size

  # Close generators under inverses.
  generators = generators + [perm_invert(a) for a in generators if perm_invert(a) not in generators]
  # Create Cayley graph and find shortest path 
  cayley_graph = cayley_graph_maker(PermutationGroup(generators), generators)
  path = nx.shortest_path(cayley_graph, Per(size-1), perm)

  if draw:
    pos = nx.circular_layout(cayley_graph)
    labels = nx.get_edge_attributes(cayley_graph, 'label')
    nx.draw_networkx_nodes(cayley_graph, pos, node_color='teal')
    nx.draw_networkx_edges(cayley_graph, pos, edge_color='blue')
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_nodes(cayley_graph, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(cayley_graph, pos, edgelist=path_edges, edge_color='red')
    nx.draw_networkx_labels(cayley_graph, pos)
    nx.draw_networkx_edge_labels(cayley_graph, pos, edge_labels=labels)
    plt.show()

  # Get back the edges as generators
  genterms = [path[i+1] * perm_invert(path[i]) for i in range(len(path)-1)]
  genterms.reverse() # Reverse to multiply left-to-right

  return(genterms)
'''
