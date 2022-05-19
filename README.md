### 一些说明

代码主要使用了遗传算法解决二维仓库布局问题，接着使用matplotlib对仓库的布局进行优化。

种群中的每一个个体设计

- 每一个个体即为一个排序序列(从下至上，从左至右)，序列中的每一个值都如下格式`[x,y,[width,length],num]`，分别为[横坐标，纵坐标，[宽，长]，编号]

变异部分

- 变异部分采用的是交换序列中两个值位置

适应性函数设置

- 其中:Rij表示SLP法得出的作业单位间的理论关系密切度,这里采用Lee提出的关系密切度定量化定义,将作业单位间相互关系密切程度划分为6个等级,分别用A、E、I、O、U、X字母代表,其取值对应为5~0; by表示关联因子,是由作业单位i与j之间的距离d和作业单位间可能的最大距离max(d).所确定的关联程度,其量化采用Lee 的定义。

    ![](C:\Users\zhao_\Desktop\SLP_GA\img\适应性函数.png)

  

| dij/max(d)                       | bij |
| -------------------------------- | --- |
| 0 < dij <= max(d)/6              | 1.0 |
| max(d)/6 < dij <= max(d)/3       | 0.8 |
| max(d)/3 < dij <= max(d)/2       | 0.6 |
| max(d)/2 < dij <= 2*max(d)/3     | 0.4 |
| 2\*max(d)/3 < dij <= 5\*max(d)/6 | 0.2 |
| 5\*max(d)/6 < dij <= max(d)      | 0.0 |

可以配置的参数

- GA.py
  
  - 区域之间的长度 self.spacing
  
  - 区域长宽 self.width_length

- SLP_GA.py
  
  - 宽 WIDTH
  
  - 长 LENGTH
  
  - 惩罚参数 PUNISH
  
  - 迭代次数 GENARATION
  
  - 物流关系图 relation_matrix
  
  - 区域编码 AREA_NAME

### 环境配置

主要是用到的库为matplotlib 

```
pip install matplotlib
```

### 具体效果

![](C:\Users\zhao_\Desktop\SLP_GA\img\布局.png)

![](C:\Users\zhao_\Desktop\SLP_GA\img\分数变化.png)
