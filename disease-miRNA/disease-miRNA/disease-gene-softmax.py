#coding=gbk
import pickle
import math
import numpy as np
from math import isnan


#��disList��ȡ����
fDis = open('disList.txt', 'rb')

disList = list()
disList = pickle.load(fDis)

print 'disList:', len(disList)

#�ر��ļ�
fDis.close()


#��disList�е�disease����id�Ź�������
disId = dict()
i = 0
for dis in disList:
    disId[dis] = i
    i = i + 1


#��geneList��ȡ����
fGene = open('geneList.txt', 'rb')

geneList = list()
geneList = pickle.load(fGene)

print 'geneList:', len(geneList)

#�ر��ļ�
fGene.close()


#��geneList�е�gene����id�Ź�������
geneId = dict()
i = 0
for gene in geneList:
    geneId[gene] = i
    i = i + 1


#������õ���disease��gene֮��Ĺ�ϵ��ȡ����
fDisGene = open('disGeneCorre.txt', 'r')

disGeneMat = np.zeros((204,1789))

while True:
    line = fDisGene.readline().strip()
    
    if line == '':
        break
    
    terms = line.split('\t')
    dis = terms[0]
    gene = terms[1]
    corre = float(terms[2])
    
    if isnan(corre):
        corre = 0
    
    disGeneMat[disId[dis]][geneId[gene]] = corre


#�ر��ļ�
fDisGene.close()



#����ÿ��disease term���ܺ�
disSumDict = dict()
for dis in disList:
    disSum = 0
    for gene in geneList:
        disSum += math.exp(disGeneMat[disId[dis]][geneId[gene]])
    disSumDict[dis] = disSum
    
print 'disSumDict:', len(disSumDict)


#����softmax֮��Ľ��������������浽�ļ���
fDisGeneSoftmax = open('disGeneSoftmax.txt', 'w')

for dis in disList:
    for gene in geneList:
        correSoftmax = math.exp(disGeneMat[disId[dis]][geneId[gene]]) / disSumDict[dis]
        
        fDisGeneSoftmax.write(dis + '\t' + gene + '\t' + str(correSoftmax) + '\n')

#�ر��ļ�
fDisGeneSoftmax.close()

