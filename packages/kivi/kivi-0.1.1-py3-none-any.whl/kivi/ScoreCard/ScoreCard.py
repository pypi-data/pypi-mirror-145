# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 10:04
# @Author  : Chensy Cao
# @Email   : chensy.cao@zjtlcb.com
# @FileName: ScoreCard.py
# @Software: PyCharm
import logging
import numpy as np
import pandas as pd
from collections import defaultdict


def get_one_score(value, group, variable_name, cut_point_name='max_bin', woe_point_name='woe_score_int'):

    # 获取此字段的最大最小值
    _max = group.max_bin.max()
    _min = group.min_bin.min()

    # 处理空箱的赋值
    if pd.isna(value):
        score = group[woe_point_name][group.min_bin.isna().tolist()]
        # 找到唯一的空箱，并赋值相应的分数
        if len(score) == 1:
            return int(score)
        # 未找到空箱警告，并对未找到的空值赋分数nan
        elif len(score) == 0:
            logging.warning(f'{variable_name} Not Found Nan Bin! return np.nan!')
            return np.nan
    # 非空箱赋值
    else:
        # 如果真实值，未在分箱给定的最大值与最小值的范围内，则给出报错
        if not (_min <= value <= _max):
            raise Exception(ValueError, f'{variable_name}: {_min} <= {value} <= {_max} Value is out of range!')
        # 获得该值在 group 中的 index
        group.sort_values(by=cut_point_name, inplace=True)
        cut_point = group[cut_point_name].dropna().tolist()
        cut_point.insert(0, -np.inf)
        cut_point[-1] = np.inf
        index = [False] * len(group)
        for i_cut_point in range(len(cut_point) - 1):
            if float(cut_point[i_cut_point]) < value <= float(cut_point[i_cut_point + 1]):
                index[i_cut_point] = True
        # 如果未能找到该值的分箱，则给出报错
        if True not in index:
            raise Exception(ValueError, f'Not fund that bin: {value}')
        # 如果得到唯一的分箱对应值，则返回该值的分箱对应值
        elif sum(index) == 1:
            return int(group[woe_point_name][index])
        # 如果找到多个分箱的对应值，则给出警告，并返回 'multi nums' 多值字符串
        else:
            logging.warning(f'multi nums {variable_name}')
            return 'multi nums'


def get_all_point(
        df_sample: pd.DataFrame, df_woe: pd.DataFrame,
        values_name='values', sample_variable_name='name',
        woe_variable_name='name', woe_point_name='woe_score_int',
        id_name=None, pbar_type=None, des=None,
):
    """
    根据计算的WOE值计算评分卡单项的得分
    :param df_sample: 样本表，每行为一个样本，每列为特征
    :param df_woe: WOE值的表
    :param values_name: df_sample 中的真实样本值的列名称
    :param sample_variable_name: df_sample 中的字段名称列的名字
    :param woe_variable_name: df_woe 中的字段名称列的名字
    :param woe_point_name: df_woe 中的woe值列的名字
    :param id_name: id列的名字
    :param pbar_type: 进度条的展示方式，如果在jupyter notebook中使用则
    :param des: 进度条分割展示的分割虚线标题
    :return: 单项得分表
    """
    res_dict = defaultdict(list)
    if id_name and id_name in df_sample.columns:
        res_dict['id'] = df_sample[id_name].tolist()
    res_dict['variable'] = df_sample[sample_variable_name].tolist()

    values = df_sample[values_name]
    variable_names = df_sample[sample_variable_name]

    # shell & Notebook 进度条
    if pbar_type is not None:
        from tqdm import tqdm_notebook as tqdm
    else:
        from tqdm import tqdm

    # 获取 scheme 下的赋值分数
    print(f"{15 * '='} {des} {15 * '='}")
    with tqdm(total=len(values), desc=f'{des} scoring:') as pbar:
        for value, variable_name in zip(values, variable_names):
            res_dict['point'].append(get_one_score(
                value=value,
                variable_name=variable_name,
                group=df_woe[df_woe[woe_variable_name] == variable_name].copy(),
                woe_point_name=woe_point_name,
            ))
            pbar.update(1)
    return pd.DataFrame(res_dict)

def PDToRant(pd: float, ranking: list, max_grade: int = 16):
    """
    PD 到主标尺等级的映射
    :param pd: 预测PD
    :param ranking: 主标尺分箱的max bin
    :return: 等级
    """
    if pd==1.:
        return max_grade
    else:
        return sum(np.array(ranking) <= pd) + 1

