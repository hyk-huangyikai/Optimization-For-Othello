import math
import time
import numpy as np 
import random
from train_main import chess_game

MUTATION_RATE = 0.5

#遗传算法
class GeneticAlgorithm():

    #初始化
    def __init__(self,population_size,individuals_size,iter_size):
        self.population_size = population_size #种群数量
        self.individuals_size = individuals_size  #个体大小
        self.popul = []  #种群，存储各个个体，每个个体是一个权值列表
        self.fit_score = []  #适应度列表
        self.iter_size = iter_size  #迭代次数
        self.negative = [2,3]  #负数参数列表
        #初始化
        # for k in range(self.population_size):
        #     individuals = np.random.random(self.individuals_size)
        #     individuals = list(individuals)
        #     #更新负数
        #     for ne in self.negative:
        #         individuals[ne] = (-1)*individuals[ne]
        #     #插入个体到种群
        #     self.popul.append(individuals)

        self.popul = [
            [5,5,-10,-4,4,4],
            [15,6,-8,-4,2,2],
            [13,5,-9,-3,3,3],
            [15,3,-6,-6,4,2],
            [10,8,-7,-4,3,5]
        ]

    #计算适应度
    def caculate_fitness(self):
        #初始化适应度列表
        self.fit_score = [0] * self.population_size
        #循环赛PK
        for x in range(self.population_size):
            for y in range(self.population_size):
                if x != y:
                    #选择两个个体进行比赛，x为先手，y为后手
                    x_count,o_count = chess_game(self.popul[x],self.popul[y])
                    if x_count > o_count :
                        result1 = 2
                        result2 = 0
                    elif x_count == o_count:
                        result1 = 1
                        result2 = 1
                    else:
                        result1 = 0
                        result2 = 2
                    #将输赢的结果作为分数更新到对应的个体的适应度值
                    self.fit_score[x] += result1
                    self.fit_score[y] += result2

                    #将输赢的结果作为分数更新到对应的个体的适应度值
                    # self.fit_score[x] += x_count - o_count
                    # self.fit_score[y] += o_count - x_count

    #交叉操作
    def crossover_operation(self,individual1,individual2):
        #得到交叉点
        index = random.randint(0,self.individuals_size-1)
        #根据交叉点的位置，将两者后面的列表进行交换
        new_individual1 = individual1[:index] + individual2[index:]
        new_individual2 = individual2[:index] + individual1[index:]

        return new_individual1,new_individual2

    #变异操作
    def mutation_operation(self,individual):
        #遍历整个个体列表
        for i in range(self.individuals_size):
            #对于每一个位置，都有一个概率，如果概率满足一定条件，进行变异
            pro = np.random.random()
            if pro <= MUTATION_RATE:
                #得到一个在0.7-1.3的权重
                weight = random.uniform(0.7,1.3)
                #将值乘以权重得到一个新的变异值
                individual[i] = individual[i] * weight
        #返回新的个体
        return individual

    #计算遗传到下一代的概率
    def genetic_rate(self):
        total_sum = 0
        #计算适应度总和
        length1 = len(self.fit_score)
        for i in range(length1):
            total_sum += self.fit_score[i]
        gene_rate = []
        #计算每一个个体的遗传概率
        for i in range(length1):
            tmp = (float)(self.fit_score[i]) / total_sum
            gene_rate.append(tmp)

        return gene_rate

    #计算遗传到下一代的概率
    # def genetic_rate(self):
    #     total_sum = 0
    #     min_value = min(self.fit_score)
    #     max_value = max(self.fit_score)
    #     fit_normal = []
    #     #计算适应度总和
    #     length1 = len(self.fit_score)
    #     for i in range(length1):
    #         tmp = (float)(self.fit_score[i] - min_value) / (max_value - min_value)
    #         total_sum += tmp
    #         fit_normal.append(tmp)

    #     gene_rate = []
    #     #计算每一个个体的遗传概率
    #     for i in range(length1):
    #         tmp = (float)(fit_normal[i]) / total_sum
    #         gene_rate.append(tmp)

    #     return gene_rate

    #遗传算法训练过程
    def GA_Train(self):
        #进行多次迭代
        for i in range(self.iter_size):
            #计算适应度
            self.caculate_fitness()
            # print("fitness: ",self.fit_score)
            # print(self.popul)
            print("iter ：",i+1)
            #得到最高的适应度值
            max_fit_score = max(self.fit_score)
            #选择适应度分数最高的个体
            max_fit_index = self.fit_score.index(max_fit_score)
            #定义下一代的列表
            new_popul = []
            #把适应度最高的个体加入到下一代
            new_popul.append(self.popul.pop(max_fit_index))
            #将该个体从当前适应度列表删除
            self.fit_score.pop(max_fit_index)
            length1 = len(self.fit_score)
            #计算遗传概率
            gene_rate = self.genetic_rate()
            # print(gene_rate)
            #交叉、变异
            for j in range((int)(length1/2)):
                #根据轮盘转法，根据遗传概率选择两个个体进行交叉
                select_choice = np.random.choice(length1,2,False,gene_rate)
                #进行交叉操作
                individual1,individual2 = self.crossover_operation(self.popul[select_choice[0]],self.popul[select_choice[1]])
                #对个体进行按概率变异操作
                individual1 = self.mutation_operation(individual1)
                individual2 = self.mutation_operation(individual2)
                #将产生的新个体放到下一代
                new_popul.append(individual1)
                new_popul.append(individual2)
            #更新种群
            self.popul = new_popul
        #迭代完成后，选择最优的权重参数
        max_fit_score = max(self.fit_score)
        max_fit_index = self.fit_score.index(max_fit_score)
        print('train weight: ',self.popul[max_fit_index])


if __name__ == "__main__":
    iter_size = 5
    population_size = 5
    individuals_size = 6
    ga = GeneticAlgorithm(population_size,individuals_size,iter_size)
    ga.GA_Train()

