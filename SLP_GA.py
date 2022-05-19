# -*- encoding: utf-8 -*-

import random
import math
from GA import GA


WIDTH = 35
LENGTH = 50
PUNISH = 0.001
GENARATION = 200
# 相互关系图 A:5 E:4 I:3 O:2 U:1
relation_matrix = [
    [0,3,4,3,1,1,1,1],
    [3,0,2,1,1,1,3,1],
    [4,2,0,1,2,2,4,1],
    [3,1,1,0,2,2,4,1],
    [1,1,2,2,0,1,2,1],
    [1,1,2,2,1,0,1,1],
    [1,3,4,4,2,1,0,1],
    [1,1,1,1,1,1,1,0]

    # [0,3,4,2,2,1,0,0],
    # [3,0,2,2,1,1,2,1],
    # [4,2,0,4,1,2,3,0],
    # [2,2,4,0,1,1,0,0],
    # [2,1,1,1,0,2,2,3],
    # [1,1,2,1,2,0,4,2],
    # [0,2,3,0,2,4,0,0],
    # [0,1,0,0,3,2,0,0]


]
AREA_NAME = (
    (0, '理货区'),
    (1, '储存区'),
    (2, '分拣区'),
    (3, '加工区'),
    (4, '展示区'),
    (5, '交易区'),
    (6, '配载区'),
    (7, '综合区')
)
class SLP():
    def __init__(self, aLifeCount=100,):
        self.lifeCount = aLifeCount
        self.ga = GA(crossRate=0.6,
                     mutationRate=0.5,
                     populationCount=100,
                     geneCount=len(relation_matrix),
                     width=WIDTH,
                     length=LENGTH,
                     aMatchFun=self.matchFun)

    def matchFun(self, life):
        # 关系因子 通过计算两个坐标之间的 曼氏距离
        distence = []
        relation_factor = []

        # 计算曼氏距离
        max_dis = 0     # 最大曼氏距离
        for i in range(len(life.gene)):
            temp = []
            for j in range(len(life.gene)):
                # 对单位自己的
                if i==j:
                    temp.append(0)
                else:
                    # 两个单位坐标
                    unit_a = life.gene[i]
                    unit_b = life.gene[j]

                    # 曼氏距离
                    d_a_b = abs(unit_a[0]-unit_b[0]) + abs(unit_a[1]-unit_b[1])

                    if max_dis<d_a_b:
                        max_dis = d_a_b

                    temp.append(d_a_b)
            distence.append(temp)

        # 填充 Lee,根据曼氏距离填充关系因子
        for m in range(len(distence)):
            temp = []
            for n in range(len(distence)):
                if distence[m][n]>0.0 and distence[m][n]<=max_dis/6.0:
                    temp.append(1.0)
                elif distence[m][n]>max_dis/6.0 and distence[m][n]<=max_dis/3.0:
                    temp.append(0.8)
                elif distence[m][n]>max_dis/3.0 and distence[m][n]<=max_dis/2.0:
                    temp.append(0.6)
                elif distence[m][n]>max_dis/2.0 and distence[m][n]<=2.0*max_dis/3.0:
                    temp.append(0.4)
                elif distence[m][n]>2.0*max_dis/3.0 and distence[m][n]<=5.0*max_dis/6.0:
                    temp.append(0.2)
                elif distence[m][n]>5.0*max_dis/6.0 and distence[m][n]<=max_dis:
                    temp.append(0.2)
                else:
                    temp.append(0.0)
            relation_factor.append(temp)
        # print(relation_factor)
        # 关系因子 * 对应关系矩阵
        sum = 0.0
        # print(len(life.gene))
        punish_matrix = [[1.0 for i in range(8)] for j in range(8)]
        for i in range(len(relation_matrix)):
            for j in range(len(relation_matrix)):
                # 获取两个gene  坐标 长宽
                gene_a = life.gene[i]
                gene_a_x = gene_a[0]
                gene_a_y = gene_a[1]
                gene_a_width = gene_a[2][0]
                gene_a_length = gene_a[2][1]

                gene_b = life.gene[j]
                gene_b_x = gene_b[0]
                gene_b_y = gene_b[1]
                gene_b_width = gene_b[2][0]
                gene_b_length = gene_b[2][1]

                '''
                惩罚: 简单处理 乘上惩罚因子 
                1. 两个gene出界  
                2. 两个gene重合  
                '''

                # 出界
                if gene_a_x-gene_a_length/2.0 < 0 or gene_a_x+gene_a_length/2.0>LENGTH \
                    or gene_a_y-gene_a_width/2.0<0 or gene_a_y+gene_a_width/2.0>WIDTH:
                    punish_matrix[i][j] = punish_matrix[i][j]*PUNISH

                if gene_b_x-gene_b_length/2.0 < 0 or gene_b_x+gene_b_length/2.0>LENGTH \
                    or gene_b_y-gene_b_width/2.0<0 or gene_b_y+gene_b_width/2.0>WIDTH:
                    punish_matrix[j][i] = punish_matrix[i][j] * PUNISH

                # 重合
                if abs(gene_a_x-gene_b_x)<(gene_a_length+gene_b_length)/2.0 \
                    and abs(gene_a_y-gene_b_y)<(gene_a_width+gene_b_width)/2.0:
                    punish_matrix[i][j] = punish_matrix[i][j] * PUNISH
                    punish_matrix[j][i] = punish_matrix[i][j] * PUNISH

                # sum = punish*(sum + relation_factor[i][j]*relation_matrix[i][j]

        for m in range(len(relation_factor)):
            for n in range(len(relation_factor)):
                sum = sum + relation_factor[m][n]*relation_matrix[m][n]*punish_matrix[m][n]



        return sum
    def run(self, n=0):
        best_list = []
        while n > 0:
            self.ga.next()
            distance = self.matchFun(self.ga.best)
            print(("%d : %f "+str(self.ga.best.gene)) % (self.ga.generation, distance))
            best_list.append(self.ga.best.score)
            n -= 1

        return self.ga.best.gene, best_list

