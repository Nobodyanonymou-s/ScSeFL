import copy
import eventlet
import numpy as np
import math
import random
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
    
    def size(self):
        '''返回列表大小'''
        return len(self.__list)

# def receiveMsg(self,flag):#这是BUG
#     eventlet.monkey_patch(time=True)
#     while True:
#         try:
#             with eventlet.Timeout(1,False):
#                 if not msgnet[self.ID].is_empty():
#                     self.msglist.append(copy.deepcopy(msgnet[self.ID].delq()))
#                     print('id {} received'.format(self.ID))
#                     if flag == 1:
#                         break
#         except eventlet.timeout.Timeout:
#             return
if __name__ == '__main__':
    # q = [qqueue() for i in range(0,10)]
    energy = [1,1,1,1,1,1,1,1,1,1]
    cPower = [1,1,1,1,1,1,1,1,1,1]
    Th_1 = 0.2
    Th_2 = 0.2
    for i in range(0,10):
    #     q[j].addq(j)
    #     print(q[j].is_empty())
    #     print(q[j].delq())
        for j in range(0,9):
            energy[j] = -0.04*i+1+0.02*random.uniform(-1,1)
            cPower[j] = np.random.rand()
        #Em = np.log((math.e-1)*(energy-Th_1)+2-math.e)*(cPower-Th_2)*(len(neigbour)/10)
    #print("{:.2f}".format(energy))
    np.array(energy)
    print(str(np.round(energy,2)))
    e_str = '['
    for i in range(0,9):
        e_str += '{:.2}, '.format(energy[i])
    e_str +=']'
    print(e_str)