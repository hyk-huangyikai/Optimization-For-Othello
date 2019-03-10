import time
from gameboard import Gameboard
from gamePlayer import Human,AI
from player2 import AI2


def main():
    #游戏板对象
    gameboard = Gameboard()
    ele_weight = [15,6,-8,-4,2,2]
    #提示输入信息
    while True:
        print("please select character: 0 - AI  1 - human ")
        print("format: 0 1 or 1 0 or 1 1 or 0 0") #按照输入格式顺序
        print("(The input order represents the order of the chess)")
        input1 = input()
        input2 = input1.split()#处理输入格式
        n1 = int(input2[0])
        n2 = int(input2[1])
        #人类与人类pk
        if n1 == 1 and n2 == 1:
            player1 = Human('X',gameboard)
            player2 = Human('O',gameboard)
            break
        else:
            #先手AI，后手人类
            if n1 == 0 and n2 == 1:
                player1 = AI('X',gameboard,ele_weight)
                player2 = Human('O',gameboard)
                break
            #先手人类，后手AI
            elif n1 == 1 and n2 == 0:
                player1 = Human('X',gameboard)
                player2 = AI('O',gameboard,ele_weight)
                break
            #AI与AIpk
            elif n1 == 0  and n2 == 0:
                player1 = AI('X',gameboard,ele_weight)
                player2 = AI2('O',gameboard,ele_weight)
                # player1 = AI2('X', gameboard)
                # player2 = AI('O', gameboard)
                break
            else:
                #格式错误，重新输入
                print("The format is wrong")

    print("Game start!")
    start1 = time.clock()
    gameboard.print_state() #输出初始状态
    current_player = player1  #当前玩家
    id = 0
    level = 1
    while True:
        start = time.clock()
        next_step = current_player.decision_making(level) #当前玩家做出决策
        #如果没有选择，则只能等待其他玩家下子
        if next_step is None:
            print("                              No step to select,pass!!!!!!!!!")
            print('-----------')
            print('-----------')
        else:
            print_step = (next_step[0] + 1,next_step[1] + 1)  #下子位置
            print("move step: ",print_step) #输出下子位置
            gameboard.move(current_player.mark,next_step) #下子
            # gameboard.print_state()
            x_count, o_count, empty_count = gameboard.count_num()
            print('X:', x_count, ' O:', o_count, ' Empty:', empty_count)
            if current_player.id == 0:
                print('score: ',current_player.evaluation_Comprehensive())
            gameboard.print_state_ts(current_player.anti_mark) #输出下子后的棋盘状态
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
        end = time.clock()
        level += 1
        print("time: ",(float)(end - start),'s')

    print("Game Over!!!")
    result = gameboard.winner() #得出结局
    #先手胜利
    if result == 0:
        print("Player1 Win!!!")
    #平局
    elif result == 1:
        print("Draw!!!")
    #后手胜利
    else:
        print("Player2 Win!!!")

    x_count, o_count, empty_count = gameboard.count_num()
    print('X:', x_count, ' O:', o_count, ' Empty:', empty_count)

    end1 = time.clock()
    print("Total time: ",(float)(end1 - start1),'s')



if __name__ == "__main__":
    main()