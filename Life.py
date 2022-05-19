# -*- encoding: utf-8 -*-


SCORE_NONE = -1

class Life(object):
      """个体类"""
      def __init__(self, gene = None):
            '''
                  每一gene 就是一个区域排列  num表示区域编码

                  [x,y,[width,length],num]
            '''
            self.gene = gene
            self.score = SCORE_NONE


