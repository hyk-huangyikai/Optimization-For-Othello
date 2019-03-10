from gameboard import Gameboard
#AI玩家对象
class AI2():
    #初始化
    def __init__(self,mark,gameboard,ele_weights):
        self.id = 0
        self.mark = mark #标记
        self.gameboard = gameboard  #游戏板
        self.size = len(gameboard.board)  #规模
        #各个位置权重
        # self.pos_weight = [
        #     [120, -10, 10 , 10, -10, 120],
        #     [-10, -20, 5, 5, -20, -10],
        #     [10, 5, 5, 5, 5, 10],
        #     [10, 5, 5, 5, 5, 10],
        #     [-10, -20, 5, 5, -20, -10],
        #     [120, -10, 10, 10, -10, 120]
        # ]
        self.pos_weight = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]
        self.pos_imt = [(0,0),(0,5),(5,0),(5,5)]

        self.ele_weights = ele_weights

        #对手的棋子标记
        if self.mark == 'O':
            self.anti_mark = 'X'
        else:
            self.anti_mark = 'O'

    #根据棋子个数差表示的评估函数
    def evaluation_score(self):
        score1 = 0
        score2 = 0
        for i in range(self.size):
            for j in range(self.size):
                #如果是对手棋子，对方分数加1
                if self.gameboard.board[i][j] == self.anti_mark:
                    score2 += 1
                #如果是对手棋子，自己分数加1
                elif self.gameboard.board[i][j] == self.mark:
                    score1 += 1
        #用自己分数减去对方分数的结果作为评估函数的分数
        return score1 - score2

    #根据位置权重的评估函数
    def evaluation_pos_weight(self):
        #统计分数
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                #如果是对方棋子，减去当前位置的权重
                if self.gameboard.board[i][j] == self.anti_mark:
                    score -= self.pos_weight[i][j]
                #如果是本方棋子，加上当前位置的权重
                elif self.gameboard.board[i][j] == self.mark:
                    score += self.pos_weight[i][j]
        #以最终的权重作为评估函数的结果
        return score

    #综合各个因素的评估函数
    def evaluation_Comprehensive(self):
        pos_score = 0
        num1 = 0
        num2 = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.gameboard.board[i][j] == self.anti_mark:
                    pos_score -= self.pos_weight[i][j]
                    num2 += 1
                elif self.gameboard.board[i][j] == self.mark:
                    pos_score += self.pos_weight[i][j]
                    num1 += 1
        num_score = num1 - num2

        valid_position = self.gameboard.find_right_flipping_position(self.mark)
        action_score = len(valid_position)

        my_stabilizer = 0
        opp_stabilizer = 0
        if self.gameboard.board[0][0] == self.mark:
            my_stabilizer += 1
        elif self.gameboard.board[0][0] == self.anti_mark:
            opp_stabilizer += 1
        if self.gameboard.board[0][self.size-1] == self.mark:
            my_stabilizer += 1
        elif self.gameboard.board[0][self.size-1] == self.anti_mark:
            opp_stabilizer += 1
        if self.gameboard.board[self.size-1][0] == self.mark:
            my_stabilizer += 1
        elif self.gameboard.board[self.size-1][0] == self.anti_mark:
            opp_stabilizer += 1
        if self.gameboard.board[self.size-1][self.size-1] == self.mark:
            my_stabilizer += 1
        elif self.gameboard.board[self.size-1][self.size-1] == self.anti_mark:
            opp_stabilizer += 1

        weights = [10, 10, 10, 100]
        total_score = pos_score * weights[0] + num_score * weights[1] + action_score * weights[2] + (my_stabilizer - opp_stabilizer) * weights[3]

        if self.gameboard.board[1][1] == self.mark:
            total_score -= 32
        elif self.gameboard.board[1][1] == self.anti_mark:
            total_score += 32
        if self.gameboard.board[1][4] == self.mark:
            total_score -= 32
        elif self.gameboard.board[1][4] == self.anti_mark:
            total_score += 32
        if self.gameboard.board[4][1] == self.mark:
            total_score -= 32
        elif self.gameboard.board[4][1] == self.anti_mark:
            total_score += 32
        if self.gameboard.board[4][4] == self.mark:
            total_score -= 32
        elif self.gameboard.board[4][4] == self.anti_mark:
            total_score += 32

        return total_score

    # 综合考虑棋子各个位置不同情况、棋子数目差、棋子行动力
    def evaluation_best(self):
        chess_num = 0
        out_corner, out_edge, inner_corner, inner_edge = 0, 0, 0, 0
        for i in range(self.size):
            for j in range(self.size):
                if self.gameboard.board[i][j] == '.':
                    continue
                amount = 1 if self.gameboard.board[i][j] == self.mark else -1
                chess_num += amount
                # 计算最外层边的情况，四个角和四条边的情况
                if i == 0 or j == 0 or i == self.size - 1 or j == self.size - 1:
                    if (i == 0 and j == 0) or (i == 0 and j == self.size - 1) or (
                            i == self.size - 1 and j == 0) or (i == self.size - 1 and j == self.size - 1):
                        out_corner += amount
                    else:
                        out_edge += amount

                # 计算上下从外往内第二层的边
                elif i == 1 or i == self.size - 2 and (j > 1 and j < self.size - 2):
                    x = self.size - 1 if i == self.size - 2 else 0
                    for k in range(j - 1, j + 2):
                        if self.gameboard.board[x][k] == '.':
                            inner_edge += amount


                # 计算左右从外往内第二层的边
                elif j == 1 or j == self.size - 2 and (i > 1 and i < self.size - 2):
                    y = self.size - 1 if j == self.size - 2 else 0
                    for k in range(i - 1, i + 2):
                        if self.gameboard.board[k][y] == '.':
                            inner_edge += amount

                # 内层左上角
                elif j == 1 and i == 1:
                    if self.gameboard.board[0][0] == '.':
                        inner_corner += amount
                    for k in range(1, 3):
                        if self.gameboard.board[k][0] == '.':
                            inner_edge += amount
                    for k in range(1, 3):
                        if self.gameboard.board[0][k] == '.':
                            inner_edge += amount

                # 内层右上角
                elif j == self.size - 2 and i == 1:
                    if self.gameboard.board[0][self.size - 1] == '.':
                        inner_corner += amount
                    for k in range(1, 3):
                        if self.gameboard.board[k][self.size - 1] == '.':
                            inner_edge += amount
                    for k in range(j - 1, j + 1):
                        if self.gameboard.board[0][k] == '.':
                            inner_edge += amount

                # 内层左下角
                elif j == 1 and i == self.size - 2:
                    if self.gameboard.board[self.size - 1][0] == '.':
                        inner_corner += amount
                    for k in range(i - 1, i + 1):
                        if self.gameboard.board[k][0] == '.':
                            inner_edge += amount
                    for k in range(1, 3):
                        if self.gameboard.board[self.size - 1][k] == '.':
                            inner_edge += amount

                # 内层右下角
                elif j == self.size - 2 and i == self.size - 2:
                    if self.gameboard.board[self.size - 1][self.size - 1] == '.':
                        inner_corner += amount
                    for k in range(i - 1, i + 1):
                        if self.gameboard.board[k][self.size - 1] == '.':
                            inner_edge += amount
                    for k in range(j - 1, j + 1):
                        if self.gameboard.board[self.size - 1][k] == '.':
                            inner_edge += amount

        # 行动力
        valid_position = self.gameboard.find_right_flipping_position(self.mark)
        action_num = len(valid_position)

        # 最终分数
        final_score = out_corner * self.ele_weights[0] + out_edge * self.ele_weights[1] + inner_corner * \
                      self.ele_weights[2]
        + inner_edge * self.ele_weights[3] + chess_num * self.ele_weights[4] + action_num * self.ele_weights[5]

        return final_score

    #极大极小值，alpha、beta剪枝
    def minimax_alpha_beta(self,opponent,depth,my_score,opponent_score):
        #如果深度为0，返回当前状态评估函数的值
        if (depth == 0):
            # score = self.evaluation_score()
            # score = self.evaluation_pos_weight()
            # score = self.evaluation_Comprehensive()
            score = self.evaluation_best()
            return score,None
        #求出当前状态的所有的合法位置
        valid_flipping_position = self.gameboard.find_right_flipping_position(self.mark)
        #如果没有可以下子的合法位置，返回当前状态的评估函数的值
        if (len(valid_flipping_position) == 0) :
            # score = self.evaluation_score()
            # score = self.evaluation_pos_weight()
            # score = self.evaluation_Comprehensive()
            score = self.evaluation_best()
            return score, None
        #令当前最好的分数值等于本方的分数值
        best_score = my_score
        #初始化最好下一步下子步骤
        best_next_step = None
        #对于所有合法位置进行遍历
        for step in valid_flipping_position:
            #下子，并且返回所有翻子的下标
            flipping_pieces_list = self.gameboard.move(self.mark,step)
            #递归调用下一层，由于是极大极小值算法，因此是对方opponent对象调用该函数，同时opponent_score、my_score取负号交换传参
            score,next_step = opponent.minimax_alpha_beta(self,depth-1,-1*opponent_score,-1*my_score)
            #回溯恢复到下子之前的步骤
            self.gameboard.un_move(self.mark,step,flipping_pieces_list)

            #由于下一层的策略是相反的，因此需要去负号
            score = (-1) * score
            #如果分数大于当前最好的分数
            if score > best_score:
                best_score = score #更新最好的分数值
                best_next_step = step #更新最佳下一步的下子步骤

            #如果alpha>beta，进行剪枝
            if best_score > opponent_score:
                break
        #返回最佳分数、最佳下子步骤
        return best_score,best_next_step

    #极大极小值算法
    def minimax(self,opponent,depth):
        #如果深度为0，返回当前状态的评估函数值
        if (depth == 0):
            score = self.evaluation_pos_weight()
            return score,None
        #找出所有可以下子的合法位置
        valid_flipping_position = self.gameboard.find_right_flipping_position(self.mark)
        #如果不存在可以下子的合法位置，则返回当前状态的评估函数值
        if (len(valid_flipping_position) == 0) :
            score = self.evaluation_pos_weight()
            return score, None

        best_score = -99999  #最佳评估值
        best_next_step = None  #最佳下子位置
        #遍历所有合法下子位置
        for step in valid_flipping_position:
            #下子，并返回所有翻子的位置
            flipping_pieces_list = self.gameboard.move(self.mark,step)
            #递归调用该算法
            score,next_step = opponent.minimax(self,depth-1)
            #回溯，撤销下子，并且将翻子的所有位置恢复
            self.gameboard.un_move(self.mark,step,flipping_pieces_list)
            #由于极大极小值算法相邻层追求最优相反，因此从下层返回的score需要取反，让同一层取得最优
            score = (-1) * score
            #如果当前分数大于最佳分数，更新最佳分数和最佳下子步骤
            if score > best_score:
                best_score = score
                best_next_step = step
        #返回最佳分数、最佳下子步骤
        return best_score,best_next_step
    #决策
    def decision_making(self,level):
        # print("It turns to AI player  [2]  .")

        for pos in self.pos_imt:
            if pos in self.gameboard.find_right_flipping_position(self.mark):
                return pos

        #生成一个虚拟的对手，进行训练
        opponent = AI2(self.anti_mark,self.gameboard,self.ele_weights)
        # best_score,next_step = self.minimax(opponent,4)
        #调用极大极小算法
        best_score,next_step = self.minimax_alpha_beta(opponent,4,-1*float('inf'),float('inf'))
        #返回最佳的下子步骤
        return next_step

    def player_move(self,next_step):
        self.gameboard.move(self.mark,next_step)