# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 17:50:33 2024

@author: Tonatiuh
"""

from feasible_edge_replacement import Feasible_edge_replacement as Fer
from amoebas import isLocalColoredAmoeba
from amoebas import isFer, FerGroup, brute_force_populate, add_pairs_prod, updating_Cayley_populate
import gravis as gv
global gv_options
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation as Per

gv_options = {'show_node_label' : True,
              'edge_size_data_source' : 'weight',
              'use_edge_size_normalization' : False,
              'edge_curvature' : 0,
              'zoom_factor' : 2,
              'many_body_force_strength' : -10}

# Graph objects
import networkx as nx

# Ejemplo: crear gráfica
G = nx.Graph()
aristas = [(0,4),(0,1),(0,2),(0,8),
           (1,9),(1,0),(1,2),(1,5),
           (2,8),(2,6),(2,1),(2,0),(2,7),
           (3,4),(3,5),(3,6),#(3,0),(3,1),(3,2),
           (4,0),(4,9),(4,3),
           (5,1),(5,3),(5,7),
           (6,3),(6,2),(6,8),
           (7,5),(7,2),
           (8,2),(8,0),(8,6),
           (9,1),(9,4)]

aristas = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),
           (6,7),(7,8),(8,9),(9,10),(10,11),(11,0),
           (0,5),(1,3),(2,10),(4,6),(7,9),(8,11),
           (12,11),(13,11)]

G.add_edges_from(set(aristas))

for node in G.nodes():
  G.nodes[node]['color'] = 0
  
G.nodes[12]['color'] = 'red'
G.nodes[13]['color'] = 'blue'


#Petersen
G = nx.petersen_graph()

G.nodes[0]['color'] = 'black'
G.nodes[1]['color'] = 'blue'
G.nodes[4]['color'] = 'blue'
G.nodes[5]['color'] = 'blue'

'''
# Colorear
coloracion = {0 : 'blue',
              1 : 'blue',
              2 : 'blue',
              3 : 'blue'}

for node, color in coloracion.items():
    G.nodes[node]['color'] = color
 '''  
# Dibujar interactivamente:
fig = gv.d3(G, **gv_options)
fig.display()

FGroup = FerGroup(G)

print(*['\t'+str(fer)+'\n' for fer in FGroup.values()])

# Método para generar el grupo completo:
#brute_force_populate(FGroup)

group = PermutationGroup([Per(per) for per in FGroup.keys()])

print(group.order())