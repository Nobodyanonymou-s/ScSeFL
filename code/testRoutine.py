import numpy as np
import random
import copy
import networkx as nx
import pylab
def Bestroutine(globalroutine):#重写一下，先深度遍历，再Dji一下保证最短
  id = 1
  distance = copy.deepcopy(globalroutine[1])
  print(distance)
  waitlist = [0,1,2,3,4,5,6,7,8,9]
  current = id
  templist = []
  neigbour = []
  routinelist = []
  for index, value in enumerate(distance):
        if 0 < value < 500:
            neigbour.append(index)
  for i in range(0,10):
    current = waitlist[0]
    for j in waitlist:
      if distance[current] > distance[j]:
        current = j
    templist = globalroutine[current]
    routinelist.append(current)
    for index, value in enumerate(templist):
      if 0 < value < 500:
        for k in waitlist:
          if index == k:
            distance[index] = min(distance[index],distance[current]+globalroutine[index][current])
          templist = globalroutine[current]
    for index, value in enumerate(waitlist):
      if value == current:
        del waitlist[index]
  temp = sorted(enumerate(distance), key=lambda distance:distance[1] )
  routinetime = [distance[1] for distance in temp]
  routinelist = [distance[0] for distance in temp]
  return(routinetime)

def randrountine(randL):#随机生成指定边数的路由拓扑
  line = copy.deepcopy(randL)
  globalroutine = []
  neigbourlist = []
  for i in range(10):
    globalroutine.append([500,500,500,500,500,500,500,500,500,500])
    neigbourlist.append([])
  templist = []
  waitlist = []
  for i in range(10):
    waitlist.append(line.pop(random.randint(0,len(line)-1)))
  linelist = [0,0,0,0,0,0,0,0,0,0]
  print(waitlist)
  for index in range(10):
    while linelist[index] < waitlist[index]:
      templist = []
      for i in range(10):
        if linelist[i] < waitlist[i]:
            templist.append(i)
      templist.remove(index)
      for i in neigbourlist[index]:
        j = 0
        while templist != [] and j < len(templist):
          if i == templist[j]:
            templist.pop(j)
          j+=1 
      if templist == []:
        temppp = random.randint(0,9)
        globalroutine[index][temppp]=random.randint(10,30)
        globalroutine[temppp][index]=globalroutine[index][randN]
        linelist[index] +=1
        linelist[temppp] +=1
        neigbourlist[index].append(temppp)
        continue
      randN = random.choice(templist)
      while waitlist[randN] == 1 and waitlist[index] == 1:
         randN = random.choice(templist)
      globalroutine[index][randN]=random.randint(10,30)
      globalroutine[randN][index]=globalroutine[index][randN]
      linelist[index] +=1
      linelist[randN] +=1
      neigbourlist[index].append(randN)

  for i in range(10):
    globalroutine[i][i] = 0
  return globalroutine

def plotroutine(gb):#画拓扑图
  plotRoutine = copy.deepcopy(gb)
  for i in range(10):
    for j in range(10):
      if plotRoutine[i][j] == 500:
        plotRoutine[i][j] = 0
  plotRoutine = np.array(plotRoutine)
  key = range(10)
  s = [str(i+1) for i in range(10)]
  s = dict(zip(key,s))
  A = nx.Graph(plotRoutine)
  pos = nx.shell_layout(A)
  pylab.figure(figsize=(10,10))
  w = nx.get_edge_attributes(A,'weight')
  nx.draw_networkx(A,pos,node_color='pink',labels=s)
  nx.draw_networkx_edge_labels(A,pos,edge_labels=w)
  pylab.savefig("routine.jpg")
  pylab.show()

def print2Dlist(list):
  for i in range(len(list)):
      for j in range(len(list[i])):
          print(list[i][j],end="\t")
      print()

if __name__ == '__main__':
  #randL = [1,2,3,4,6,6,4,3,2,1]#网络拓扑图边数
  randL = [1,1,2,2,3,3,4,4,6,6]
  num_nodes = 10
  num_edges = sum(randL)
  globalr = randrountine(randL)
  print2Dlist(globalr)
  #print(globalr)
  print(Bestroutine(globalr))
  plotroutine(globalr)