
import pandas as pd

class AIP(object):
    """
    此方法用来解决 定投收益分析 问题
    目前可导出的分析结果
    1. AIP.fenwei()滚动分析的0-1分位收益率
    2. AIP.zhenghuibao()正回报概率
    3. 

    使用方法：实例化后，依次调用需要使用的分析函数即可
    """
    def __init__(self, data, gap) -> None:
        #data：要求columns等于 分析的项目（私募/行业名称） index为时间 目前导入数据需要为处理好的周和年
        #gap：滚动分析的时间跨度，即一次定投持续的时间单位，同index的时间单位一致
        self.data = data
        self.gap = gap
        self.interest = pd.DataFrame().reindex_like(self.data.iloc[self.gap:, :])#得到的定投收益率表
        self.answer = pd.DataFrame(index=self.data.columns)#分析结果表

        #定投收益表，以gap为时间单位的滚动收益率
        for i in range(self.data.shape[0] - self.gap):
            self.interest.iloc[i, :] = ((1. / self.data.iloc[i:self.gap+i, :]).sum(axis=0) * self.data.iloc[self.gap+i, :]-self.gap)/self.gap - 0.015
        
    def fenwei(self):
        #最低，最高，四分位，二分位，四分之三分位
        self.answer[['最低', '25%', '50%', '75%', '最高']] = self.interest.quantile([0,0.25,0.5,0.75,1],axis=0).T.iloc[:,:]
    
    def zhenghuibao(self):
        #计算正回报概率
        self.answer['正回报概率']=((self.interest>0).sum(0)/self.interest.count(0)).T

data=pd.read_excel("dt.xlsx",sheet_name=0,index_col=0)

problem=AIP(data,12)
problem.fenwei()
problem.zhenghuibao()
problem.answer.to_excel('excel1.xlsx', sheet_name='Sheet1')


