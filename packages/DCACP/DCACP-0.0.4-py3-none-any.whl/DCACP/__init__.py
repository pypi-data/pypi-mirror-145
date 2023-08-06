import dataPreprocessing
import math
import random
import scipy.stats as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import seaborn as sns
import pandas as pd
from matplotlib import colors

def scatterPlot(data):
    """
    Data visualization ( scatter plot )
    :param data: data set
    :return: No return
    """
    x = data[:, 0]
    y = data[:, 1]
    n = np.arange(data.shape[0])

    fig, ax = plt.subplots()
    ax.scatter(x, y)

    for i, txt in enumerate(n):
        ax.annotate(txt + 1, (x[i], y[i]))
    plt.savefig('img\meta_data.svg', dpi=600)
    plt.show()


def scatterPlotPhe(data, pheList):
    """
    Data visualization ( pheromone map )
    :param data: Data set
    :return: No return
    """

    x = data[:, 0]
    y = data[:, 1]
    fig, ax = plt.subplots()

    for i in range(0, len(pheList)):
        now_pheList = normalize(pheList, pheList[i])
        plt.scatter(x[i], y[i], marker=".", s=now_pheList * 1000, c='orange')
        ax.annotate(i + 1, (x[i], y[i]))
    plt.savefig('img\phefig.svg', dpi=600)
    plt.show()

def scatterPlotLine(data, num,history_run_list):
    """
    Data visualization ( path map )
    :param data: data set
    :return: 无返回
    """

    x = data[:, 0]
    y = data[:, 1]
    fig, ax = plt.subplots()
    x_list=[]
    y_list=[]
    for j in range(0,len(history_run_list)):
        now_point=history_run_list[j]-1
        now_x=x[now_point]
        now_y=y[now_point]
        x_list.append(now_x)
        y_list.append(now_y)
    ax.plot(x_list, y_list, color='black', label='.', marker='.',markersize=10,linewidth=1,alpha=0.3,markerfacecolor='red')
    figname='img\line_'+str(num)+'.svg'
    plt.savefig(figname, dpi=600)
    plt.show()


def distanceMatrix(matrix):
    """
    distanceMatrix
    :param matrix: Matrix composed of original coordinate data
    :return: dis_matrix: distance matrix
    """
    matrix = np.array(matrix, dtype=np.float64)  # Transform the incoming matrix into a numpy type matrix ( ndarray )
    dis_matrix = distance.cdist(matrix, matrix,
                                'euclidean')  # Call the distance function, find the distance of matrix AB, A = matrix, B = matrix, Euclidean distance
    return dis_matrix  # Returns a distance matrix


def neighborPointList(p1, disMatrix):
    """
    Gets the column of p1 in the nearest neighbor matrix and arranges the nearest neighbor of p1 in turn
    :param p1:To find the nearest neighbor point
    :param disMatrix: distance matrix
    :return: The neighbor of p1 arranged in order
    """
    keys = []  # Create list
    for i in range(1, disMatrix.shape[1] + 1):  # Create key value
        keys.append(i)
    a = dict(zip(keys, disMatrix[p1 - 1]))  # compression dictionary
    a = sorted(a.items(), key=lambda x: x[1])  # Updated to list
    neighborArr = []  # The column of p1 nearest neighbor matrix

    for i in range(1, len(a)):
        neighborArr.append(a[i][0])  # Add the returned value to the nearest neighbor column
    return neighborArr


def neighborListALL(disMatrix):
    """
    Get a complete nearest neighbor matrix
    :param disMatrix: Distance Matrix
    :return:neighborMatrix
    """
    res = []
    for i in range(0, disMatrix.shape[1]):  # 把近邻列加入到近邻矩阵内
        sorted_id = sorted(range(len(disMatrix[i])), key=lambda k: disMatrix[i][k], reverse=False)
        temp = sorted_id
        sorted_id = sorted(range(len(temp)), key=lambda k: temp[k], reverse=False)
        res.append(sorted_id)
    return np.array(res)


def pheromonesList(data):
    pointNum = data.shape[0]  # Number of points sought
    pheList = []  # Create a list of pheromones
    for i in range(0, pointNum):
        pheList.append(1)  # Add values to the pheromone list
    return pheList


