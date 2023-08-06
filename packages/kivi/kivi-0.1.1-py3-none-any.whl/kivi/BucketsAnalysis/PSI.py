from ..Utils.utils import pd, np, saveCsv
from ..Utils.Bins import Bins

class PSI(Bins):

    def __init__(self, csvName=None):
        """
        Des: 计算PSI
        :param margin: cutoff point 左右填充预留边界
        :param csvName: 结果保存的csv文件名称（如果需要保存的话）
        """
        super(PSI, self).__init__()
        self.csvName = csvName

    def miss_data_cnt(self, expected, actual):
        """

        """
        sum_ex = sum(expected.isna())
        sum_ac = sum(actual.isna())

        if sum_ex > 0 or sum_ac > 0:
            na_bin = pd.DataFrame({
                'min_bin': [np.nan],
                'max_bin': [np.nan],
                'Expected': [sum_ex],
                'Actual': [sum_ac],
            })
            return na_bin
        else:
            return None

    @staticmethod
    def _psi(res):
        """
        Des: 计算PSI的核心函数
        :param res: 明细表
        :return: 明细表以及PSI值 res, psi
        """
        if 0 in res.Expected:
            res.Expected += 1
        if 0 in res.Actual:
            res.Actual += 1

        res['Expected_percentage'] = res.Expected / res.Expected.sum()
        res['Actual_percentage'] = res.Actual / res.Actual.sum()
        res['A-E'] = res.Actual_percentage - res.Expected_percentage
        res['A/E'] = res.Actual_percentage / res.Expected_percentage
        res['ln(A/E)'] = np.log(res['A/E'])
        res['index'] = res['A-E'] * res['ln(A/E)']
        psi = res['index'].sum()
        return res, psi

    def Continue(self, expected, actual, bins=10, binType='distance', cutPoint=None):
        """
        Des: 连续型变量的PSI指标
        :param expected: 预期分布
        :param actual: 实际分布
        :param bins: 分箱数目
        :param binType: 分箱类型 'distance'等距 or 'frequency'等频 or 'customize'自定义
        :param csvName: 保存CSV Name, 默认不保存
        :return: 明细表以及PSI值 res, PSI
        """
        expectedMax = expected.max()
        expectedMin = expected.min()
        actualMax = actual.max()
        actualMin = actual.min()

        if not pd.api.types.is_numeric_dtype(expected):
            raise Exception(TypeError, 'expected must be numeric!')

        if not pd.api.types.is_numeric_dtype(actual):
            raise Exception(TypeError, 'actual must be numeric!')

        if (expectedMax == expectedMin) or (actualMax == actualMin):
            raise Exception()

        if (expectedMin > actualMin) or (expectedMax < actualMax):
            raise Exception()

        if cutPoint is not None:
            cutoffPoint = cutPoint
        elif binType == 'distance':
            cutoffPoint = self._cutoffPoint(
                bins=bins, min=expectedMin, max=expectedMax)
        elif binType == 'frequency':
            cutoffPoint = self._cutoffPoint(
                bins=bins, percent=True, expected=expected)
        else:
            raise Exception(TypeError, '分箱错误!')

        df_ex = pd.DataFrame(pd.cut(expected, cutoffPoint).value_counts(sort=False), columns=['Expected'])
        df_ac = pd.DataFrame(pd.cut(actual, cutoffPoint).value_counts(sort=False), columns=['Actual'])
        res = df_ex.join(df_ac, how='outer')
        res['min_bin'] = cutoffPoint[: -1]
        res['max_bin'] = cutoffPoint[1: ]

        na_bin = self.miss_data_cnt(expected, actual)
        if na_bin is not None: res = res.append(na_bin)

        return self._psi(res)


    def Category(self, expected, actual):
        """
        Des: 类别型变量的PSI
        :param expected:
        :param actual:
        :return: 明细表以及PSI值 res, PSI
        """

        if (not pd.api.types.is_string_dtype(expected)) or (not pd.api.types.is_object_dtype(expected)):
            raise Exception(TypeError, 'expected must be string or object!')
        if (not pd.api.types.is_string_dtype(actual)) or (not pd.api.types.is_object_dtype(actual)):
            raise Exception(TypeError, 'actual must be string or object!')

        expected.dropna(inplace=True)
        actual.dropna(inplace=True)

        expectedGroup = expected.value_counts(sort=False)
        actualGroup = actual.value_counts(sort=False)

        res = pd.merge(
            pd.DataFrame({'category': expectedGroup.index, 'Expected': expectedGroup.values}),
            pd.DataFrame({'category': actualGroup.index, 'Actual': actualGroup.values}),
            on='category',
            how='outer',
        )

        self.res, self.psi = self._psi(res)

        if self.csvName:
            saveCsv(res, self.csvName)
            return self.psi
        else:
            return self.res, self.psi


