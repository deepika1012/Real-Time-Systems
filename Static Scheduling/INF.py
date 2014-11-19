/**
 * @author deepika lakshmanan
 * Real Time Systems 
 */
import math
from fractions import gcd
import random

phase = []
period = []
execT = []
relD = []
with open('input.dat','r') as f:
    newlines = []
    for line in f.readlines():
    	newlines.append(line.replace(')' ,' ').replace('(',' ').strip())
    	
with open('input.dat', 'r') as f:
    for line in newlines:
	
        input = line.split(",")
	
	phase.append(float(input[0]))
	period.append(int(input[1]))
	execT.append(float(input[2]))
	relD.append(float(input[3]))
print "****************Relative Deadline********************"
# Finding the Frame Size using the conditions

def lcm(x,y):
    tmp=x
    while (tmp%y)!=0:
        tmp+=x
    return tmp

def lcmm(*args): 
    return reduce(lcm, args)
hyperP = lcmm(*period)
print "=================HyperPeriod  %d============"% (hyperP)
	
def factors(n):    
    result = set()
    for i in range(1, int(n ** 0.5) + 1):
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div}
    return result

frameSet = set()
frameSet = factors(hyperP)
list1=[]

for f in frameSet:
	list1.append(f)
list1.sort()
frameList = []
seen = set()

for f in list1:
	for val in range(0,len(period)):
		if ((2*f)-gcd(period[val],f))<=(relD[val]):
    			if f not in seen:
				frameList.append(f)
				seen.add(f)
		else:
			break
frameList.sort(reverse=True)
print "\n \n------------------------- "
print " Values of F "
print frameList
print "-------------------------------------Part 1 ends here ------------------------------ "		

''' ** FORD FULKERSON  ** '''
def BFS(C, F, source, sink):
    queue = [source]         # the BFS queue                 
    paths = {source: []}     # 1 path ending in the key
    while queue:

        u = queue.pop(0)     # next node to explore (expand) 
        for v in range(len(C)):   # for each possible next node
 
            # path from u to v?     and   not yet at v?
            if C[u][v] - F[u][v] > 0 and v not in paths:
                 paths[v] = paths[u] + [(u,v)]
                 if v == sink:
                      return paths[v]  # path ends in the key!

                 queue.append(v)   # go from v in the future 
    return None



def max_flow(C, source, sink):
    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in range(n)] # F is the flow matrix
    # residual capacity from u to v is C[u][v] - F[u][v]

    while True:
        path = BFS(C, F, source, sink)
        if not path: break   # no path - we're done!

        edge_flows = [C[u][v]-F[u][v] for u,v in path]
        path_flow = min( edge_flows )
       
        '''print "Augmenting by", path_flow'''
        for u,v in path: # traverse path to update flow
            F[u][v] += path_flow     # forward edge up 
            F[v][u] -= path_flow     # backward edge down 
    copyMatrix = [row[:] for row in F]
    return sum([F[source][i] for i in range(n)])

if __name__ == "__main__":

    # make a capacity graph
    # node   A   B   C   D   E   F
    C = [ [ 00, 16, 13, 00, 00, 00 ],  # A
          [ 00, 00, 10, 12, 00, 00 ],  # B
          [ 00, 04, 00, 00, 14, 00 ],  # C
          [ 00, 00,  9, 00, 00, 20 ],  # D
          [ 00, 00, 00,  7, 00,  4 ],  # E
          [ 00, 00, 00, 00, 00, 00 ] ] # F

    #print "C is", C
    source = 0  # A
    sink = 5    # F

    max_flow_value = max_flow( C, source, sink )
    #print "max_flow_value is", max_flow_value
''' **** FORD FULKERSON  ** '''

print "-------------------------------------Part 2 starts here ------------------------------ "	
# Scheduling conditions using the Iterative Network Flow Algorithm 
frameVertices = []
M = []
for frameSize in frameList:
	counter1=1
	counter=1
	totalExectime = 0
	totalVertices=0
	jobVertices=0
	totalJobVertices=0
	
	for input in range(0,len(period)):
		jobVertices = hyperP/period[input]
		totalJobVertices += jobVertices
		
	frameIndex = hyperP/frameSize
	totalVertices = frameIndex + totalJobVertices + 2
	Matrix = [[0 for row in range(0,totalVertices)] for col in range(0,totalVertices)]
	copyMatrix=[[0 for row in range(0,totalVertices)] for col in range(0,totalVertices)]
	
	for i in range(0,totalVertices):
		for j in range(0,totalVertices):
			Matrix[i][j]=0
			
	for nf in range(0,frameIndex):
		fv = 'FrameVertex'+ str(nf+1)
		frameRowIndex = totalJobVertices+nf+1
		Matrix[frameRowIndex][totalVertices-1]=frameSize
		
	for input in range(0,len(period)):
		for nj in range(0,hyperP/period[input]):
			jv = 'JobVertex'+str(input+1)+'-'+str(nj+1)
			jobColIndex=counter1
			counter1 = counter1+1
			Matrix[0][jobColIndex]=execT[input]
			totalExectime += execT[input]
			periodStartTime = nj * period[input]
			jobRowIndex=counter
			counter = counter+1
			for nf in range(0,frameIndex):
				if(((nf*frameSize)>=(periodStartTime))and((periodStartTime+relD[input])>=((nf+1)*frameSize))):
					edge1 = jv
					edge2 = 'FrameVertex' + str(nf+1)
					frameColIndex=totalJobVertices+1+nf
					Matrix[jobRowIndex][frameColIndex]=frameSize
	print "Execution Time =  %f"%totalExectime
	MaxFlow = max_flow(Matrix,0,totalVertices-1)
	print "Maxflow value = %f"%MaxFlow
	print " FRAME SIZE = %d"% frameSize
	if(totalExectime==MaxFlow):
		print "MaxFlow Attained"
	else: 
		print "MaxFlow not Attained"
	print "********************************************************************************"	


