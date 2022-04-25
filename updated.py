# -- coding: utf-8 --
import math, sys, pygame, random
from math import *
from pygame import *
import time


#################
# 1. 增加计时
# 2. 更改结构 
# 3. 换个算法 
#################

# if __name__ == '__main__':
#     run_game()


Dijkstra = 1
#模式选择: Dijkstra or Astar
mode = Dijkstra

GAME_LEVEL = 0  #障碍物等级，目前可选项为0或1
delay_sec = 0  #算法延时，单位：秒；可设置延时来观察学习路径规划的逐步实现过程
#颜色RGB值
# grey = (169, 169, 169)
# blue = (0, 0, 255)
# red = (255, 0, 0)
# black = (0, 0, 0)
# green = (0, 255, 0)
# yellow = (255, 255, 0)
# orange = (255, 165, 0)
# bg_color = (255, 255, 255)
# purple = (160, 32, 240)
#初始化相关
pygame.init()
screen = pygame.display.set_mode((1000, 700))
fpsClock = pygame.time.Clock()

#定义Node类，用于存储每个节点信息
class Node(object):
    def __init__(self, point, parent, d, f):
        super(Node, self).__init__()
        self.point = point      #current node
        self.parent = parent    #parent node
        self.d = d      #actual distacne cost from astar point
        self.f = f      #heutrisci distance

#init grid map
def init_grid():
    start_point = [0, 0]
    end_point = [0, 1400]
    i = 10
    while start_point[0] <= 2000:
        pygame.draw.line(screen, (169, 169, 169), start_point, end_point)
        start_point[0] += i
        end_point[0] += i 
    
    start_point = [0, 0]
    end_point = [2000, 0]
    while start_point[1] <= 1400:
        pygame.draw.line(screen, (169, 169, 169), start_point, end_point)
        start_point[1] += i
        end_point[1] += i 

#judge the clicking point
def judge_in_grid(p):
    p0 = int(p[0]/10)
    p1 = int(p[1]/10)
    rect1 = ((p0*10, p1*10), (10,10))
    return rect1

# nitializa obstacles setting
def init_obstacles(configNum):
    global rectObs
    rectObs = []
    if configNum == 0:
        rectObs.append(pygame.Rect((0, 0), (1000, 30)))


        rectObs.append(pygame.Rect((0,40), (30, 490)))


        rectObs.append(pygame.Rect((50, 50), (340, 60)))

        rectObs.append(pygame.Rect((50, 130), (340, 60)))

        rectObs.append(pygame.Rect((50, 210), (340, 60)))

        rectObs.append(pygame.Rect((50, 290), (340, 60)))
        rectObs.append(pygame.Rect((50, 370), (340, 60)))
        rectObs.append(pygame.Rect((50, 450), (340, 60)))
        rectObs.append(pygame.Rect((50, 530), (340, 60)))



        rectObs.append(pygame.Rect((420, 40), (50, 280)))

        rectObs.append(pygame.Rect((530, 40), (50, 280)))

        rectObs.append(pygame.Rect((610, 50), (340, 60)))
        rectObs.append(pygame.Rect((610, 130), (340, 60)))
        rectObs.append(pygame.Rect((610, 210), (340, 60)))

        rectObs.append(pygame.Rect((960, 30), (60, 580)))




        rectObs.append(pygame.Rect((890, 290), (60, 260)))
        rectObs.append(pygame.Rect((810, 290), (60, 260)))

        rectObs.append(pygame.Rect((450, 400), (310, 310)))

        rectObs.append(pygame.Rect((460, 390), (60, 10)))
        rectObs.append(pygame.Rect((470, 380), (50, 10)))
        rectObs.append(pygame.Rect((480, 370), (40, 10)))
        rectObs.append(pygame.Rect((490, 360), (30, 10)))
        rectObs.append(pygame.Rect((500, 350), (20, 10)))
        rectObs.append(pygame.Rect((510, 340), (10, 10)))



        rectObs.append(pygame.Rect((40, 680), (210, 30)))
        rectObs.append(pygame.Rect((250, 670), (220, 40)))

        rectObs.append(pygame.Rect((760, 680), (230, 30)))

    if configNum == 1:
        rectObs.append(pygame.Rect((0, 0), (1000, 20)))
        rectObs.append(pygame.Rect((0, 50), (20, 470)))

        rectObs.append(pygame.Rect((60, 60), (320, 40)))

        rectObs.append(pygame.Rect((60, 140), (320, 40)))
        rectObs.append(pygame.Rect((60, 220), (320, 40)))

        rectObs.append(pygame.Rect((60, 300), (320, 40)))
        rectObs.append(pygame.Rect((60, 380), (320, 40)))
        rectObs.append(pygame.Rect((60, 460), (320, 40)))
        rectObs.append(pygame.Rect((60, 540), (320, 40)))

        rectObs.append(pygame.Rect((430, 50), (30, 240)))

        rectObs.append(pygame.Rect((540, 50), (30, 240)))

        rectObs.append(pygame.Rect((620, 60), (320, 40)))
        rectObs.append(pygame.Rect((620, 140), (320, 40)))
        rectObs.append(pygame.Rect((620, 220), (320, 40)))

        rectObs.append(pygame.Rect((980, 50), (20, 540)))

        rectObs.append(pygame.Rect((900, 300), (40, 240)))
        rectObs.append(pygame.Rect((820, 300), (40, 240)))

        rectObs.append(pygame.Rect((460, 410), (290, 290)))


        rectObs.append(pygame.Rect((470, 400), (40, 10)))
        rectObs.append(pygame.Rect((480, 390), (30, 10)))
        rectObs.append(pygame.Rect((490, 380), (20, 10)))
        rectObs.append(pygame.Rect((500, 370), (10, 10)))

        rectObs.append(pygame.Rect((50, 690), (190, 10)))
        rectObs.append(pygame.Rect((260, 680), (200, 20)))

        rectObs.append(pygame.Rect((770, 690), (210, 10)))

    for rect in rectObs:
        pygame.draw.rect(screen, (0, 0, 0), rect)

