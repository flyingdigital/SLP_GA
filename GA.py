# -*- coding: utf-8 -*-

import random
from Life import Life

class GA(object):
      """遗传算法类"""
      def __init__(self, crossRate, mutationRate, populationCount, geneCount, width, length, aMatchFun):
            self.crossRate = crossRate               # 交叉算子
            self.mutationRate = mutationRate         # 变异算子
            self.lifeCount = populationCount         # 种群数量
            self.geneLength = geneCount              # 基因长度
            self.matchFun = aMatchFun                # 适配函数
            self.lives = []                          # 种群
            self.best = None                         # 保存这一代中最好的个体
            self.generation = 1
            self.crossCount = 0
            self.mutationCount = 0
            self.bounds = 0.0                        # 适配值之和，用于计算概率

            # 定义仓库的长宽
            self.WIDTH = width
            self.LENGTH = length
            # 定义间隔  （简单定义 类似间隔矩阵）
            self.spacing = 1.2
            '''
                  定义每一个个体的长宽 [[长,宽]]  数量与基因长度一致
                  0. 理货区      [15,8]
                  1. 储存区      [5,12]
                  2. 分拣区      [10,12]
                  3. 加工区      [9,10]
                  4. 展示区      [8,9]
                  5. 交易区      [6,10]
                  6. 配载区      [10,8]
                  7. 综合区      [10,6]
            '''
            self.width_length = [
                  [15,8],
                  [5,12],
                  [10,12],
                  [9,10],
                  [8,9],
                  [6,10],
                  [10,8],
                  [10,6]
            ]
            self.initPopulation()


      def initPopulation(self):
            """初始化种群"""
            self.lives = []
            for x in range(self.lifeCount):
                  # 初始化排序
                  temp_dic = {}

                  init_sequence = [x for x in range(self.geneLength)]
                  random.shuffle(init_sequence)  # 随机打乱
                  # print('$'*100)
                  # print(init_sequence)
                  unit_first = [self.spacing + self.width_length[init_sequence[0]][1]/2.0, self.spacing + self.width_length[init_sequence[0]][0]/2.0,
                                self.width_length[init_sequence[0]], init_sequence[0]]
                  temp_dic[0] = [unit_first]
                  line = 0    # 用来确定当前行
                  column = 1  # 用来确定当前放置列
                  for i in range(1,len(init_sequence)):
                        max_line = 0  # 最长的一行
                        for index in range(len(temp_dic)):
                              if len(temp_dic[index]) >= max_line:
                                    max_line = index
                        flag = 0
                        # 一直找一个地方放下这块区域（找一百次找不到那就说明这种排列不行）
                        while(True):
                              if temp_dic.get(line, None) is not None:
                                    # 同一行上一个单位
                                    unit_line_previous = temp_dic[line][column-1]
                                    # 假设放在同一行 则本轮需要放置的区域
                                    unit_x = unit_line_previous[0]+self.spacing+(unit_line_previous[2][1]+ self.width_length[init_sequence[i]][1])/2.0 # 上一个区域的x+间隔+连个区域的长的一半
                                    # 判断这一行是否放得下 放不下 就放下一行
                                    if unit_x+self.spacing+self.width_length[init_sequence[i]][1]/2.0>self.LENGTH:
                                          line = line + 1
                                          column = 0
                                          unit_x = self.spacing + self.width_length[init_sequence[i]][1]/2.0


                                    if line == 0:
                                          unit_y =  self.spacing + self.width_length[init_sequence[i]][0]/2.0
                                    else:
                                          # 同一列 上个单位
                                          unit_column_previous = temp_dic.get(line - 1)
                                          # 找最长的一行做比对
                                          if column >= len(unit_column_previous) and column<= len(temp_dic.get(max_line)):
                                                unit_column_previous = temp_dic.get(max_line)[column]
                                          else:
                                                unit_column_previous = temp_dic.get(line-1)[column]

                                          unit_y = self.spacing + unit_column_previous[1] + (self.width_length[init_sequence[i]][0]+unit_column_previous[2][0])/2.0 # 上一行同一列区域的y+间隔+连个区域的宽的一半

                                    if temp_dic.get(line, None) is None:
                                          temp_dic[line] = [[unit_x,unit_y,self.width_length[init_sequence[i]],init_sequence[i]]]
                                    else:
                                          temp_dic[line].append([unit_x,unit_y,self.width_length[init_sequence[i]],init_sequence[i]])

                                    # print('2'*199)
                                    # print(line)
                                    # print(temp_dic[line])
                                    column=column+1
                                    flag = 1
                              else:
                                    temp_dic[line] =list([])
                              if flag==1:
                                    break

                  gene_list = []
                  for key in temp_dic.keys():
                        for item in temp_dic[key]:
                              gene_list.append(item)

                  self.lives.append(Life(gene_list))

      def judge(self):
            """评估，计算每一个个体的适配值"""
            self.bounds = 0.0
            self.best = self.lives[0]
            for life in self.lives:
                  life.score = self.matchFun(life)
                  self.bounds += life.score
                  if self.best.score < life.score:
                        self.best = life

      def cross(self, parent1, parent2):
            """交叉"""
            index1 = random.randint(0, self.geneLength - 1)
            index2 = random.randint(index1, self.geneLength - 1)
            tempGene = parent2.gene[index1:index2]  # 交叉的基因片段
            temp = []
            for i in parent1.gene[0:index1]:
                  temp.append(i)
            for i in tempGene:
                  temp.append(i)
            for i in parent1.gene[index2:]:
                  temp.append(i)

            new_gene = []
            count = 0
            for i in range(self.geneLength):
                  if count <= index1:
                        new_gene.append(parent1.gene[count])
                  else:
                        new_gene.append([parent2.gene[count][0], parent2.gene[count][1], parent1.gene[count][2],
                                         parent1.gene[count][3]])

            self.crossCount += 1
            return new_gene

      def  mutation(self, gene):
            """突变"""

            index1 = random.randint(0, self.geneLength - 1)
            index2 = random.randint(0, self.geneLength - 1)

            newGene = gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
            newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
            self.mutationCount += 1
            return newGene

      def getOne(self):
            """选择一个个体"""
            r = random.uniform(0, self.bounds)
            for life in self.lives:
                  r -= life.score
                  if r <= 0:
                        return life

            raise Exception("选择错误", self.bounds)


      def newChild(self):
            """产生新后代"""
            parent1 = self.getOne()
            rate = random.random()

            # 按概率交叉
            if rate < self.crossRate:
                  # 交叉
                  parent2 = self.getOne()
                  gene = self.cross(parent1, parent2)

            else:
                  gene = parent1.gene

            # 按概率突变
            rate = random.random()
            if rate < self.mutationRate:
                  gene = self.mutation(gene)

            return Life(gene=gene)


      def next(self):
            """产生下一代"""
            self.judge()
            newLives = []
            newLives.append(self.best)            #把最好的个体加入下一代
            while len(newLives) < self.lifeCount:
                  newLives.append(self.newChild())
            self.lives = newLives
            self.generation += 1
		