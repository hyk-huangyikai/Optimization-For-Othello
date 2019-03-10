import sys
import time
import numpy as np

#游戏板
class Gameboard():

    #初始化棋盘
    def __init__(self):
        self.size = 8
        self.space = '.'  #棋盘为空的标记
        self.board = []
        for i in range(self.size):
            tmp = [self.space] * self.size
            self.board.append(tmp)
        self.board[3][3] = 'O'
        self.board[4][4] = 'O'
        self.board[3][4] = 'X'
        self.board[4][3] = 'X'

    #判断是否已经结束
    def is_over(self):
        n1 = self.find_right_flipping_position('X')
        n2 = self.find_right_flipping_position('O')
        #如果双方都没有可以走下一步的位置，则说明游戏结束
        if len(n1) == 0 and len(n2) == 0:
            return True
        return False

    #得出胜利者
    def winner(self):
        x_count = 0
        o_count = 0
        #计算白琪和黑棋的个数
        for i in range(self.size):
            for j in range(self.size):
                #黑棋个数+1
                if self.board[i][j] == 'X':
                    x_count += 1
                #白琪个数+1
                elif self.board[i][j] == 'O':
                    o_count += 1
        #黑棋胜利
        if x_count > o_count:
            return 0
        #平局
        elif x_count == o_count:
            return 1
        #白琪胜利
        else:
            return 2

    #打印棋盘
    def print_state(self):
        print(' ',' '.join(list('12345678')))
        for i in range(self.size):
            print(i + 1, ' '.join(self.board[i]))

    #打印棋盘状态
    def print_state_ts(self,mark):
        board = []
        #得出当前可以下子的合法位置
        valid_position = self.find_right_flipping_position(mark)
        #复制棋盘，防止后面操作改变原来的棋盘
        for i in range(self.size):
            tmp = []
            for j in range(self.size):
                tmp.append(self.board[i][j])
            board.append(tmp)
        #将合法位置改为'+'
        for i in range(len(valid_position)):
            x = valid_position[i][0]
            y = valid_position[i][1]
            board[x][y] = '+'
        #打印棋盘
        print(' ', ' '.join(list('12345678')))
        for i in range(self.size):
            print(i + 1, ' '.join(board[i]))

    #放棋子
    def move(self,mark,next_step):
        self.board[next_step[0]][next_step[1]] = mark #下子
        flipping_pieces_list = self.flipping_pieces(mark,next_step)  #将所有可以翻的位置都进行翻子
        return flipping_pieces_list #返回翻子的二维坐标的列表，方便后面回溯恢复

    #翻子
    def flipping_pieces(self,mark,next_step):

        flipping_list = []
        #检查当前位置的各方向
        for direction_line in self.direction_lines(next_step):
            for i,j in enumerate(direction_line):
                #找到相同颜色的，将前面探索的位置放进队列
                if self.board[j[0]][j[1]] == mark:
                    flipping_list.extend(direction_line[:i])
                    break
                #遇到空位，结束探索
                elif self.board[j[0]][j[1]] == self.space:
                    break
        #对所有可以翻子的位置进行翻子
        for i in range(len(flipping_list)):
            self.board[flipping_list[i][0]][flipping_list[i][1]] = mark

        return flipping_list


    #回溯，撤销放棋子
    def un_move(self,mark,next_step,flipping_list):
        if mark == 'X':
            anti_mark = 'O'
        else:
            anti_mark = 'X'
        #将下子的位置恢复原状
        self.board[next_step[0]][next_step[1]] = self.space
        #将所有翻子的位置恢复原状
        for i in range(len(flipping_list)):
            self.board[flipping_list[i][0]][flipping_list[i][1]] = anti_mark

    #检查是否有棋子可以翻
    def is_fipping(self,mark,next_step):
        flipping_list = []
        #检查当前位置的各个方向
        for direction_line in self.direction_lines(next_step):
            for i, j in enumerate(direction_line):
                #遇到相同子，结束，将之前探索的点放进队列
                if self.board[j[0]][j[1]] == mark:
                    flipping_list.extend(direction_line[:i])
                    break
                #遇到空格，结束探索
                elif self.board[j[0]][j[1]] == self.space:
                    break
        #如果有合适位置，则返回True
        if len(flipping_list) > 0:
            return True
        else:
            return False

    #找到所有合法的放棋子位置
    def find_right_flipping_position(self,mark):
        if mark == 'X':
            anti_mark = 'O'
        else:
            anti_mark = 'X'
        #8个方向
        move_direct = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        valid_flipping_position = []
        for i in range(self.size):
            for j in range(self.size):
                #找到相同颜色的子，进行下一步探索
                if self.board[i][j] == anti_mark:
                    for move in move_direct:
                        x = i + move[0]
                        y = j + move[1]
                        #检查合法性
                        if x < self.size and x >= 0 and y < self.size and y >= 0 and self.board[x][y] == self.space and (x,y) not in valid_flipping_position:
                            next_step = (x,y)
                            #检查是否能够翻子，可以说明合法
                            if self.is_fipping(mark,next_step) == True:
                                valid_flipping_position.append((x,y))

        return valid_flipping_position


    #八个方向的数组
    def direction_lines(self,next_step):
        x = next_step[0]
        y = next_step[1]
        board_array = []
        for i in range(self.size):
            tmp = []
            for j in range(self.size):
                tmp.append((i,j))
            board_array.append(tmp)
        #左右方向
        left = board_array[x][0:y]
        right = board_array[x][y+1:]
        top = []
        for i in range(x):
            top.append(board_array[i][y])

        bottom = []
        for i in range(x+1,self.size,1):
            bottom.append(board_array[i][y])
        #4个斜方向
        x1 = x-1
        y1 = y+1
        right_top = []
        while x1 >= 0 and y1 < self.size:
            right_top.append(board_array[x1][y1])
            x1 = x1-1
            y1 = y1+1

        x1 = x + 1
        y1 = y + 1
        right_bottom = []
        while x1 < self.size and y1 < self.size:
            right_bottom.append(board_array[x1][y1])
            x1 = x1+1
            y1 = y1+1

        x1 = x-1
        y1 = y-1
        left_top = []
        while x1 >= 0 and y1 >= 0:
            left_top.append(board_array[x1][y1])
            x1 = x1-1
            y1 = y1-1

        x1 = x + 1
        y1 = y - 1
        left_bottom = []
        while x1 < self.size and y1 >= 0:
            left_bottom.append(board_array[x1][y1])
            x1 = x1+1
            y1 = y1-1

        left = list(reversed(left))
        top = list(reversed(top))

        # print(left,right,top,bottom,right_top,right_bottom,left_top,left_bottom)
        #存储8个方向的列表
        direction_lines = [left,right,top,bottom,right_top,right_bottom,left_top,left_bottom]
        # print(direction_lines)
        return direction_lines

    def count_num(self):
        x_count = 0
        o_count = 0
        empty_count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'X':
                    x_count += 1
                elif self.board[i][j] == 'O':
                    o_count += 1
                else:
                    empty_count += 1

        return x_count,o_count,empty_count

if __name__ == "__main__":
    gameboard = Gameboard()
    gameboard.print_state()
    gameboard.direction_lines((2,3))
