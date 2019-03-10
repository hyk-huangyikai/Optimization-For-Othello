import time
from gameboard import Gameboard
from gamePlayer import Human,AI
from player2 import AI2

def chess_game(weight1,weight2):
    gameboard = Gameboard()
    player1 = AI('X',gameboard,weight1)
    player2 = AI('O',gameboard,weight2)
    # player2 = AI('O',gameboard,weight2)
    # start1 = time.clock()
    # gameboard.print_state() #输出初始状态
    current_player = player1  #当前玩家
    id = 0
    level = 1
    while True:
        next_step = current_player.decision_making(level) #当前玩家做出决策
        #如果没有选择，则只能等待其他玩家下子
        if next_step is None:
            # print("                              No step to select,pass!!!!!!!!!")
            # print('-----------')
            # print('-----------')
            #判断游戏是否结束
            if gameboard.is_over():
                break
            #切换状态
            if id == 0:
                current_player = player2
                id = (id+1)%2
            else:
                current_player = player1
                id = (id+1)%2
            level += 1
        else:
            # print_step = (next_step[0] + 1,next_step[1] + 1)  #下子位置
            # print("move step: ",print_step) #输出下子位置
            gameboard.move(current_player.mark,next_step) #下子
            # gameboard.print_state()
            # x_count, o_count, empty_count = gameboard.count_num()
            # print('X:', x_count, ' O:', o_count, ' Empty:', empty_count)
            # if current_player.id == 0:
                # print('score: ',current_player.evaluation_Comprehensive())
            # gameboard.print_state_ts(current_player.anti_mark) #输出下子后的棋盘状态
            #判断游戏是否结束
            if gameboard.is_over():
                break
            #切换状态
            if id == 0:
                current_player = player2
                id = (id+1)%2
            else:
                current_player = player1
                id = (id+1)%2
            level += 1

    # print("Game Over!!!")
    # result = gameboard.winner() #得出结局
    # #先手胜利
    # if result == 0:
    #     print("Player1 Win!!!")
    # #平局
    # elif result == 1:
    #     print("Draw!!!")
    # #后手胜利
    # else:
    #     print("Player2 Win!!!")

    x_count, o_count, empty_count = gameboard.count_num()
    # print('X:', x_count, ' O:', o_count, ' Empty:', empty_count)
    # gameboard.print_state_ts(current_player.anti_mark) #输出下子后的棋盘状态
    # end1 = time.clock()
    # print("Total time: ",(float)(end1 - start1),'s')

    return (x_count,o_count)


def main():
    #游戏板对象
    iter1 = 1
    while (iter1):
        # x_count,o_count = chess_game([15,6,-8,-4,2,2],[5,5,-10,-4,4,4])
        # print("---------------------------------------")
        # print(x_count,o_count)
        x_count,o_count = chess_game([5,5,-10,-4,4,4],[15,6,-8,-4,2,2])
        print("---------------------------------------")
        print(x_count,o_count)
        iter1 -= 1



if __name__ == "__main__":
    main()