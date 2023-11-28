# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 16:56:17 2023

@author: Tonatiuh
"""
from amoebas import perm_fact_into_trans, fact_to_fer, fer_verifier
import treebonacci as trb
from feasible_edge_replacement import Feasible_edge_replacement as Fer

from sympy.combinatorics.permutations import Permutation as Per
from functools import cache
from time import time
from random import shuffle

def randomIso(k):
  p_list = list(range(1,trb.fibs(k)))
  shuffle(p_list)
  return Per([0] + p_list)

# Stem-symmetric algorithm
@cache
def trans_to_fer(x, k):
  # Treebonacci-specific base case:
  if k < 5:
    hash_gen = trb.Tk_generators()
    y0 = 1
    fer = hash_gen[k][tuple(Per(y0,x).resize(trb.fibs(k)))]
    old_per = fer.seq_perm
    fer.seq_perm = old_per.resize(trb.fibs(k))
    return fer
  a, b, c, d = trb.Tk_roots(k) # b=0
  
  # CASES:
  if x == b: # b=0
    '''
    Write (y0, b) = ...?... using (ab -> ac)
    '''  
    phi = trb.Tk_phi(k) # isomorphism B -> CUD
    fer_phi = Fer({a,b}, {a,c}, phi) # (phi : ab -> ac)
    known_fer = trans_to_fer((phi**(-1)).apply(x), k)
    fer = fer_phi*known_fer*fer_phi
    old_per = fer.seq_perm
    fer.seq_perm = old_per.resize(trb.fibs(k))
    return fer
  
  A, B, C, D = trb.Tk_sets(k)
  if x in A or x in B: # x in AUB\{b}
    '''
    (y0 ,x) is known inside k-1.
    '''
    fer = trans_to_fer(x, k-1)
    old_per = fer.seq_perm
    fer.seq_perm = old_per.resize(trb.fibs(k))
    return fer
  
  if x in C:
    '''
    Write (y0, x) = rho**(-1)*(y0, w**(-1)(x))*rho, where
    rho:cd->ad
    (w**(-1)(x), y0) is in case 1 cause w**(-1)(x) in A.
    '''
    rho = trb.Tk_rho(k) # isomorphism A -> C
    fer_rho = Fer({c,d}, {a,d}, rho) # (rho : cd -> ad)
    known_fer = trans_to_fer((rho**(-1)).apply(x), k)
    fer = fer_rho*known_fer*fer_rho
    old_per = fer.seq_perm
    fer.seq_perm = old_per.resize(trb.fibs(k))
    return fer
  
  if x in D:
    '''  
    Write (y0, x) = (y0, x0)(x, x0)(y0, x0), where
    (y0, x0) is in case 2 for k
    (x, x0) is known by case 2 for k-2.
    '''
    x0 = c + 1 # An element of C\{c}
    y0x0_fer = trans_to_fer(x0, k)
    xx0_fer = trans_to_fer(x-c, k-2) + c
    fer = y0x0_fer*xx0_fer*y0x0_fer
    old_per = fer.seq_perm
    fer.seq_perm = old_per.resize(trb.fibs(k))
    return fer

#=============================== MAIN ALGORITHM ===============================

#---------------- 0. GENERATE TREES AND FIND GENERATORS UP TO 4 ---------------
#print(*[str(Per(per))+' : '+str(len(fer))+'\n' for per,fer in hash_gen[4].items() if len(fer) == 3])
#print("Here dummy",len(hash_gen[4][tuple(Per(5)(1,3))]))

#------------------------------[VERIFY GENERATORS]-----------------------------
#T_k = trb.Treebonacci(8)
#fer_verifier(T_k[1], hash_gen[1])
#fer_verifier(T_k[2], hash_gen[2])
#fer_verifier(T_k[3], hash_gen[3])
#fer_verifier(T_k[4], hash_gen[4])

#--------------------------------- 0. INPUT -----------------------------------
k = 6

permutation = Per(trb.fibs(k))
for x in range(0,trb.fibs(k),2):
  permutation = permutation*Per(x, x+1)
  
permutation = Per(*tuple(randomIso(k).cyclic_form[0])).resize(trb.fibs(k))
  
#permutation = Per(1,trb.fibs(k)-1)

#-------------------- 1. FACTOR PERMUTATION INTO GENERATORS -------------------
y0 = 1 # Or any element of B\{b}. In our labeling, b=0.
permutation = permutation.resize(trb.fibs(k))
fact_in_trans = perm_fact_into_trans(permutation, y0)

#------------------------- 2. FIND FERS OF GENERATORS -------------------------  
known_fer = {}
t0 = time()
for trans in fact_in_trans:
  i, j = trans.cyclic_form[0] # Extract non y0 value in cycle.
  if i == y0:
    x = j
  elif j == y0:
    x = i
  
  found_fer = trans_to_fer(x, k)
  known_fer[tuple(trans)] = found_fer
print("Found Fer in time:",time()-t0)
#-------------------- 3. FIND FER ASSOCIATED TO PERMUTATION -------------------
fer = fact_to_fer(fact_in_trans, known_fer)  

#--------------------------------- 4. OUTPUT ----------------------------------
#T = T_k[k]
#fer_verifier(T, known_fer)

print(*[str(f)+'\n' for f in fer])
#l = len(fer)
#print("Fer len is",l)
#==============================================================================