# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 06:34:32 2020

@author: Vipul
"""

import sys

import pandas as pd
import csv
import copy
import queue as Q

inp=sys.argv[1]
#inp="000000000302540000050301070000000004409006005023054790000000050700810000080060009"
#inp="000100702030950000001002003590000301020000070703000098800200100000085060605009000"
#inp="000260701680070090190004500820100040004602900050003028009300074040050036703018000"#AC3 1

#inp="000001000020000008691200000000000014102506003800020506005000000730000000006319405" #AC3 2

rw="ABCDEFGHI"
sudoku={rw[int(i/9)]+str((i%9)+1) : int(inp[i]) for i in range(81)}

domain=set(range(1,10))

#unassigned={rw[int(i/9)]+str((i%9)+1) : int(inp[i]) for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]==0}
#unassigned={rw[int(i/9)]+str((i%9)+1) : {int(inp[i])} for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]==0}

def unass(sudoku):
    #return {rw[int(i/9)]+str((i%9)+1) : {int(inp[i])} for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]==0}
    return {rw[int(i/9)]+str((i%9)+1) : {sudoku[rw[int(i/9)]+str((i%9)+1)]} for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]==0}
#unassigned=unass(sudoku)
    
#assigned=sudoku
#assigned={rw[int(i/9)]+str((i%9)+1) : int(inp[i]) for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]!=0}

def ass(sudoku):
    #return {rw[int(i/9)]+str((i%9)+1) : int(inp[i]) for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]!=0}
    return {rw[int(i/9)]+str((i%9)+1) : sudoku[rw[int(i/9)]+str((i%9)+1)] for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]!=0}

#assigned=ass(sudoku)
# BTS 44

#AC3 59 & 61

def printsudoku(sudku):
    for i in range(81):
        key=rw[int(i/9)]+str((i%9)+1)
        print(sudku[key], end = " ")
        if (i+1)%9==0 :
            print("\n")
#printsudoku(sudoku)
    

#Check for duplicates in row or column or grid. Returns True if all unique
def alldiff(assigned,cell):
    g1=[cell[0]+ str(i) for i in range(1,10)] #row
    g2=[rw[i-1]+cell[1] for i in range(1,10)] #col
    cellx=int((rw.index(cell[0]))/3)*3
    #celly=int(int(cell[1])/3)*3
    celly=int((int(cell[1])-1)/3)*3
    g3=[rw[i]+str(j+1) for i in range(cellx,cellx+3) for j in range(celly,celly+3)] #3*3 grid
    """print(g1)
    print(g2)
    print(g3)"""
    
    diff=True
    for g in [g1,g2,g3]:
        gv=[ assigned[i] for i in g if i in assigned]
        """print(gv )
        print(len(gv))
        print(len(set(gv)))"""
        if len(gv) != len(set(gv)):
            diff=False
            break
        #gv=gv+[9]
        
    return diff
    
    #import timeit
    #timeit.timeit("[ assigned[i] for i in g3 if i in assigned]")


#assigned['D1']=5
#assigned['A7']=5
#assigned['D7']=5


#dif=alldiff(assigned,"D7")
#print(dif)
    
# optimization scope: g1 g2 g3 will have some common cells too. so instead of 9+9+9=27 check we can do 21 checks by avoiding repetitions
#prepare a list of all neighbor elements from row, column and grid. Returns this list
def neighbors(assigned,cell):
    g1=[cell[0]+ str(i) for i in range(1,10)] #row
    g2=[rw[i-1]+cell[1] for i in range(1,10)] #col
    cellx=int((rw.index(cell[0]))/3)*3
    #celly=int(int(cell[1])/3)*3
    celly=int((int(cell[1])-1)/3)*3
    g3=[rw[i]+str(j+1) for i in range(cellx,cellx+3) for j in range(celly,celly+3)] #3*3 grid
    """print(g1)
    print(g2)
    print(g3)"""
    
    
    nbrs=[]
    
    for g in [g1,g2,g3]:
        gv=[ assigned[i] for i in g if i in assigned]
        nbrs+=gv
        #print(gv )
        """print(nbrs)"""
        
    return nbrs
#nbrs=neighbors(assigned,"D7")
#print(nbrs)

#prepare a list of domains for all neighbor elements from row, column and grid. Returns this list
def neighbors_dom(unassigned,cell):
    g1=[cell[0]+ str(i) for i in range(1,10)] #row
    g2=[rw[i-1]+cell[1] for i in range(1,10)] #col
    cellx=int((rw.index(cell[0]))/3)*3
    #celly=int(int(cell[1])/3)*3
    celly=int((int(cell[1])-1)/3)*3
    g3=[rw[i]+str(j+1) for i in range(cellx,cellx+3) for j in range(celly,celly+3)] #3*3 grid
    """print(g1)
    print(g2)
    print(g3)"""
    
    
    nbrs=[]
    
    for g in [g1,g2,g3]:
        #gv=[ list(unassigned[i]) for i in g if i in unassigned ]
        gv=[ j for i in g if i in unassigned for j in list(unassigned[i])]
        nbrs+=gv
        """print(gv )
        print(nbrs)"""
        
    return nbrs

#nbrs=neighbors_dom(unassigned,"I7")
#print(nbrs)

#Take dictionary as input and calculate domain for all unassigned cells based on their neighbours
def domain_calc(unassigned,assigned):
    for i in range(81):
        key=rw[int(i/9)]+str((i%9)+1)
        if key in unassigned:
            nbrs=set(neighbors(assigned,key))
            unassigned[key]=domain-nbrs
    return unassigned
            #print(key)
        
#domain_calc(unassigned,assigned)
        
#Among unassigned cells, select cell with minimum legal values
def mrv(unassigned):
    min_legal_val_count=10
    min_legal_val_key="Z1"
    for i in range(81):
        key=rw[int(i/9)]+str((i%9)+1)
        if key in unassigned:
            legal_val_count=len(unassigned[key])
            if min_legal_val_count>legal_val_count:
                min_legal_val_count=legal_val_count
                min_legal_val_key=key
            if min_legal_val_count==0:
                break
    #return min_legal_val_key,min_legal_val_count
    return min_legal_val_key

#print(mrv(unassigned))

"""#Select least constraining value for a cell out of its domain. ie a value that won't that would reduce the domain of other cells by minimum
def lcv(cell):
    nbrs=neighbors(cell)
    dom=list(unassigned[cell])
    print(nbrs)
    print(dom)
    least_con=len(nbrs)
    for i in dom:
        ln=nbrs.count(i)
        if ln < least_con:
            least_con=ln
            least_con_val=i
        #print(least_con_val, least_con)
    return least_con_val, least_con

