import csv
import math
import operator
import random
import numpy as np
import pandas as pd
import os 
from math import exp
import math
basedir = os.path.abspath(os.path.dirname(__file__))


def test(standname,modelname,examplename):

    standpath = basedir + "/standard/" + standname
    modelpath = basedir + "/model/" + modelname

    standard = np.loadtxt(standpath)
    model = np.loadtxt(modelpath)
    path = "data_test/" + examplename
    datafile = path #参数初始化
    data = pd.read_excel(datafile, header = None) #读取数据

    data1 = (data - standard[0])/standard[1]
    test_ar = np.array(data1)

    result_sum = 0

    print(model)
    print(test_ar)
    status = np.shape(test_ar)[1]

    for i in range(status):
        result_sum = result_sum + (model[i] * test_ar[0][i])
    result = np.zeros(2)
    
    result_sum = result_sum - 1.5
    print(result_sum)
    if result_sum > 0:
        result[0] = 2
    else:
        result[0] = 1

    result[1] = model[status]

    return result