def randomData(mu, sigma, row, col):
    """
    Production of Gaussian distribution data
    :param mu: mean
    :param sigma: standard deviation
    :param row: number of rows
    :param col: number of columns
    :return: Gaussian distribution data set
    """
    data1=np.random.normal(mu, sigma, [row, col])
    data2=np.random.normal(mu/2, sigma/2, [row, col])
    data3=np.append(data1,data2,axis=0)
    return data3


def normalize(list, value):
    range = max(list) - min(list)
    if range == 0:
        return 1
    else:
        value2 = (value - min(list)) / range
        return value2


def getReciprocal(matrix):
    """
    Get the reciprocal of matrices
    :param matrix:incoming matrix
    :return: reciprocal of matrix
    """

    return np.divide(1, matrix, out=np.zeros_like(matrix, np.float64), where=matrix != 0)


def getNND(neighborMatrix):
    """
    Get NND of Matrix
    :param matrix: The incoming matrix
    :return: Returns the NND list
    """
    NND = []  # NND List
    # i j represents the serial number of points, so start with 1
    for i in range(0, neighborMatrix.shape[0]):
        NND.append(np.mean(np.divide(neighborMatrix[i], neighborMatrix.T[i], out=np.zeros_like(neighborMatrix[i], np.float64), where=neighborMatrix.T[i] != 0)))
    return NND

def getTypeList(data):
    """
    Gets TypeList to represent the type of data
    :param data: data matrix
    :return: TypeList
    """
    TypeList = []
    for i in range(0, data.shape[0]):
        TypeList.append(-1)
    return TypeList


def resPlot(data, typeList):
    """
    Make clustering diagrams ( for 2D data only )
    :param data: Data
    :param typeList: typeList
    :return:
    """
    df1 = pd.DataFrame({'x': data[:, 0], 'y': data[:, 1]})  # Get X, Y corresponding data
    df2 = pd.DataFrame(typeList)  # Get type
    df1.insert(df1.shape[1], 'type', df2)
    sns.lmplot(x='x', y='y', hue='type',
               data=df1, fit_reg=False)

    return plt

