from ..Utils.utils import unpivot, F, np, pd, Window

def quantile(col: str, percent=0.5):
    """
    描述：分位数计算

    参数：
    :param col: 字段名称
    :param percent: 分位点
    :return : pyspark.sql.functions
    """
    return F.expr(f'percentile_approx({col}, {percent})')

def getQuantiles(df, column_name, ranges=np.linspace(0, 1, 11))->list:
    """
    描述：获取字段的分位数点。

    参数：
    :param df:
    :param column_name:
    :param ranges:
    :return : 分位数值 List

    示例：获取多个字段的多个分位点
    >>> quant_val_list = [getQuantiles(df, col) for col in cols]
    >>> pd.DataFrame(dict(zip(cols, quant_val_list)), index=np.linspace(0, 1, 11)).T
    """
    quantiles = [quantile(column_name, i).alias(f'i') for i in ranges]
    return df.agg(*quantiles).toPandas().values.flatten().tolist()

