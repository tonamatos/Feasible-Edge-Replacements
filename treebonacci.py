# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 09:27:03 2023

@author: Tonatiuh
"""
from feasible_edge_replacement import Feasible_edge_replacement as Fer

import networkx as nx
from time import time
from sympy.combinatorics.permutations import Permutation as Per
from functools import cache
from amoebas import updating_Cayley_populate

from functools import reduce
fib = lambda n:reduce(lambda x,n:[x[1],x[0]+x[1]], range(n),[0,1])[0]
fibs = lambda i:2*fib(i)

def getMaxdegree(G): # Regresa un vértice de grado máximo.
  dic = dict(G.degree())
  return max(dic, key=dic.get)

def Treebonacci(k): # Genera los primeros n>3 árboles de Fibonacci.
  k += 1
  t0 = time()
  T = [nx.empty_graph(),
       nx.path_graph(2),
       nx.path_graph(2)]

  for i in range(3,k):
    b = getMaxdegree(T[i-2]) + len(T[i-1].nodes())
    Ti = nx.disjoint_union(T[i-1],T[i-2])
    Ti.add_edge(0,b)
    Ti[0][b]['weight'] = i
    Ti[0][b]['color'] = 'green'
    for x in range(b+1):
      for y in range(x+1,b):
        if (x,y) in Ti.edges():
          Ti[x][y]['color'] = 'red'

    for x in range(b,len(Ti.nodes())):
      for y in range(x+1,len(Ti.nodes())):
        if (x,y) in Ti.edges():
          Ti[x][y]['color'] = 'blue'

    T.append(Ti)
  #print("Time to generate trees:",time()-t0)
  return T

# Treebonacci-specific parameters:
  return rho
@cache
def Tk_roots(k):
  '''
  Return roots a, b, c, d for T_k, according to
  the labeling given by Treebonacci.
  '''
  return fibs(k-2), 0, fibs(k-1), fibs(k-1)+fibs(k-3)

@cache
def Tk_sets(k):
  '''
  Generates sets A, B, C, D for Treebonacci, according
  to the above labeling.
  '''
  a, b, c, d = Tk_roots(k)
  A = list(range(a, c))
  B = list(range(b, a))
  C = list(range(c, d))
  D = list(range(d, fibs(k)))
  return A, B, C, D
  
@cache
def Tk_rho(k):
  '''
  Isomorphism A -> C
  rho(5) = Per(9)(a, c)(a + 1, c + 1) 
  rho(6) = = Per(15)(a, c)(a+1,c+1)(a+2,c+2)(a+3,c+3)
  '''
  a, b, c, d = Tk_roots(k)
  A = list(range(a, c))
  rho = Per(fibs(k))
  for x in A:
    rho = rho*Per(x, x + (c - a))
  return rho

@cache
def Tk_phi(k):
  '''
  Isomorphism B -> CUD
  '''
  a, b, c, d = Tk_roots(k)
  B = list(range(b, a))
  phi = Per(fibs(k))
  for x in B:
    phi = phi*Per(x, x + c)
  return phi

@cache
def Tk_generators():
  '''
  For Fibonacci trees up to 4, generates a list of dictionaries with all fers
  associated to their respective permutations. According to our theorem and
  algorithm, this list SHOULD be enough to generate the permutationgroups, and
  thus we can factor any permutation over this hash_map to find its fer.
  '''
  t0 = time()
  
  # Inductive base. NOTE: called hashable function to use @cache decorator.
  hash_fers = [{},
               {tuple(Per(0,1))      : Fer({0,1}, {0,1}, Per(0,1))},
               {tuple(Per(0,1))      : Fer({0,1}, {0,1}, Per(0,1))}]
  hash_fers3 = {tuple(Per(2,3))      : Fer({0,2}, {0,3}, Per(2,3)),
                tuple(Per(3)(1,2))   : Fer({2,3}, {1,3}, Per(3)(1,2)),
                tuple(Per(0,1,3,2))  : Fer({0,1}, {1,3}, Per(0,1,3,2)),
                tuple(Per(0,2,3,1))  : Fer({2,3}, {1,3}, Per(0,2,3,1))}
  hash_fers4 = {tuple(Per(5)(2,3))   : Fer({0,2}, {0,3}, Per(5)(2,3)),
                tuple(Per(5)(1,2))   : Fer({2,3}, {1,3}, Per(5)(1,2)),
                tuple(Per(5)(1,4))   : Fer({4,5}, {1,5}, Per(5)(1,4)),
                tuple(Per(4,5))      : Fer({0,4}, {0,5}, Per(4,5)),
                tuple(Per(0,4)(1,5)) : Fer({0,2}, {2,4}, Per(0,4)(1,5))}
  updating_Cayley_populate(hash_fers3)
  hash_fers.append(hash_fers3)
  updating_Cayley_populate(hash_fers4)
  hash_fers.append(hash_fers4)

  #print("Time to generate base hash maps:",time()-t0)
  return hash_fers