# -*- coding: utf-8 -*-
# @Time    : 2020/2/6 16:53
# @Author  : Chensy Cao
# @Email   : chensy.cao@zjtlcb.com
# @FileName: Bins.py
# @Software: PyCharm

from numpy import linspace, percentile

class Bins:

    def __init__(self, margin=.1):

        self.margin = margin

    def _cutoffPoint(self, bins, percent=False, **kwargs):
        """
        Des: 计算cutoff point，包括等距分箱，等频分箱
        :param bins: 分箱数
        :param percent: 是否使用等频分箱，默认为不使用False
        :param kwargs: 其他参数
        :return: cutoff point
        """

        if percent:
            expected = kwargs['expected']
            points = linspace(0, 100, bins + 1).tolist()
            cutoffPoint = [percentile(expected, point) for point in points]
            return cutoffPoint
        else:
            _min = kwargs['min']
            _max = kwargs['max']
            cutoffPoint = linspace(_min, _max, bins + 1).tolist()
            cutoffPoint.remove(_max)
            cutoffPoint.remove(_min)
            cutoffPoint.insert(0, _min - self.margin)
            cutoffPoint.append(_max + self.margin)
            return cutoffPoint