class BinomialTest:

    def __init__(self, df_res=None, ranking=None,
                 target=None, proba=None, alpha=0.05,):
        """
        主标尺下的二项检验，支持两种调用方式
        方式一（推荐）：给定样本的评级等级 ranking、预测PD proba、真实违约 target
        方式二（不推荐）：给定依据评级等级分组后 df_res (DataFrame)
        :param df_res:
        :param ranking:
        :param target:
        :param proba:
        :param alpha:
        """
        import scipy.stats as st
        self.st = st

        self.ranking = ranking
        self.target = target
        self.proba = proba
        self.alpha = alpha

        if self.target is not None:
            groups = pd.DataFrame({
                'ranking': self.ranking,
                'target': self.target,
                'proba': self.proba,
            }).groupby('ranking')

            self.res = pd.DataFrame({
                'ranking': groups.target.sum().index,
                'counts': groups.target.count(),
                'default_nums': groups.target.sum(),
                'default': groups.target.mean(),
                'proba': groups.proba.mean(),
            })
        else:
            self.res = df_res

    def binomial_pvalue(
            self, count_col='counts', proba_col='proba', default_nums_col='default_nums'
    ):
        """
        若给定等级分组后的 df_res 则需指定以下列
            样本计数列 count_col
            分级内的平均预测概率 proba_col
            违约样本数 default_num_col
        :param count_col:
        :param proba_col:
        :param default_nums_col:
        :return:
        """
        group_proba = self.res[proba_col].copy()
        group_proba[group_proba != 1] = group_proba[group_proba != 1] + 1e-6
        group_proba[group_proba == 1] = group_proba[group_proba == 1] - 1e-6

        self.res['Z'] = (self.res[default_nums_col] - self.res[count_col] * group_proba) /\
                   np.sqrt(self.res[count_col] * group_proba * (1 - group_proba))
        self.res['distr'] = self.st.norm.cdf(-np.abs(self.res.Z))
        self.res['p_value'] = self.res.distr * 2
        self.res['binomial_test'] = [True if p > self.alpha else False for p in self.res.p_value]
        return self.res

    def binomial_boundary(
            self, count_col='counts', proba_col='proba', default_nums_col='default_nums',
            unilateral=None,
    ):
        """
        若给定等级分组后的 df_res 则需指定以下列
            样本计数列 count_col
            分级内的平均预测概率 proba_col
            违约样本数 default_num_col
        :param count_col:
        :param proba_col:
        :param default_nums_col:
        :param unilateral: left right
        :return:
        """
        group_proba = self.res[proba_col].copy()
        group_proba[group_proba != 1] = group_proba[group_proba != 1] + 1e-6


        if unilateral == 'left':
            self.res['d_min'] = self.st.binom.ppf(self.alpha, self.res[count_col], group_proba)
            self.res['binomial_test'] = self.res[default_nums_col] >= self.res.d_min
        elif unilateral == 'right':
            self.res['d_max'] = self.st.binom.ppf(1 - self.alpha, self.res[count_col], group_proba)
            self.res['binomial_test'] = self.res[default_nums_col] <= self.res.d_max
        else:
            self.res['d_min'] = self.st.binom.ppf(self.alpha / 2, self.res[count_col], group_proba)
            self.res['d_max'] = self.st.binom.ppf(1 - (self.alpha / 2), self.res[count_col], group_proba)
            self.res['binomial_test'] = np.logical_and(
                self.res[default_nums_col] <= self.res.d_max, self.res[default_nums_col] >= self.res.d_min)

        return self.res

def herfindahl(ranking: pd.Series):
    """
    Herfindahl index 赫芬达尔指数
    计量样本中不同评级的集中度, 一般值域为[1/k, 1]最大为20%。
    :param ranking: 评级等级
    :return: Herfindahl index
    """
    value_counts = ranking.value_counts()
    return sum((value_counts / value_counts.sum())**2)

def PDToScore(PD, base_score=300, pdo=17, log='log2'):
    """
    描述：将预测概率转换为分数，这里区分以e为底取log或以2为底取log。
    以2为底取log，B 即为 pdo
    以e为底取log，B 即为 pdo / ln(2)
    1. ln(odds) = ln(p / 1 - p) = WX^T + b
    2. score = A - B ln(odds)
             = A - B ln(p / 1 - p)
             = A - B (WX^T + b)
    2. score = A - B log2(odds)
             = A - B log2(p / 1 - p)
             = A - B (WX^T + b)
    参数：
    :param PD: 违约概率
    :param base_score: 基准分
    :param pod: Points to Duble the Odds, Odds（好坏比）变为2倍时，所减少的信用分。
    :return: 分数
    """
    if log == 'log2':
        log = np.log2
    else:
        log = np.log
    return base_score + pdo * log((1 - PD) / PD)

def BaseScoreAndPDO(odds=1/50, base_score=600, pdo=20):
    """
    计算 base_score, pdo

    参数：
    :param odds:
    :param base_score:
    :param pdo:
    :return: A, B

    示例：
    >>> BaseScoreAndPDO()
    """
    B = pdo / np.log(2)
    A = base_score + B * np.log(odds)
    return A, B

