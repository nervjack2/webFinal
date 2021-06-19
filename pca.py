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
        self.count = 0

    def ipToNum(self, ip):
        ipSplit = str(ip).split('.')
        return int(ipSplit[-1])

    def getYdist(self):
        return self.ydist

    def calYdist(self, srcIpNum, dstIpNum):
        proj = self.slope * srcIpNum + self.intercept
        self.ydist = dstIpNum-proj

    def updatePCA(self, srcIP, dstIP):
        if srcIP in self.src_ip_dict:
            srcIpNum = self.src_ip_dict[srcIP]
        else:
            srcIpNum = len(self.src_ip_dict) + 1
            self.src_ip_dict[srcIpNum] = srcIpNum
            
        dstIpNum = self.ipToNum(dstIP)

        if len(self.src_ip_list) > 10:
            self.src_ip_list = []
            self.dst_ip_list = []
            self.src_ip_dict = {}
        
        self.src_ip_list.append(srcIpNum)
        self.dst_ip_list.append(dstIpNum)
        d = {'x': self.src_ip_list, 'y': self.dst_ip_list}
        data = pd.DataFrame(data=d)
        lm = smf.ols(formula = 'y ~ x', data=data).fit()
        self.intercept = lm.params.Intercept
        self.slope = lm.params.x

        self.calYdist(srcIpNum, dstIpNum)
        print('ydist:', self.ydist)
        if abs(self.ydist) < 1e-10:
            if self.count > 10:
                print("\n___________________________________________________________________________________________")
                print("\n                                  DDOS DETECTED                                          \n")
                print("\n___________________________________________________________________________________________")
                self.count = 0
                self.src_ip_list = []
                self.dst_ip_list = []
                self.src_ip_dict = {}
                                
            else:
                self.count += 1
        else:
            self.count = 0
