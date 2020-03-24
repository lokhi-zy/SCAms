# -*- coding: UTF-8 -*-
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

def fit( weight_temp, train_ar,status):
    accuracy = np.zeros(10)
    for i in range (0,10):
        predict_right = 0
        predict_fail = 0
        for j in range(len(train_ar)):
            resuit_sum = 0
            for k in range(0,status):#
                resuit_sum = resuit_sum + (weight_temp[i][k] * train_ar[j][k])  
                te =  weight_temp[i][k] * train_ar[j][k] #
               # print(te,weight_temp[i][k],train_ar[j][k],sep = ',')
                # if math.isnan(te) == False:
                    # print(j,k)
            #print(j,resuit_sum,sep = ",")
            
            if resuit_sum  * (train_ar[j][status] - 1.5) > 0:#
                predict_right = predict_right + 1


            else:
                predict_fail = predict_fail + 1

            #    print(predict_fail,predict_right,sep = ",")   
            # print(predict_fail + predict_right)
        accuracy[i] = predict_right/(predict_right + predict_fail)        
   
    return accuracy


def SCA(generation,filename):

    
    path = "data_train/" + filename
    datafile = path #参数初始化
    data = pd.read_excel(datafile, header = None) #读取数据
    data1 = (data - data.mean())/data.std() #零-均值规范化
    
    train_ar = np.array(data1)
    status = np.shape(train_ar)[1]
    status = status - 1
    mean = data.mean()
    std = data.std()
    mest = np.zeros((2,status))

    for i in range(0,status):
        mest[0][i] = mean[i]

    for i in range(0,status):
        mest[1][i] = std[i]

    file_name = filename.split('.')[0]

    mestpath = basedir + "/standard/" + file_name
    np.savetxt(mestpath,mest)




    weight_origin = 2 * np.random.random((10,status)) - 1
    #print(train_ar)
    fitness = fit(weight_origin , train_ar,status)
    best = 0
    max = 0
    for i in range(len(fitness)):
        if fitness[i] > max:
            max = fitness[i]
            best = i

    # for i in range(0,23):
    #     weight_origin[9] = weight_origin[best] 

    T = generation
    population_best = np.zeros(status + 1)#
    for i in range(0,status):
        population_best[i] = weight_origin[best][i]

    population_best[status] = fitness[best]
    weight_temp = weight_origin

    for FEs in range(T): 
        a1 = 5

        if FEs < 200:
            r1= a1-2 * a1 /(pow(math.e,FEs/T)); # r1 decreases linearly from a to 0
        else:
            r1= a1-FEs*( (a1) / T );

        # r1 = a1 - (FEs*(a1/T))
        # r2 = random.uniform(0,3.1415926)
        # r3 = random.uniform(0, 2)
        # r4 = random.random()  
        for i in range(0,10):
            
            # if i != best:

            for j in range(0,status):#
                
                r2 = random.uniform(0,3.1415926)
                r3 = random.uniform(0, 2)
                r4 = random.random()  
                if r4 >= 0.5:
                    weight_temp[i][j] = weight_temp[i][j] + r1*(math.sin(r2)) * abs((r3*population_best[j])-weight_temp[i][j])
                else:
                    weight_temp[i][j] = weight_temp[i][j] + r1*(math.cos(r2)) * abs((r3*population_best[j])-weight_temp[i][j])

        fitness = fit(weight_temp , train_ar,status)
        max = 0
        
        for l in range(len(fitness)):
           
            if fitness[l] >= max:
                max = fitness[l]
                best = l

        for i in range(0,status):

            if population_best[status] < fitness[best]:

                population_best[i] = weight_temp[best][i]
                population_best[status] = fitness[best]

        # for i in range(0,23):
        #     weight_temp[9] = weight_temp[best] 


        # if fitness[best] > 0.80:
        #     a = 2
        # if fitness[best] > 0.70:
        #     a = 3
        # if fitness[best] > 0.60:
        #     a = 4

        # for m in range(0,23):

        #     weight_temp[9][m] = weight_temp[best][m]

        print( population_best[status] , best )
        # print(population_best)
        #print(fitness[best], best, sep = ",")
    weight_final = np.zeros(status)
    for i in range(0,status):

        weight_final[i] = weight_temp[best][i]
    
    return population_best

def train(generation,filename):
    
    weight_final = SCA(generation,filename)
    return weight_final
    

def Run(testSet):
        traingroup = []
        testLength = len(testSet)
        for x in range(testLength):
                testSet[x] = float(testSet[x])
        testSet[10] = round(testSet[10]*0.1,1)
        
        weight = train()
        result_sum = 0
        for i in range(testLength):
            result_sum =result_sum + (weight[i] * testSet[i])

        if result_sum > 0 :
            result = 1
        else:
            result = 0

        return result


