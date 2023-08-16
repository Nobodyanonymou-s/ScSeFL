import numpy as np
from hashlib import sha256
from hashlib import md5
import time
import copy
import math
import random
import threading
import eventlet
import os
from blockchain import Blockchain
from blockchain import Block
Th_1 = 0.2
Th_2 = 0.2
difficulty = 4
lock = threading.RLock()
timeP = [0,0,0,0,0,0,0,0,0,0]
class mail:
      def __init__(self, id, time, str, broadcast):
            #self.hash = 0
            self.id = int(id)
            self.timestamp = time
            self.content = str
            self.flag = broadcast
    #   def  compute_hash(self):
    #         temp = self.__dict__
    #         str_temp = str(temp)
    #         return md5(str_temp.encode('utf8')).hexdigest()
     #  def __str__(self):
     #        return "{}-{}-{}-{}".format(self.timestamp, self.id, self.content, self.flag)
      #__repr__ = __str__
class qqueue:
    '''收信箱'''
    def __init__(self):
        self.__list = []
    
    def addq(self,item):
        '''往队尾加元素，深拷贝'''
        self.__list.append(copy.deepcopy(item))

    def delq(self):
        '''从队列头部删除元素'''
        return self.__list.pop(0)

    def is_empty(self):
        '''判断是否为空'''
        return self.__list == []
    
    def empty(self):
         '''清空信箱，主要用于给主程序返回消息'''
         self.__list=[]
    def size(self):
        '''返回列表大小'''
        return len(self.__list)
    
