import numpy as np 
import scipy.stats as sps
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf
from numpy import linalg as LA 


class PCA():
    # Initialize PCA object
    def __init__(
        self, 
    ):
        self.src_ip_list = []
        self.dst_ip_list = []

        self.intercept = 0
        self.slope = 0
        self.ydist = 0
        
        self.src_ip_dict = {}

    def ipToNum(self, ip):
        ipSplit = str(ip).split('.')
        return int(ipSplit[-1])

    def getYdist(self):
        return self.ydist

    def calYdist(self, srcIpNum, dstIpNum):
        proj = self.slope * srcIpNum + self.intercept
        self.ydist = dstIpNum-proj

    def updatePCA(self, srcIP, dstIP):
        if str(srcIP) in self.src_ip_dict.keys():
            srcIpNum = self.src_ip_dict[str(srcIP)]
        else: 
            self.src_ip_dict[str(srcIP)] = len(self.src_ip_dict)+1
            srcIpNum = self.src_ip_dict[str(srcIP)] 
        dstIpNum = self.ipToNum(dstIP)
        self.src_ip_list.append(srcIpNum)
        self.dst_ip_list.append(dstIpNum)
        d = {'x': self.src_ip_list, 'y': self.dst_ip_list}
        data = pd.DataFrame(data=d)
        lm = smf.ols(formula = 'y ~ x', data=data).fit()
        self.intercept = lm.params.Intercept
        self.slope = lm.params.x

        self.calYdist(srcIpNum, dstIpNum)
