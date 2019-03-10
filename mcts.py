import math
from gameboard import Gameboard
import random

#树结点
class TreeNode():

    #初始化
    def __init__(self,parent=None,action=None):
        self.children = []  #孩子结点
        self.parent = parent  #父母
        self.action = action  #行动
        self.visit_count = 0  #访问次数
        self.action_value = 0.0  #行动分数
        self.valid_choice = []  #合法走法
        self.child_visit_index = []  #访问过的孩子下标，方便计算

    #将另一个结点的信息复制给当前结点
    def copy(self,children,parent,action,visit_count,action_value,valid_choice):
        self.children = children
        self.parent = parent
        self.action = action
        self.visit_count = visit_count
        self.action_value = action_value
        self.valid_choice = valid_choice

    #判断当前结点是否为叶子结点
    def is_leaf(self):
        #如果当前没有孩子，返回正确
        if len(self.children) == 0:
            return True
        #如果有孩子，证明不是叶子结点
        return False
    
    #插入新结点
    def insert_new_child(self,sub_node):
        sub_node.parent = self #设置父母
        self.children.append(sub_node)  #添加结点入孩子列表

    #判断是否完全扩展
    def is_total_expand(self):
        #如果该结点的所有孩子结点都已经被访问，则相当于完全扩展
        if len(self.valid_choice) == len(self.children) and len(self.children) != 0:
            return True
        return False

 
