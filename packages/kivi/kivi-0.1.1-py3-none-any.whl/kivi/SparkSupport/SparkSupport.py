# -*- coding:utf-8 -*-
# @Time : 2022/3/24 12:36
# @Author: Chensy
# @File : SparkSupport.py
# @Email: chensy.cao@foxmail.com
from ..Utils import F, StringType

def EnableArrow(spark, disp=False):
    """
    描述：开启Arrow加速模式。

    参数：
    :param spark: spark入口
    :param disp: 是否展示Arrow开启状态
    :return None:
    """
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    if disp:
        print(f'Enable Arrow: {spark.conf.get("spark.sql.execution.arrow.enabled")}')


def mapLabel(mapping):
    """
    描述：[UDF] 用来匹配 pyspark DataFrame 中的键值对

    参数：
    :param mapping[Dict]: 需要匹配的字典

    示例：使用行业分类码值表，设置一列中文行业名称。
    >>> df.withColumn('industryCnName', mapLabel(industryDict)(df.industryCode))
    """
    def f(value):
        return mapping.get(value)
    return F.udf(f, returnType=StringType())


def unpivot(df, columns, index_name='uuid', feature_name='name', feature_value='value'):
    """
    描述：对数据表进行反 pivot 操作

    参数：
    :param df:
    :param columns:
    :param index_name:
    :param feature_name:
    :param feature_value:
    :return:
    """
    stack_query = []
    for col in columns:
        stack_query.append(f"'{col}', `{col}`")
    df = df.selectExpr(
        f"`{index_name}`", f"stack({len(stack_query)}, {', '.join(stack_query)}) as (`{feature_name}`, `{feature_value}`)"
    ).orderBy(index_name, feature_name)
    return df