#check if point collides with the obstacle
def collides(p):
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            return True
    return False

# reset simulation
def reset():
    screen.fill((255, 255, 255))
    init_grid()
    init_obstacles(GAME_LEVEL)

#test display
def text_display(text0, rect, colour, Size):
    fontObj = pygame.font.Font(None,Size)
    textSurfaceObj = fontObj.render(text0,True,colour)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center=(5+(rect[0][0]),5+(rect[0][1]))
    screen.blit(textSurfaceObj,textRectObj)

#Euclid distance
def Euclid(p1, p2):

    return ((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))**0.5

#Manhattan distance
def Manhattan(p1, p2):

    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

#Astar估算函数
def evaluation_Astar(ynode, goalPoint):
    judge_open = False
    judge_close = False
    if collides(ynode.point) == True:
        return
    # if ynode.point[0] < 0 or ynode.point[1] < 0:
    #     return
    ynode.f = ynode.d*1+0.1*Manhattan(ynode.point, goalPoint.point)
    for p in openlist:
        if p.point == ynode.point:
            judge_open = True
            index_open = openlist.index(p)
    for p in closelist:
        if p.point == ynode.point:
            judge_close = True
            index_close = closelist.index(p)
    if judge_close == True:
        return
    if judge_open == False:
        openlist.append(ynode)
        pygame.draw.rect(screen, (255*abs(1-float(ynode.d)*1.2/140), 255*abs(1-float(ynode.d)*1.2/140), 255), (ynode.point, (10, 10)))
        text_display(str(int(ynode.d)), (ynode.point, (10, 10)), (0, 0, 0), 10)
        pygame.display.flip()
    else:
        if openlist[index_open].d > ynode.d:
            openlist[index_open] = ynode

#Dijkstra估算函数
def evaluation_Dijkstra(ynode, goalPoint):
    judge_open = False
    judge_close = False
    if collides(ynode.point) == True:
        return
    if ynode.point[0] < 0 or ynode.point[1] < 0:
        return
    for p in closelist:
        if p.point == ynode.point:
            judge_close = True
            index_close = closelist.index(p)
    if judge_close == True:
        return
    for p in openlist:
        if p.point == ynode.point:
            judge_open = True
            index_open = openlist.index(p)
    if judge_open == True:
        if openlist[index_open].d > ynode.d:
            openlist[index_open] = ynode
    else:
        openlist.append(ynode)
        pygame.draw.rect(screen, (255*abs(1-float(ynode.d)*1.2/140), 255*abs(1-float(ynode.d)*1.2/140), 255), (ynode.point, (10, 10)))
        text_display(str(ynode.d), (ynode.point, (10, 10)), (0, 0, 0), 10)
        pygame.display.flip()