class Node:#处理Pow结果的, 重写消息相关
      def __init__(self, ID, energy, cPower,msgnet):
            self.ID = ID
            self.energy = energy
            self.cPower = cPower
            self.strategy = 0
            self.Em = 0.0
            self.AvgEm = 0.0
            self.globalEm = [0,0,0,0,0,0,0,0,0,0]
            self.flag = 0
            self.mailbox = mail(self.ID,0.0,"",0)
            self.neigbour = []
            self.routinetime = []
            self.routinelist = []
            self.msglist = []
            self.winner = []
            self.msgnet = msgnet
          #   self.sever = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          #   self.address = (f'192.168.3.31', 18887+self.ID)
          #   self.sever.bind(self.address)
          #   self.sever.settimeout(1)

      def compute_hash(self, content):
            str_temp = str(content)
            return sha256(str_temp.encode('utf8')).hexdigest()
      
      def assembleMsg(self, content, flag):#不搞转发就不加上hash了
            self.mailbox.timestamp = time.time()
            self.mailbox.content = content
            self.mailbox.flag = flag
            #self.mailbox[0].hash = 0
            #self.mailbox[0].hash = self.compute_hash(self.mailbox[0])

      def sendMsg(self,id):#加上根据路由算wait时间的部分
            if id == 500 and self.mailbox.flag == 1:#广播
               self.msgnet[self.ID].addq(self.mailbox)
               for i in range(1,10):
                    temp = 0.001*(self.routinetime[i]-self.routinetime[i-1])
                    time.sleep(temp)
                    self.msgnet[self.routinelist[i]].addq(self.mailbox)#sort以后要把ID对应换回来。。
            else:#发指定地址,要考虑发给自己
                  for i in range(0,10):
                       if self.routinelist[i] == id:
                         time.sleep(0.001*self.routinetime[i])
                         self.msgnet[id].addq(self.mailbox)
                         break
            self.mailbox = mail(self.ID,0.0,"",0)
 
      def receiveMsg(self,flag):#
           eventlet.monkey_patch(time=True)
           tim = 3                                                                                                                             
           with eventlet.Timeout(tim,False):
               while True:
                    time.sleep(0.001)
                    if not self.msgnet[self.ID].is_empty():
                        self.msglist.append(copy.deepcopy(self.msgnet[self.ID].delq()))
                        #print('id {} received'.format(self.ID))
                        if flag == 1 or len(self.msglist) > 8:
                             break

      def calEm(self):
           tE = pow(self.energy-Th_1,0.5) if self.energy-Th_1 > 0 else 0
           tC = self.cPower-Th_2 if self.cPower-Th_2 > 0 else 0
           tK = len(self.neigbour)/10
           self.Em = pow(3,0.5)*(tE*tC+tE*tK+tC*tK)#雷达图面积
           #print('{}:{}'.format(self.ID,self.Em))

      def PoW(self, block):
          """
          难度值由全局变量difficulty获取
          """
          begin = time.time()
          self.flag = 1
          temp_block = copy.deepcopy(block)
          temp_block.nonce = 0
          #content = str(temp_block)
          computed_hash = self.compute_hash(temp_block)
          self.msgnet[self.ID].empty()
          while not computed_hash.startswith('0' * difficulty):
               if self.msgnet[self.ID].is_empty():
                 temp_block.nonce += 1
                 computed_hash = self.compute_hash(temp_block)
               else:
                    self.flag = 0
                    break  
          del temp_block
          if self.flag == 1:
            self.assembleMsg(self.ID,1)
            self.sendMsg(500)
          end = time.time()
          timeP[self.ID] = end - begin
          #return computed_hash
      
      def calStrategy(self,s,block):
           self.strategy = s
           match self.strategy:
                case 1:
                     if self.Em > self.AvgEm:
                          self.PoW(block)
                case 2:
                     if random.random() >0.5:
                          self.PoW(block)
                case 3:
                     if self.globalEm.index(self.Em)>6:
                          self.PoW(block)
                case _:
                     return
                          
      def Bestroutine(self,globalroutine):#重写一下
          distance = copy.deepcopy(globalroutine[self.ID])
          waitlist = [0,1,2,3,4,5,6,7,8,9]
          current = self.ID
          templist = []
          for index, value in enumerate(distance):
               if 0 < value < 500:
                    self.neigbour.append(index)
          for i in range(0,10):
               current = waitlist[0]
               for j in waitlist:
                    if distance[current] > distance[j]:
                         current = j
               templist = globalroutine[current]
               self.routinelist.append(current)
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
          self.routinetime = [distance[1] for distance in temp]
          self.routinelist = [distance[0] for distance in temp]
          #print(distance)
          #return bestroutine
           #return self.bestroutine
      def calAvgEm(self):
          Emlist = [0,0,0,0,0,0,0,0,0,0]
          while self.msglist != []:
               temp = self.msglist.pop()
               Emlist[temp.id] = temp.content
          self.globalEm = sorted(Emlist)
          self.AvgEm = sum(self.globalEm)/10
          #print(self.AvgEm)
      def respond(self,flag):
          match flag:
                case 1:#给不需要验证用的
                    self.receiveMsg(1)
                    if self.ID != 1:
                      if self.msglist != []:
                        self.assembleMsg(123,0)
                        self.sendMsg(1)
                case 2:#给要验证PoW用的,要广播自己认为的winner
                    self.receiveMsg(1)
                    if self.msglist != []:
                       temp = self.msglist[0]
                       self.winner = temp.id
                       #print('{}:{}'.format(self.ID,self.winner))
                       self.msglist = []
                       self.msgnet[self.ID].empty()
                       self.assembleMsg(self.winner,1)
                       self.sendMsg(500)
                    self.receiveMsg(flag)
                    self.verifyPoW()
                case 3:#通知主进程winner
                    self.msglist = []
                    self.msgnet[self.ID].empty()
                    self.assembleMsg(self.winner,0)
                    self.sendMsg(self.ID)
                    self.assembleMsg(123,0)
                    self.sendMsg(self.winner)
                case _:
                     return
          self.msglist = []

      
      def verifyPoW(self):#统计一下谁是真正赢家，然后给他发消息
          winlist = [0,0,0,0,0,0,0,0,0,0]
          while self.msglist != []:
               temp = self.msglist.pop()
               if int(temp.content) < 10:
                   winlist[int(temp.content)] += 1
          t = 0
          for i in range(0,9):
               if winlist[t] < winlist[i]:
                    t = i
          self.winner = t

#写一个主进程函数放main_fed里跑✔
class ePoWProcess(threading.Thread):
    def __init__(self,name,node,block,gr):
         threading.Thread.__init__(self, name=name)
         self.node = node
         self.block = block
         self.gr = gr
    def run(self):
         st = time.time()
         strategy = 3#策略
         self.node.Bestroutine(self.gr)
         self.node.calEm()
         self.node.assembleMsg(self.node.Em, 1)
         self.node.sendMsg(500)
         self.node.receiveMsg(2)
         self.node.calAvgEm()
         self.node.calStrategy(strategy,self.block)
         self.node.respond(2)
         self.node.respond(3)
         et = time.time()
         #timeP[self.node.id] = et-st
         #print('id:{} time:{}'.format(self.node.ID,et - st))
         #return et - st
    