def resPlot3D(data, typeList,fig_x,fig_y):
    """
    Make clustering maps ( for 3D data only )
    :param data: data
    :param typeList: typeList
    :return:
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    mycolors=list(colors.CSS4_COLORS.keys())
    for i in range(0,len(typeList)):
        ax.scatter(data[i, 0], data[i, 1], data[i, 2], c=mycolors[(typeList[i]+5)])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.view_init(fig_x, fig_y)
    return plt



def antRun(pheList, p, dis_Recip, NND, eta, niu, dataAnal, k, maxType, typeList, now_round, round_ant_num,
           now_ant_num, ant_order_max, alpha, beta, neighborMatrix, history_run_list):
    """
    Crawling and clustering after death
    :param pheList: List of pheromones
    :param p: starting point
    :param dis_Recip: Inverted distance matrix
    :param NND: NND Matrix
    :param eta: Ant life ( a sign of survival )
    :param niu: Factors determining type 2 mortality. Triggered less, used to shorten clustering time and correct clustering results
    :param dataAnal: Record how many times each point was crawled
    :param k: k-nearest neighbor
    :param maxType: Maximum number of clusters
    :param typeList: Clustering matrix. Represents the type of each point
    :param now_round: Number of rounds now
    :param round_ant_num: Number of ants per round
    :param now_ant_num: Now ant num of this round
    :param ant_order_max: Total number of ants
    :param alpha: Upper Limit for Controlling Ant Type 1 Death
    :param beta: Lower Limits for Controlling Ant Type 1 Death
    :param neighborMatrix: nearest neighbor matrix
    :param history_run_list: Record the Historical Path of Ant Crawling ( Drawing )
    :return: Maximum number of clusters updated
    """
    delta_List = []  # delta used to record climbing points
    nabla_List = []  # nabla used to record crawl points
    run_List = []  # Record the number of points ants crawl through
    run_List.append(p)  # Add the starting point to run_List
    history_run_list.append(p)

    ant_order = now_round * round_ant_num + now_ant_num  # The current ant in the overall ant number. Round and num start counting from 0, so finally + 1
    N_mu = ant_order_max / 2  # Take the middle ant to reach the maximum curve
    N_sigma = ant_order_max / 6  # (u-3*sig,u+3*sig)  6*sig=ant_order_max
    multiple_for_max_neibor = alpha * (
        math.sqrt(2 * math.pi)) * N_sigma  # Used to raise a normal distribution to a required value ( multiple )
    mu = multiple_for_max_neibor * st.norm.pdf(ant_order, N_mu, N_sigma) + beta
    # This is the ant ' s mu, mu affects the ant ' s crawling range, if the nabla + delta value is greater than mu, then terminate the ant ' s crawling.
    # Here replace the current ant number, normal distribution of mu,
    # sigma get the corresponding normal distribution position, and then add beta to improve the basic value.
    while eta >= 0:
        nextpoint, probability = AntChoice(pheList, p, dis_Recip, NND, k, dataAnal, neighborMatrix)  # Finding the next point and its probability
        run_List.append(nextpoint)  # Add the point to climb to run_List
        history_run_list.append(p)

        # Stop finding condition 1
        new_delta = neighborMatrix[p][nextpoint]  # Get the delta of this step
        new_nabla = neighborMatrix[nextpoint][p]  # Get the nabla for this step
        delta_List.append(new_delta)  # Add a new delta to delta_List
        nabla_List.append(new_nabla)  # Add a new nabla to nabla_List
        temp_sum2 = new_nabla + new_delta  # A new definition, added later

        if temp_sum2 > mu:  # If the value of nabla + delta is greater than mu, stop the ant crawling
            eta = -1  # Let ants die
            run_List.pop()  # Let ants die
            history_run_list.pop()
            break  # Delete the point to add crawling

        # Stop searching condition 2
        max_num = max(run_List, key=run_List.count)  # Statistics of the most frequent points
        max_time = run_List.count(max_num)  # Count the number of occurrences of this point
        if max_time > niu:  # If you want a point to crawl more than niu, stop the ant crawling
            eta = -1  # Let ants die
            run_List.pop()  # Delete the point to add crawling
            history_run_list.pop()
            break  # Exit cycle
        # Normal situation

        pheList[p] = pheUpdate(pheList[p], probability)
        pheList[nextpoint] = pheUpdate(pheList[nextpoint], probability)  # Update endpoint pheromone
        p = nextpoint  # Update the next point
        dataAnal[nextpoint] += 1  # Update the number of crawls at the next point
        eta = etaUpdate(eta)  # Update eta

    # ---------------Ants begin clustering after death-------------
    if ((eta == -1) & (len(run_List) != 0)):  # If the ants die and the crawling list is not empty.
        dead_run_list = list(set(run_List))  # Get the run_List that 's gone, and see where the ant climbs all his life
        dead_run_list_num = len(dead_run_list)  # Gets the size of dead_run_list for subsequent loop traversal
        color_list = []  # Cluster list
        for m in range(0, dead_run_list_num):  # Start traversing every point you crawl through
            now_point = dead_run_list[m]  # Get which point the current climb is.
            color_list.append(typeList[now_point])  # Add the class corresponding to this point to the cluster list
        color_list2 = pd.value_counts(color_list)  # Sort the cluster list to see which category appears most frequently
        mark = color_list2.index[0]  # Get the most frequent cluster
        if (mark == -1):  # If the largest cluster is-1, -1 denotes the undefined cluster. Then make the crawl point a new cluster
            maxType = maxType + 1  # If the largest cluster is-1, -1 denotes the undefined cluster. Then make the crawl point a new cluster
            for n in range(0, dead_run_list_num):  # Go through every point you crawl through
                now_point = dead_run_list[n]  # Get this point number
                typeList[now_point] = maxType  # Set this point to a new cluster
        else:  # If the most frequent clusters are not - 1 clusters, then all points are summed up as the most frequent clusters
            for n in range(0, dead_run_list_num):  # To traverse every point
                now_point = dead_run_list[n]  # Get the current point serial number
                typeList[now_point] = mark  # Set the most frequent cluster to the cluster at the current point
    return maxType


def AntChoice(pheList, p, dis_Recip, NND, k, dataAnal, neighborMatrix):
    """
    :param pheList: List of pheromones
    :param p: starting point
    :param dis_Recip: reciprocal of distance matrix
    :param NND: NND matrix
    :param dis: distance matrix
    :param k: k nearest neighbor
    :param run_List: list of points that have been crawled
    :return: the next point selected
    """
    PC_List = []  # Path reliability matrix
    PC_sum = 0  # Sum of path reliability
    Probability = []  # Probability list
    neighborMatrix_index = sorted(range(len(neighborMatrix[p])), key=lambda k: neighborMatrix[p][k])
    for i in range(1, k + 1):
        phe = pheList[i]  # Finding the pheromone of the end point
        factor1 = getPC(phe, p, neighborMatrix_index[i], dis_Recip, NND, neighborMatrix)  # The path reliability from point p to point i is
        # Another influencing factor (factor 2) was added here to act on PC_temp
        # The purpose is to solve the problem of ants running back and forth at two points.
        # Factor 2 is similar to sigmoid function, but take x as negative
        appear_num = dataAnal[i]  # Count the number of crawls at this point
        if (appear_num > 5):
            appear_num = 5
        factor2 = 1 / (1 + math.e ** appear_num)  # Calculation factor2
        PC_temp = factor1 * factor2  # Definition of PC_temp
        PC_List.append(PC_temp)  # Add path reliability to the list
        PC_sum = PC_sum + PC_temp  # Cumulative summation
    for i in range(0, len(PC_List)):  # The probability of each point is calculated
        if PC_sum != 0:
            Probability.append(PC_List[i] / PC_sum)
        else:
            Probability.append(PC_List[i])
    chosen_point_index = roulette(Probability)  # The end point is obtained
    chosen_point = neighborMatrix_index[chosen_point_index]
    probability = Probability[chosen_point_index]  # The probability from the starting point to the end point
    return chosen_point, probability


def getPC(phe, p, pap, dis_Recip, NND, neighborMatrix):
    """
    :param phe: pheromone of the endpoint
    :param p: starting point
    :param pap: endpoint
    :param dis_Recip: reciprocal of distance matrix
    :param NND: NND matrix
    :param neighborMatrix: neighbor matrix
    :return:
    """
    nabla = neighborMatrix[pap][p]  # Get the nabla
    delta = neighborMatrix[p][pap]  # Get the delta
    dis_p_pap = dis_Recip[p][pap]  # Find the reciprocal of p p ' distance
    pc = phe * (nabla + 1) / (delta + 1) * dis_p_pap * NND[pap]  # Seeking Path Reliability
    return pc  # Return path reliability


def roulette(fitness):
    """
    Implementation method of stochastic acceptance for roulette strategy
    :param fitness:Imported probabilistic data that can be arranged in a small to large order ( list or tuple )
    :return: selected point
    """
    N = len(fitness)  # Length of probability data
    maxFit = max(fitness)
    if maxFit == 0:
        return -1
    while True:
        # randomly select an individual with uniform probability
        ind = int(N * random.random())
        # with probability wi/wmax to accept the selection
        if random.random() <= fitness[ind] / maxFit:
            return ind


def pheUpdate(oldphe, probability):
    newphe = oldphe + probability  # Update pheromone
    return newphe  # Return the updated pheromone


def etaUpdate(oldeta):
    neweta = oldeta
    return neweta


def antModel(data, round, niu, k, alpha, beta,ant_num,n_cluster,type):
    """
    :param data: data set
    :param round: The num of implemented rounds, every round has an ant crawling
    :param niu: The maximum number of repeated crawling at the same point
    :param k: Traversal neighbor range, k = 10, count only 10 nearest neighbors
    :param alpha: Factors controlling ant death. Is also the maximum value of normal distribution curve
    :param beta: Represents the base value to be added to the normal distribution curve.
                Because the first and last values of the normal distribution are the smallest, the ant will die meaninglessly
    :param ant_num: Number of ants
    :param n_cluster: Expected clusters ( valid only when type = = 2 )
    :param type: Type of Ant Clustering
    :return:
    """

    dis = distanceMatrix(data)  # distance matrix
    dis = (dis - np.min(dis)) / (np.max(dis) - np.min(dis))  # Normalization of distance matrix
    dis_Recip = getReciprocal(dis)  # Finding the reciprocal of distance matrix
    dis_Recip = (dis_Recip - np.min(dis_Recip)) / (np.max(dis_Recip) - np.min(dis_Recip))  # Normalization of reciprocal of distance matrix
    neighborMatrix = neighborListALL(dis) # Finding nearest neighbor matrix
    pheList = pheromonesList(data)  # Find the list of pheromones
    n_s=ant_num
    NND = getNND(neighborMatrix)  # Obtaining NND Matrix
    dataAnal = [0] * data.shape[0]  # Number of records selected
    typeList = getTypeList(data)  # List of final point type
    maxType = 0
    ant_order_max = round * n_s
    history_run_list = []
    birth_list=[]

    for i in range(0, round):  # Traversing each round
        for j in range(0, n_s):  # Traversing every ant
            eta=1
            p = pheList.index(min(pheList)) # Ant Birth Point
            birth_list.append(p)
            maxType = antRun(pheList, p, dis_Recip, NND, eta,niu, dataAnal, k, maxType, typeList, i, n_s,
                                    j, ant_order_max, alpha, beta, neighborMatrix,history_run_list)  # Let the ants run

    # type==1 direct return

    if type==2:
        allPoint=len(typeList)
        group_point_num=int(allPoint/n_cluster)
        typeList_count=pd.value_counts(typeList)
        hub_group_type=list(typeList_count.index[0:(n_cluster)])
        for i in range(0,allPoint):
            if typeList[i] in hub_group_type:
                continue
            else:
                neighborMatrix_index = sorted(range(len(neighborMatrix[i])), key=lambda k: neighborMatrix[i][k])
                nowpoint_type_list=[]
                for j in range(0,group_point_num):
                    neighbor_num=neighborMatrix_index[j]
                    nowpoint_type_list.append(typeList[neighbor_num])
                typeList[i]=pd.value_counts(typeList).index[0]

    elif type==3:
        # --------example------------
        # old_pheList [1 2 5 3 2 1]
        # old_typeList [1 1 2 2 3 4]
        # old_index 0,1,2,3,4,5
        # new_pheList [1 1 2 2 3 5]
        # new_typeList [1, 4, 1, 3, 2, 2]
        # new_index [0 5 1 4 3 2]
        # --X---------------X--
        hub_index_old=[]
        typeSet=set(typeList)# {1,2,3,4}
        typeSet_listType=list(typeSet)# [1,2,3,4]
        len_typeSet=len(typeSet)
        len_typeList=len(typeList)
        new_typeList=[]
        new_index = np.argsort(pheList) # new_index [0 5 1 4 3 2]
        for i in range(0,len_typeList):
            now_index=new_index[i]# old_typeList [1 1 2 2 3 4]
            new_typeList.append(typeList[now_index])# new_typeList [1, 4, 1, 3, 2, 2]
        for i in range(0,len_typeSet):
            nowType=typeSet_listType[i]                         ##  typeSet:{1,2,3,4} typeSet[3]=4
            type_first_time_index=new_typeList.index(nowType) ## new_typeList.index(4)=1
            old_position=new_index[type_first_time_index]## new_index=[0 5 1 4 3 2]  new_index[1]=5
            hub_index_old.append(old_position) ### hub_index_old=[5] old_pheList[5]=1 old_typeList[5]=4
        for i in range(0,len_typeList):
            nearest_neighbor=hub_index_old[0]
            min_neighbor_num=len_typeSet
            for choice in range(0,len(hub_index_old)):
                if neighborMatrix[i][hub_index_old[choice]]<min_neighbor_num:
                    min_neighbor_num=neighborMatrix[i][nearest_neighbor]
                    nearest_neighbor=hub_index_old[choice]
            typeList[i]=typeList[nearest_neighbor]

    return pheList, dataAnal, typeList

