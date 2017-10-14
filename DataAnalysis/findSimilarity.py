# _*_ coding:utf-8 _*_

from load_data import get_gradient_list
import numpy as np

def get_maxcorrcoefresult():
    ratematrix = get_gradient_list()
    sortName = ratematrix.keys()
    sortValue = ratematrix.values()
    sortValue = np.array(sortValue)
    for i in range(13):
        finalsortValue = np.array([i.flatten() for i in sortValue])
    corrcoefresult = [(a, b, np.corrcoef(finalsortValue[a], finalsortValue[b])[0, 1]) for a in range(13) for b in
                      range(a)]
    corrcoefresult.sort(key=lambda s: s[2], reverse=True)

    print(sortName[corrcoefresult[0][0]], sortName[corrcoefresult[0][1]])

get_maxcorrcoefresult()