# 画仓库布局图
def plot_best_layout(gene):
    from matplotlib import pyplot as plt
    from matplotlib import patches as pc

    # 支持中文
    plt.rcParams['font.sans-serif'] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False
    figure = plt.figure()
    ax = figure.add_subplot(111, aspect='equal')
    plt.xlim(0, LENGTH)
    plt.ylim(0, WIDTH)
    # 开始画图
    for g in gene:
        ax.add_patch(
            pc.Rectangle(
                (float(g[0]) - g[2][1] / 2.0, float(g[1]) - g[2][0] / 2.0),
                g[2][1],
                g[2][0],
                fill=False
            )
        )
        # 标字
        plt.text(float(g[0])-g[2][1]/4.0, float(g[1]),AREA_NAME[g[3]][1])
        # 标长宽
        plt.text(float(g[0]), float(g[1]) - g[2][0] / 2.0,g[2][1],fontdict={'color':'blue'}) # 长
        plt.text(float(g[0]) - g[2][1] / 2.0, float(g[1]),g[2][0],fontdict={'color':'blue'}) # 宽
        # print(AREA_NAME[g[3]])
        # print(AREA_NAME[g[3]][1])
    plt.axvline(LENGTH)
    plt.axhline(WIDTH)

    plt.show()

# 分数变化
def plot_best_score_change(best_list):
    import matplotlib.pyplot as plt
    import numpy as np

    # 分别存放所有点的横坐标和纵坐标，一一对应
    x_list = [i for i in range(len(best_list))]
    y_list = [score for score in best_list]

    # 创建图并命名
    plt.figure('Line fig')
    ax = plt.gca()
    # 设置x轴、y轴名称
    ax.set_xlabel('Number of Iteration')
    ax.set_ylabel('Score')

    # 画连线图，以x_list中的值为横坐标，以y_list中的值为纵坐标
    # 参数c指定连线的颜色，linewidth指定连线宽度，alpha指定连线的透明度
    ax.plot(x_list, y_list, color='b', alpha=0.4)

    plt.show()

def main():
    flag = 1

    tsp = SLP()
    gene, best_list = tsp.run(GENARATION)
    plot_best_layout(gene)  # 画仓库布局图
    # plot_best_score_change(best_list) # 分数变化

if __name__ == '__main__':
    main()


