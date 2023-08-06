from .WOE import WOE, np, pd
import multiprocessing as mp
from tqdm import tqdm_notebook as tqdm
from itertools import combinations

class SearchWoe(WOE):

    def __init__(self, variables, target, interval, bins, margin=1e-6, unique=20, **kwargs):
        """
        搜索式WoeIV
        :param variables: variables
        :param target: target
        :param interval: 搜索间隔步长
        :param bins: 分箱数
        :param margin: 边缘单位
        """
        super(SearchWoe, self).__init__(variables, target, bins, )
        self.name = variables.name
        self.bins = bins
        self.unique = unique
        self.maxIVCutoffPoint = []
        self.maxIV = 0
        self.maxIVRes = 0
        self.margin = margin

        kwargs.setdefault('cutType', 'qcut')
        kwargs.setdefault('qcutMaxBin', 5)
        self.cutType = kwargs.get('cutType')
        self.qcutMaxBin = kwargs.get('qcutMaxBin')

        self.cutoffPointLs = self.CutoffPoint(
            start=self.variables.min(),
            end=self.variables.max(),
            interval=interval,
            bins=bins,
        )

    def __getCutoffPoint(self, start, end, interCutoffPoint, bins):

        if len(interCutoffPoint) < bins and len(self.variables.unique()) < self.unique:
            if (start not in interCutoffPoint) or ((start - self.margin) not in interCutoffPoint):
                interCutoffPoint.insert(0, start-self.margin)
            if end not in interCutoffPoint:
                interCutoffPoint.append(end)
            return [interCutoffPoint]

        else:
            cutoffPointLs = list(combinations(interCutoffPoint, bins - 1))
            newCutoffPointLs = []

            for cutoffPint in cutoffPointLs:
                _temp = list(cutoffPint)
                _temp.insert(0, start - self.margin)
                _temp.append(end + self.margin)
                newCutoffPointLs.append(_temp)
                assert len(_temp) == bins + 1
            return newCutoffPointLs

    def CutoffPoint(self, start=None, end=None, interval=None, bins=None):

        if self.cutType == 'maxSearch':
            try:
                interCutoffPoint = list(np.arange(start + interval, end, interval))
                if (end - start) < (interval * bins):
                    interCutoffPoint = list(np.arange(start + interval/2, end, interval/2))
            except Exception as e:
                _, cutoffPoint = pd.qcut(self.variables, self.qcutMaxBin, retbins=True, duplicates='drop')
                return [cutoffPoint]
            return self.__getCutoffPoint(start, end, interCutoffPoint, bins)

        elif self.cutType == 'qcut':
            _, interCutoffPoint = pd.qcut(self.variables, self.qcutMaxBin, retbins=True, duplicates='drop')
            interCutoffPoint = list(np.delete(interCutoffPoint, [0, len(interCutoffPoint) - 1]))
            return self.__getCutoffPoint(start, end, interCutoffPoint, bins)

        elif self.cutType == 'cate':
            interCutoffPoint = list(np.sort(self.variables.unique()))
            if len(interCutoffPoint) <= self.bins:
                interCutoffPoint.insert(0, interCutoffPoint[0] - 1e-6)
                return [interCutoffPoint]
            return self.__getCutoffPoint(start, end, interCutoffPoint, bins)

    def BucketRes(self, cutoffPoint):

        bucket = pd.DataFrame({
            'variables': self.variables,
            'target': self.target,
            'Bucket': pd.cut(self.variables, cutoffPoint, include_lowest=True, duplicates='drop')
        })
        bucket.dropna(axis=0, how='all', inplace=True)
        bucket = bucket.groupby('Bucket', as_index=True)

        res = pd.DataFrame({
            'min_bin': bucket.variables.min(),
            'max_bin': bucket.variables.max(),
            'bad': bucket.target.sum(),
            'total': bucket.target.count(),
        })

        _df_temp = pd.DataFrame()
        if len(self.justMiss) != 0:
            _df_temp = pd.DataFrame({
                'min_bin': [np.nan],
                'max_bin': [np.nan],
                "bad": self.justMiss.sum().target,
                'total': self.justMiss.count().target,
            })

        return res, _df_temp

    def CalculateOneTime(self, cutoffPoint):
        """
        描述: 计算一次分箱结果。
        :param cutoffPoint:
        :return: iv
        """
        bucketRes = self.BucketRes(cutoffPoint)
        res, iv = self.calculate_woe(bucketRes)
        return iv

    def res_analysis(self, bucketRes, nan_bucketRes, cutoffPoint, WoeType, freq=False):
        res = self.calculate_woe(bucketRes)
        if len(self.justMiss) != 0:
            _res = self.calculate_woe(nan_bucketRes)
            res = res.append(_res)
        iv_parts = (res['badattr'] - res['goodattr']) * res['woe']
        iv = iv_parts[-np.isinf(iv_parts)].sum()

        if (self.maxIV < iv) and (not freq):
            self.maxIV = iv
            self.maxIVRes = res
            self.maxIVCutoffPoint = cutoffPoint
            self.maxIVRes['name'] = self.name
            self.maxIVRes['WoeType'] = WoeType
        else:
            self.maxIV = iv
            self.maxIVRes = res
            self.maxIVCutoffPoint = cutoffPoint
            self.maxIVRes['name'] = self.name
            self.maxIVRes['WoeType'] = WoeType

        self.maxIVRes['iv_value'] = self.maxIVRes.iv[-np.isinf(self.maxIVRes.iv)].sum()
        self.maxIVRes['missing_rate'] = 1 - (self.variables.count() / self.sampleLength)

    def SearchMaxIV(self, parallel=False):
        """
        描述: 寻找最优分箱。
        :param parallel: 是否使用分布式计算，默认为False，即不使用分布式计算
        :return: maxIV, maxIVRes, maxIVCutoffPoint
        """

        @Timmer
        def Parallel():
            pool = mp.Pool()
            ivLs = pool.map(self.CalculateOneTime, self.cutoffPointLs)
            self.maxIV = max(ivLs)
            maxIVindex = ivLs.index(self.maxIV)
            self.maxIVCutoffPoint = self.cutoffPointLs[maxIVindex]
            bucketRes = self.BucketRes(self.maxIVCutoffPoint)
            self.maxIVRes = self.calculate_woe(bucketRes)
        if parallel:
            Parallel()

        else:
            for cutoffPoint in tqdm(self.cutoffPointLs, desc=f'寻找最大IV分割点'):
                bucketRes, nan_bucketRes = self.BucketRes(cutoffPoint)

                if (0 not in  bucketRes.bad.tolist()) and (((bucketRes.total / bucketRes.total.sum()) <= 0.05).sum()==0):
                    # print('test 1')
                    self.res_analysis(bucketRes, nan_bucketRes, cutoffPoint, 'SearchWoe')

                else:
                    # print('use frequency _1 ')
                    if self.cutType == 'cate' and len(self.cutoffPointLs) == 1:
                        cutoffPoint = self.cutoffPointLs[0]
                        # print(cutoffPoint, self.cutoffPointLs, self.cutType, len(self.cutoffPointLs))
                        bucketRes, nan_bucketRes = self.BucketRes(cutoffPoint)
                        self.res_analysis(bucketRes, nan_bucketRes, cutoffPoint, 'Category', freq=True)

                    else:
                        _, cutoffPoint = pd.qcut(self.variables, self.bins, retbins=True, duplicates='drop')
                        bucketRes, nan_bucketRes = self.BucketRes(cutoffPoint)
                        self.res_analysis(bucketRes, nan_bucketRes, cutoffPoint, 'Frequency_1', freq=True)


        if isinstance(self.maxIVRes, int):
            # print('use frequency _2 ')
            _, cutoffPoint = pd.qcut(self.variables, self.bins, retbins=True, duplicates='drop')
            bucketRes, nan_bucketRes = self.BucketRes(cutoffPoint)
            self.res_analysis(bucketRes, nan_bucketRes, cutoffPoint, 'Frequency_2', freq=True)


        self.maxIVRes = self.maxIVRes[['name', 'min_bin', 'max_bin', 'bad',
                                       'total', 'bad_rate', 'badattr', 'goodattr', 'woe',
                                       'iv', 'iv_value', 'missing_rate', 'WoeType']]

        return self.maxIV, self.maxIVRes, self.maxIVCutoffPoint