print(lcv("I1"))"""

"""#Select least constraining value for a cell out of its domain. ie a value that won't that would reduce the domain of other cells by minimum
def lcv(cell):
    nbrs=neighbors_dom(cell)
    dom=list(unassigned[cell])
    print(nbrs)
    print(dom)
    least_con=len(nbrs)
    for i in dom:
        ln=nbrs.count(i)
        if ln < least_con:
            least_con=ln
            least_con_val=i
        #print(least_con_val, least_con)
    return least_con_val, least_con

print(lcv("I7"))"""

#Select least constraining value for a cell out of its domain. ie a value that won't that would reduce the domain of other cells by minimum
def lcv_ordered_dom(unassigned,cell):
    nbrs=neighbors_dom(unassigned,cell)
    dom=list(unassigned[cell])
    #print(nbrs)
    #print(dom)
    ordered_dom=[]
    for i in dom:
        ln=nbrs.count(i)
        ordered_dom+=[(ln,i)]
        ordered_dom.sort(key= lambda tup:tup[0])
        ordered_dom2=[i[1] for i in ordered_dom]
        
    return ordered_dom2

#print(lcv_ordered_dom(unassigned,"I7"))
#1,4,3,2
        
def state_chk(state):
    
    if len(state)==0:
        return "result"
    dom_size=[ len(state[i]) for i in state ] #checks domain size for every unassigned value
    
    if dom_size.count(0) >=1: #checks if domain size is 0 for any unassigned value
        return "Failure"
    #elif len(state)==sum(dom_size):
    #    return "result"
    elif len(state)<sum(dom_size):
        return "valid"
        

#tst={rw[int(i/9)]+str((i%9)+1) : {int(inp[i])} for i in range(81) if sudoku[rw[int(i/9)]+str((i%9)+1)]==0}
#print(state_chk(tst))
        
#unassigned.pop("A1")

def backtrack(state,depth):
    #print("depth ",depth)
    global cntr    
    cntr+=1
    #print("cntr ",cntr)
    unassigned0=unass(copy.deepcopy(state))
    assigned=ass(copy.deepcopy(state))
    unassigned=domain_calc(copy.deepcopy(unassigned0),copy.deepcopy(assigned))
    
    chk=state_chk(copy.deepcopy(unassigned))
    if chk=="result":
        #print("This is result")
        #print( len(unassigned0))
        #printsudoku(state)
        return state
    elif chk=="Failure":
        #print("Failed")
        return "Failure"
        
    
    
    
    var=mrv(copy.deepcopy(unassigned))
    
    lcv_list=lcv_ordered_dom(copy.deepcopy(unassigned),var)
    
    for val in lcv_list:
        global cntr2
        cntr2+=1
        #print("cntr2 ",cntr2)
        
        state[var]=val
        
        #below 5 line for debugging  only
        """print("Var :", var)
        print("Val :", val)
        print("Domain : ", lcv_ordered_dom(copy.deepcopy(unassigned),var))"""
        #printsudoku(state)  
        """if cntr==8: # first failed on cntr 8.
            return state,unassigned0,assigned,unassigned"""
        
        """assigned[var]=val
        if alldiff(copy.deepcopy(assigned),var):"""
        
        result=backtrack(copy.deepcopy(state), depth+1)
            
        if result=="Failure":
            #print("Failure returned")
            #print("depth ",depth , " loop size ", len(lcv_ordered_dom(copy.deepcopy(unassigned),var)))
            #print("depth ",depth , " loop size ", len(lcv_ordered_dom(copy.deepcopy(unassigned),var)) , " " ,len(lcv_list))
            state[var]=0
        else:
            return result
        """else:
            del assigned[var]"""
            
    
    
    #return state
    return "Failure"
    
#sudoku={rw[int(i/9)]+str((i%9)+1) : int(inp[i]) for i in range(81)}
global cntr,cntr2
cntr=0
cntr2=0
sol=backtrack(copy.deepcopy(sudoku),0)
#sol,una0,ass,una=backtrack(copy.deepcopy(sudoku))
#printsudoku(sol)

#printsudoku(sudoku)

    
"""sols=[str(i) for i in list(sol.values())]
sols_out="".join(sols)"""
#print(sols_out)
#sol.values()

    
    
#Identify all the Binary Arcs
def binary_arcs(unassigned,cell):
    g1=[cell[0]+ str(i) for i in range(1,10)] #row
    g2=[rw[i-1]+cell[1] for i in range(1,10)] #col
    cellx=int((rw.index(cell[0]))/3)*3
    #celly=int(int(cell[1])/3)*3
    celly=int((int(cell[1])-1)/3)*3
    g3=[rw[i]+str(j+1) for i in range(cellx,cellx+3) for j in range(celly,celly+3)] #3*3 grid
    """print(g1)
    print(g2)
    print(g3)"""
    
    g_all=list(set(g1+g2+g3))
    #print(g_all)
    
    arcs0=[]
    
    #for g in [g1,g2,g3]:
    for g in [g_all]:
        #gv=[ list(unassigned[i]) for i in g if i in unassigned ]
        #gv=[ [cell,i] for i in g if i in unassigned ]
        gv=[ [cell,i] for i in g if (i in unassigned) & (i!=cell) ]
        arcs0+=gv
        """print(gv )
        print(nbrs)"""
        #arcs=list(set(arcs0))
        arcs=arcs0
    return arcs
"""tst=binary_arcs(unassigned,"A1")
tst2=binary_arcs(unassigned,"A2")
tstn=tst+tst2"""

def pos_arcs(unassigned):
    arc_set=[]
    for i in unassigned:
        #print(i)
        arc=binary_arcs(unassigned,i)
        arc_set=arc_set+arc
        #print(arc_set)
    return arc_set
    
#unassigned=unass(sudoku)
#final_arc_set=pos_arcs(unassigned)
        
        


def rev(xi,xj,unass):
    di=unass[xi]
    dj=unass[xj]
    """print(di)
    print(len(di))
    print(dj)
    print(len(dj))"""
    dk=[]
    for x in di:
        if (len(dj)==1) & (x in dj):
            dk=dk+[x]
            #print(dk)
        """    print(x, " Not Consistent")
        else:
            print(x, " Consistent")"""
    if len(dk)>0:
        new_di=di-set(dk)
        #print(new_di)
        unass[xi]=new_di
        return True
    else:
        return False
            
#domain_calc(unassigned,assigned)      
#rev("I9","I7",unassigned)
    
def ac3(state):
    
    unassigned0=unass(copy.deepcopy(state))
    assigned=ass(copy.deepcopy(state))
    unassigned=domain_calc(copy.deepcopy(unassigned0),copy.deepcopy(assigned))
    #unassigned_orig=copy.deepcopy(unassigned)
    
    final_arc_queue=pos_arcs(copy.deepcopy(unassigned))
    
    qu=Q.Queue()
    for i in final_arc_queue:
        qu.put_nowait(i)
    #j=0
    while not qu.empty():
        #j+=1
        #print(j)
        arc=qu.get_nowait()
        #print(arc)
        #print(arc[0],arc[1])
        
        if rev(arc[0],arc[1],unassigned):
            if len(unassigned[arc[0]])==0:
                #return False
                #print("No more valid moves")
                return "Failure"
            
            for nbrs in binary_arcs(copy.deepcopy(unassigned),arc[0]):
                nbrs.reverse()
                qu.put_nowait(nbrs)
    
    #return True
    for v in unassigned:
        if len(unassigned[v])!=1:
            #print("Not solved fully")
            #print(unassigned)
            return "Failure"
        tmp=list(unassigned[v])
        state[v]=tmp[0]
        
    return state
        
    """chk=state_chk(copy.deepcopy(unassigned))
    if chk=="result":
        return state
    elif chk=="Failure":
        print("Failed")
        return "Failure"
    """
  
sol=ac3(copy.deepcopy(sudoku))
sol
algo="AC3"
if sol=="Failure":
    sol=backtrack(copy.deepcopy(sudoku),0)
    algo="BTS"
    
sols=[str(i) for i in list(sol.values())]
sols_out="".join(sols)
#print(sols_out)
#print(algo)

"""with open("output.txt", 'a', newline='') as csvfile:
            fieldnames = ['sols_out', 'algo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'sols_out': sols_out, 'algo': algo})
            csvfile.close()"""
            
outf=open("output.txt","w")
outf.write(sols_out+" "+ algo)
outf.close()
#sol,una0,ass,una=backtrack(copy.deepcopy(sudoku))
#printsudoku(sol)