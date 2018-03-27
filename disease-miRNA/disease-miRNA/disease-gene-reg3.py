#coding=gbk
import xlrd
import pickle
import networkx as nx
import numpy as np
from sklearn import linear_model


#将Excel中的disease加载进来
data = xlrd.open_workbook('disease.xlsx')
sheet = data.sheets()[0]
tempList = sheet.col_values(1)

disNameList = list()
for dis in tempList:
    temp = str(dis).lower()
    disNameList.append(temp)

print 'disNameList:', len(disNameList)



#将diNameList中的disease和其id号关联起来
disNameId = dict()
i = 0
for dis in disNameList:
    disNameId[dis] = i
    i = i + 1
    
    
#将disease similarity加载进来
data = xlrd.open_workbook('Gaussian_disease.xlsx')

disNameLen = len(disNameList)
disSim = np.zeros((disNameLen,disNameLen))

sheet = data.sheets()[0]

for i in range(383):
    rowData = sheet.row_values(i)
    for j in range(383):
        disSim[i][j] = rowData[j]
        
print disSim[0][0]
print disSim[10][2]
print disSim[382][382]


#将diseaseList加载进来
fDis = open('disList.txt', 'rb')

disList = list()
disList = pickle.load(fDis)

print 'disList', len(disList)

#关闭文件
fDis.close()


#将disease中的disease和其id号关联起来
disId = dict()
i = 0
for dis in disList:
    disId[dis] = i
    i = i + 1



#将gene network加载进来
fGeneNet = open('GeneNetwork.txt', 'rb')

geneNet = nx.Graph()
geneNet = pickle.load(fGeneNet)

geneNetList = list()
for gene in geneNet:
    if gene not in geneNetList:
        geneNetList.append(gene)
        
print 'geneNetList:', len(geneNetList)

#关闭文件
fGeneNet.close()


#将geneList加载进来
fGene = open('geneList.txt', 'rb')

geneList = list()
geneList = pickle.load(fGene)

print 'geneList', len(geneList)

#关闭文件
fGene.close()


#将disease和gene的关系加载进来
fGeneDis = open('curated_gene_disease_associations.tsv', 'r')

disGeneDict = dict()

i = 0
while True:
    line = fGeneDis.readline().strip()
    
    if line == '':
        break
    
    if i > 0:
        terms = line.split('\t')
        gene = terms[1]
        dis = terms[3].lower()
        
        if dis not in disList:
            i = i + 1
            continue
        
        if gene not in geneNetList:
            i = i + 1
            continue
        
        if dis not in disGeneDict:
            disGeneDict[dis] = list()
            disGeneDict[dis].append(gene)
        else:
            if gene not in disGeneDict[dis]:
                disGeneDict[dis].append(gene)
                
    i = i + 1
    
print i
print 'disGeneDict', len(disGeneDict)

#关闭文件
fGeneDis.close()


#将合并后的geneMergeList中的gene加载进来
fGeneMerge = open('geneMergeList.txt', 'rb')

geneMergeList = list()
geneMergeList = pickle.load(fGeneMerge)

print 'geneMergeList', len(geneMergeList)

#关闭文件
fGeneMerge.close()


#将geneMergeList中的gene和其id号关联起来
geneMergeId = dict()
i = 0
for gene in geneMergeList:
    geneMergeId[gene] = i
    i = i + 1



#将gene和disease之间的closeness关系加载进来
fGeneDisClo = open('geneDisClo.txt', 'r')

geneDisCloMat = np.zeros((4277,204))

while True:
    line = fGeneDisClo.readline().strip()
    
    if line == '':
        break
    
    terms = line.split('\t')
    gene = terms[0]
    dis = terms[1]
    clo = float(terms[2])
    
    geneDisCloMat[geneMergeId[gene]][disId[dis]] = clo

#关闭文件
fGeneDisClo.close()



#将重新计算的disease similarity读取进来
fDisSim = open(r'disRegSim.txt', 'r')

disSimMat = np.zeros((204,204))

while True:
    line = fDisSim.readline().strip()
    
    if line == '':
        break
    
    terms = line.split('\t')
    dis1 = terms[0]
    dis2 = terms[1]
    sim = float(terms[2])
    
    disSimMat[disId[dis1]][disId[dis2]] = sim

#关闭文件
fDisSim.close()


#计算disease和gene之间的相关关系
fDisGeneCorre = open('\disGeneCorre.txt', 'w')

i = 0
for dis in disList:
    for gene in geneList:
        
        disSimList = list()
        for dis1 in disList:
            disSimList.append(disSimMat[disId[dis]][disId[dis1]])
            
        geneDisCloList = list()
        for dis2 in disList:
            geneDisCloList.append(geneDisCloMat[geneMergeId[gene]][disId[dis2]])
            
        cov_matrix = np.cov(disSimList, geneDisCloList)
        cov_value = cov_matrix[0][1]
        cov_std = np.sqrt(cov_matrix[0][0] * cov_matrix[1][1])
        cs = cov_value / cov_std
        
        fDisGeneCorre.write(dis + '\t' + gene + '\t' + str(cs) + '\n')
        
        i = i + 1
        print i

#关闭文件
fDisGeneCorre.close()