#程序主要函数
def run_game():
    currentState = 'init'
    initPoseSet = False
    goalPoseSet = False
    global openlist
    openlist = []
    global closelist
    closelist = []
    reset()

    while True:

        #处理不同currentState状态下的工作，其中包括规划路径的实现
        if currentState == 'init':
            pygame.display.set_caption('Select Starting Point and then Goal Point')
            fpsClock.tick(10)
        elif currentState == 'lookingForGoal':
            starttime = time.time()

            run = True
            while(len(openlist) != 0):
                # for event in pygame.event.get():
                #     if event.type == MOUSEBUTTONDOWN :
                #         if run == True:
                #             run = False
                #         else:
                #             run = True
                if run == True:
                    # find the min from priority list

                    xnode = openlist[0]
                    if xnode.point == goalPoint.point:
                        pygame.draw.rect(screen, (255, 165, 0), (xnode.point, (10, 10)))
                        text_display("G",(xnode.point, (10, 10)), (0, 0, 0), 12)
                        currentState = 'goalFound'
                        flag = 1
                        goalNode = xnode

                        # 计时
                        endtime = time.time()
                        print('共用时', round(endtime - starttime, 6))


                        break
                    closelist.append(xnode)
                    del openlist[0]
                    # if delay_sec > 0:
                    #     pygame.draw.circle(screen, (255, 0, 0), (xnode.point[0]+5, xnode.point[1]+5), 2)
                    i = 0
                    while i < 8:
                        if i == 0:
                            ynode = Node((xnode.point[0],xnode.point[1]-10), xnode, xnode.d+1, 0)
                        elif i == 1:
                            ynode = Node((xnode.point[0],xnode.point[1]+10), xnode, xnode.d+1, 0)
                        elif i == 2:
                            ynode = Node((xnode.point[0]-10,xnode.point[1]), xnode, xnode.d+1, 0)
                        elif i == 3:
                            ynode = Node((xnode.point[0]+10,xnode.point[1]), xnode, xnode.d+1, 0)
                        elif i == 4:
                            ynode = Node((xnode.point[0]-10,xnode.point[1]-10), xnode, xnode.d+2, 0)
                        elif i == 5:
                            ynode = Node((xnode.point[0]+10,xnode.point[1]-10), xnode, xnode.d+2, 0)
                        elif i == 6:
                            ynode = Node((xnode.point[0]+10,xnode.point[1]+10), xnode, xnode.d+2, 0)
                        elif i == 7:
                            ynode = Node((xnode.point[0]-10,xnode.point[1]+10), xnode, xnode.d+2, 0)
                        # if mode == 0:
                        #     evaluation_Astar(ynode, goalPoint)
                        if mode == 1:
                            evaluation_Dijkstra(ynode, goalPoint)

                        i += 1
                    for i in range(0, len(openlist)-1):
                        for j in range(0, len(openlist)-1-i):
                            #
                            # if mode == 1:
                            data_j = openlist[j].d
                            data_j1 = openlist[j+1].d
                            if data_j > data_j1:
                                temp = openlist[j]
                                openlist[j] = openlist[j+1]
                                openlist[j+1] = temp
                    pygame.display.flip()

                    ## debug log
                    # for i in range(0, len(openlist)):
                    #     print(str(openlist[i].point)+"\t--- d = "+str(openlist[i].d)+"  &  f = "+str(openlist[i].f))
                    #     print("parent:"+str(openlist[i].parent.point))
                    # print("-------------------")
                    # time.sleep(delay_sec)
                if len(openlist) == 0:
                    print('False to find the path')


        elif currentState == 'goalFound':
            if flag == 1:
                print('goalFound!!!!!!')
                currNode = goalNode.parent
                # print("******************")
                # print("startPoint = "+(str(initialPoint.point)))
                # print("goalPoint = "+(str(goalPoint.point)))
                # print("******************")

                ## debug log

                # for i in range(0, len(closelist)):
                #     print(str(closelist[i].point)+"\t--- d = "+str(closelist[i].d)+"  &  f = "+str(closelist[i].f))
                #     if i > 0:
                #         print("parent:"+str(closelist[i].parent.point))
            while currNode.parent != None:
                pygame.draw.rect(screen, (0, 255, 0), (currNode.point, (10, 10)))
                text_display(str(currNode.d), (currNode.point, (10, 10)), (0, 0, 0), 10)
                currNode = currNode.parent
                flag = 0
                pygame.display.flip()
                # time.sleep(float(delay_sec)/2)
            fpsClock.tick(10)

        #处理鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if currentState == 'init':
                    rect = judge_in_grid(event.pos)
                    if initPoseSet == False:
                        if collides(event.pos) == False:
                            initialPoint = Node(rect[0], None, 0, 0)
                            
                            pygame.draw.rect(screen, (255, 0, 0), rect)
                            text_display("S",rect, (0, 0, 0), 20)
                            initPoseSet = True
                    elif  goalPoseSet == False:
                        if collides(event.pos) == False:
                            if rect[0] != initialPoint.point:
                                goalPoint = Node(rect[0],None, 0, 0)
                                print("******************")
                                print("startPoint = "+(str(initialPoint.point)))
                                print("goalPoint = "+(str(goalPoint.point)))
                                print("******************")
                                if mode == 0:
                                    initialPoint.f = initialPoint.d+0.1*Manhattan(goalPoint.point, initialPoint.point)
                                openlist.append(initialPoint)
                                pygame.draw.rect(screen, (255, 165, 0), rect)
                                text_display("G",rect, (0, 0, 0), 20)
                                goalPoseSet = True
                                currentState = 'lookingForGoal'
                else:
                    currentState = 'init'
                    initPoseSet = False
                    goalPoseSet = False
                    openlist = []
                    closelist = []
                    reset()
        init_grid()
        pygame.display.flip()
        
if __name__ == '__main__':
    run_game()