#蒙特卡罗搜索树
class MonteCarloTreeSearch():
    #初始化
    def __init__(self,mark,anti_mark,gameboard,size,weights,node,iter1):
        self.turn = 0  #轮流顺序
        self.chess = {0:mark,1:anti_mark}  #棋子颜色
        self.gameboard = gameboard  #棋盘对象
        self.size = size  #棋盘大小
        self.ele_weights = weights  #权重
        self.iter = iter1  #迭代次数
        self.node = node  #结点
        self.constant = 1 / math.sqrt(2.0)  #常数

    #搜索实现
    def search(self):
        #进行多次迭代
        for i in range(self.iter):
            self.turn = 0  #轮流顺序
            self.depth = 10  #深度
            #复制棋盘，防止影响原来的状态
            gameboard = Gameboard()
            gameboard.board = []
            #复制每一个位置
            for i in range(self.size):
                tmp = [x for x in self.gameboard.board[i]]
                gameboard.board.append(tmp)
            #选择并扩展一个结点
            select_node = self.selection_expansion(self.node,gameboard)

            #进行模拟
            action_value = self.simulation(select_node,gameboard)

            #回溯更新行动值和访问次数
            self.back_propagation(select_node,action_value)
        #得到最好的行动步骤
        best_action = self.choose_best_action(self.node)
        return best_action

    #选择并且扩展结点
    def selection_expansion(self,node,gameboard):
        #直到终点为止
        while gameboard.is_over() != True:
            #如果子结点已经全部被扩展
            if node.is_total_expand() == True:
                #选择最好的子结点
                node = self.get_best_child(node)
                #根据当前选择的子结点下子
                gameboard.move(self.chess[self.turn],node.action)
                #改变角色
                self.turn = (self.turn+1) % 2 
            #如果是叶子结点
            elif node.is_leaf() == True:      
                #找出合法下子的所有坐标          
                valid_choice = self.gameboard.find_right_flipping_position(self.chess[self.turn])
                #如果当前没法下子，直接返回
                if len(valid_choice) == 0:
                    return None
                #更新当前结点的子结点下子选择列表
                node.valid_choice = valid_choice
                #扩展新的子结点
                new_sub_node = self.expansion(node)
                #下子
                gameboard.move(self.chess[self.turn],new_sub_node.action)
                #改变角色
                self.turn = (self.turn+1) % 2
                #返回选中的子结点
                return new_sub_node
            else:
                #扩展新的子结点
                new_sub_node = self.expansion(node)
                #下子
                gameboard.move(self.chess[self.turn],new_sub_node.action)
                #改变角色
                self.turn = (self.turn+1) % 2
                return new_sub_node
        #返回结点
        return node

    #模拟
    # def simulation(self,node,gameboard):
    #     #搜索到最低
    #     while gameboard.is_over() != True :
    #         #搜索合法走法
    #         valid_choice = gameboard.find_right_flipping_position(self.chess[self.turn])
    #         #如果当前没有合法走法，则换到另一方下子
    #         if len(valid_choice) == 0:
    #             self.turn = (self.turn+1) % 2
    #             continue
    #         #随机得到一个合法走子
    #         index = random.randint(0,len(valid_choice)-1)
    #         #得到行动步骤
    #         action = valid_choice[index]
    #         #下子
    #         gameboard.move(self.chess[self.turn],action)
    #         #转换角色
    #         self.turn = (self.turn+1) % 2

    #     #统计最终的得分差
    #     x_count,o_count,empty_count = gameboard.count_num()
    #     if self.chess[0] == 'X':
    #         if x_count > o_count:
    #             final_reward = 2
    #         else:
    #             final_reward = -2
    #     else:
    #         if x_count > o_count:
    #             final_reward = -2
    #         else:
    #             final_reward = 2
    #     return final_reward

    #模拟
    def simulation(self,node,gameboard):
        #搜索到最低或到指定深度
        while gameboard.is_over() != True and self.depth >= 0:
            #搜索合法走法
            valid_choice = gameboard.find_right_flipping_position(self.chess[self.turn])
            #如果当前没有合法走法，则换到另一方下子
            if len(valid_choice) == 0:
                self.turn = (self.turn+1) % 2
                continue
            #随机得到一个合法走子
            index = random.randint(0,len(valid_choice)-1)
            #得到行动步骤
            action = valid_choice[index]
            #下子
            gameboard.move(self.chess[self.turn],action)
            #转换角色
            self.turn = (self.turn+1) % 2
            #深度减一
            self.depth -= 1

        #使用评估函数评估当前得分
        final_reward = self.evaluation_best(self.chess[0],gameboard)    

        return final_reward

    #回溯
    def back_propagation(self,select_node,action_value):
        #回溯，直到父结点为空
        while select_node != None:
            #访问次数加一
            select_node.visit_count += 1
            #行动值增加
            select_node.action_value += action_value
            #向上追溯
            select_node = select_node.parent 

    #选择最好的子结点，使用UCB评判方式
    def get_best_child(self,node):
        optimal_score = -10000
        optimal_son_node = None
        #遍历所有子结点，找出最优的
        for son_node in node.children:
            #公式前半部分，平均行动力
            value1 = son_node.action_value / son_node.visit_count
            #公式后半部分，加入访问次数限制，优先访问已访问次数少的
            value2 = (math.log(node.visit_count)*2.0) / son_node.visit_count
            tmp_score = value1 + self.constant*math.sqrt(value2)
            #如果找到更优的值，进行更新
            if tmp_score > optimal_score:
                optimal_score = tmp_score
                optimal_son_node = son_node
        #返回最优子结点
        return optimal_son_node

    #选择最优的行动步骤
    def choose_best_action(self,node):
        optimal_score = -10000
        optimal_son_node = None
        #遍历所有子结点
        for son_node in node.children:
            value = son_node.action_value / son_node.visit_count
            # print(value)
            if value > optimal_score:
                optimal_score = value
                optimal_son_node = son_node
        #如果没有子结点，返回None
        if optimal_son_node == None:
            return None 
        #返回最优下子坐标
        return optimal_son_node.action
    
    #扩展新的子结点
    def expansion(self,node):
        #合法下子列表
        length = len(node.valid_choice)
        #循环
        while True:
            #随机得到一个下子下标
            index = random.randint(0,length-1)
            #如果没有扩展过，则跳出，否则一直随机找下标
            if index not in node.child_visit_index:
                break
        #添加下子访问下标列表
        node.child_visit_index.append(index)
        #创建新的结点
        new_node = TreeNode(node,node.valid_choice[index])
        #加入到父结点的子结点列表
        node.children.append(new_node)
        return new_node

    #综合考虑棋子各个位置不同情况、棋子数目差、棋子行动力
    def evaluation_best(self,mark,gameboard):


        chess_num = 0
        out_corner,out_edge,inner_corner,inner_edge = 0,0,0,0
        for i in range(self.size):
            for j in range(self.size):
                if gameboard.board[i][j] == '.':
                    continue
                amount = 1 if gameboard.board[i][j] == mark else -1
                chess_num += amount
                #计算最外层边的情况，四个角和四条边的情况
                if i == 0 or j == 0 or i == self.size-1 or j == self.size-1:
                    if (i == 0 and j == 0) or (i == 0 and j == self.size-1) or (i == self.size-1 and j == 0) or (i == self.size-1 and j == self.size-1):
                        out_corner += amount
                    else:
                        out_edge += amount

                #计算上下从外往内第二层的边
                elif i == 1 or i == self.size-2 and (j > 1 and j < self.size-2):
                    x = self.size-1 if i == self.size-2 else 0
                    for k in range(j-1,j+2):
                        if gameboard.board[x][k] == '.':
                            inner_edge += amount


                #计算左右从外往内第二层的边
                elif j == 1 or j == self.size-2 and (i > 1 and i < self.size-2):
                    y = self.size-1 if j == self.size-2 else 0
                    for k in range(i-1,i+2):
                        if gameboard.board[k][y] == '.':
                            inner_edge += amount

                #内层左上角
                elif j == 1 and i == 1:
                    if gameboard.board[0][0] == '.':
                        inner_corner += amount
                    for k in range(1,3):
                        if gameboard.board[k][0] == '.':
                            inner_edge += amount
                    for k in range(1,3):
                        if gameboard.board[0][k] == '.':
                            inner_edge += amount

                #内层右上角
                elif j == self.size-2 and i == 1:
                    if gameboard.board[0][self.size-1] == '.':
                        inner_corner += amount
                    for k in range(1,3):
                        if gameboard.board[k][self.size-1] == '.':
                            inner_edge += amount
                    for k in range(j-1,j+1):
                        if gameboard.board[0][k] == '.':
                            inner_edge += amount

                #内层左下角
                elif j == 1 and i == self.size-2:
                    if gameboard.board[self.size-1][0] == '.':
                        inner_corner += amount
                    for k in range(i-1,i+1):
                        if gameboard.board[k][0] == '.':
                            inner_edge += amount
                    for k in range(1,3):
                        if gameboard.board[self.size-1][k] == '.':
                            inner_edge += amount

                #内层右下角
                elif j == self.size-2 and i == self.size-2:
                    if gameboard.board[self.size-1][self.size-1] == '.':
                        inner_corner += amount
                    for k in range(i-1,i+1):
                        if gameboard.board[k][self.size-1] == '.':
                            inner_edge += amount
                    for k in range(j-1,j+1):
                        if gameboard.board[self.size-1][k] == '.':
                            inner_edge += amount


        #行动力
        valid_position = gameboard.find_right_flipping_position(mark)
        action_num = len(valid_position)

        #最终分数
        final_score = out_corner*self.ele_weights[0] + out_edge*self.ele_weights[1] + inner_corner*self.ele_weights[2] + inner_edge*self.ele_weights[3] + chess_num*self.ele_weights[4] + action_num*self.ele_weights[5]


        return final_score