class PoWProcess(threading.Thread):#调好了
    def __init__(self,name,node,block,gr):
         threading.Thread.__init__(self, name=name)
         self.node = node
         self.block = block
         self.gr = gr
    def run(self):
         st = time.time()
         self.node.Bestroutine(self.gr)
         self.node.PoW(self.block)
         self.node.respond(2)
         self.node.respond(3)
         et = time.time()
         #timeP[self.node.id] = et-st
         #print('id:{} time:{}'.format(self.node.ID,et - st))
         #return et - st

class FLProcess(threading.Thread):#调通了
    def __init__(self,name,node,block,gr):
         threading.Thread.__init__(self, name=name)
         self.node = node
         self.block = block
         self.gr = gr
    def run(self):
         st = time.time()
         id = 1
         self.node.Bestroutine(self.gr)
         if self.node.ID == 1: 
              self.node.assembleMsg(123,1)
              self.node.sendMsg(500)
         if self.node.ID !=1:
              self.node.respond(2)
         else:
              self.node.respond(1)
              self.node.assembleMsg(123,1)
              self.node.sendMsg(500)
         et = time.time()
         #print('id:{} time:{}'.format(self.node.ID,et - st))
         #return et - st
    
def randrountine(randList):#随机生成指定边数的路由拓扑
  line = copy.deepcopy(randList)
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




#def ePow():#ePow过程，差更新能量、计算资源和全局路由的函数
    #测试样例
#if __name__ == "__main__":
def PPPorcess(test,iter,lastW):
     bchain = Blockchain()
     bchain.create_genesis_block()
     energy = [1,1,1,1,1,1,1,1,1,1]
     cPower = [1,1,1,1,1,1,1,1,1,1]
     Gwinner = [0,0,0,0,0,0,0,0,0,0]
     randLine = [1,1,2,2,3,3,4,4,6,6]
     #last = Block(0,[], 0, "0")
     msgnet = [qqueue() for i in range(0,10)]
     #for i in range(0,20):#差三个函数，算能量的，算算力的和算全局路由的
     #只是方便改格式
          #start = time.time()
          #print("========================Main Thread{}============================".format(i))
     globalroutine = randrountine(randLine)
     temp_str = str(energy)+str(cPower)
     last = bchain.last_block()
     new_block = Block(index=last.index + 1,
                         transactions=temp_str,
                         timestamp=time.time(),
                         previous_hash=last)
     bchain.addblock(new_block)
     for j in range(0,9):
          energy[j] = -0.04*iter+1+0.02*random.uniform(-1,1)
          cPower[j] = np.random.rand()
          if j == lastW:
               energy[j] = 0
               cPower[j] = 0
     node=[Node(ind, energy[ind], cPower[ind],msgnet) for ind in range(0,10)]
     match test:
          case 1: 
               UAVnode = [FLProcess(f'node{j}',node[j],new_block,globalroutine) for j in range(0,10)]
          case 2:
               UAVnode = [PoWProcess(f'node{j}',node[j],new_block,globalroutine) for j in range(0,10)]
          case 3:   
               UAVnode = [ePoWProcess(f'node{j}',node[j],new_block,globalroutine) for j in range(0,10)]
          case _:
               print('wrong para')
     # UAVnode[1].run()
     # UAVnode[2].run()
     # UAVnode[1].join()
     # UAVnode[2].join()
     #(timeout=1)
     for t in UAVnode:
          t.start()
          # t.run()
     for t in UAVnode:
          t.join()
     for k in range(0,10):
          if not msgnet[k].is_empty():
               Gwinner[k] = int(msgnet[k].delq().content)
               msgnet[k].empty()
     #end = time.time()
     #print(Gwinner)
     #print(end-start)
     #os.system("pause")
     del node,UAVnode,globalroutine
     
     temp = sum(timeP)
     print(Gwinner)
     return temp#Gwinner[0]