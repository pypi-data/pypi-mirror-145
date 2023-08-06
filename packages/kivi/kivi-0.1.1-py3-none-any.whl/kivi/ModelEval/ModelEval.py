from ..Utils import pd, np


def lift(df_score, bins=20, score_name='score', target_name='target'):
    """
    描述：计算模型结果的lift

    :param df_score: DataFrame 评分、PD 结果文件。
    :param bins: 分箱数量。
    :param score_name: 分数字段名称。
    :param target_name: 目标变量名称。
    :return:
    """
    df_score = df_score[[score_name, target_name]].copy()
    bins = np.linspace(df_score[score_name].min(), df_score[score_name].max(), bins + 1)
    df_score["buckets"] = pd.cut(df_score[score_name], bins=bins, include_lowest=True)

    df_buckets = df_score.groupby('buckets').agg({target_name: ['count', 'sum']})
    df_buckets.columns = ['total', 'bad']
    df_buckets['good'] = df_buckets.total - df_buckets.bad

    df_buckets['cum_total'] = df_buckets.total.cumsum() / df_buckets.total.sum()
    df_buckets['cum_bad'] = df_buckets.bad.cumsum() / df_buckets.bad.sum()
    df_buckets['cum_good'] = df_buckets.good.cumsum() / df_buckets.good.sum()
    df_buckets['ks'] = df_buckets.cum_bad - df_buckets.cum_good
    df_buckets['lift'] = df_buckets.cum_bad / df_buckets.cum_total
    return df_buckets


