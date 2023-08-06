import matplotlib.pyplot as plt
import numpy as np  # 调用 numpy 包作为 np 使用
from scipy.spatial import distance  # 调用distance函数求距离矩阵
import math
import random


def roulette(fitness):
    """
    轮盘赌策略 随机接受（Stochastic Acceptance）的实现方法
    参考:https://github.com/mangwang/PythonForFun/blob/master/rouletteWheelSelection.py
    :param fitness:传入的概率数据，可以不按从小到大的顺序排列 (list or tuple)
    :return: 选择的点
    """
    N = len(fitness)  # 概率数据的长度
    maxFit = max(fitness)
    if maxFit==0:
        return -1
    while True:
        # randomly select an individual with uniform probability
        ind = int(N * random.random())
        # with probability wi/wmax to accept the selection
        if random.random() <= fitness[ind] / maxFit:
            return ind

def loadData(filename):
    """
    加载数据
    :param filename: 文件名
    :return: 数据集 numpy集合的形式
    """
    data = np.loadtxt(filename)  # 加载数据
    return data


def scatterPlot(data):
    """
    数据可视化（散点图）
    :param data: 数据集
    :return: 无返回
    """
    x = data[:, 0]
    y = data[:, 1]
    n = np.arange(data.shape[0])

    fig, ax = plt.subplots()
    ax.scatter(x, y)

    for i, txt in enumerate(n):
        ax.annotate(txt + 1, (x[i], y[i]))
    plt.show()


def distanceMatrix(matrix):
    """
    距离矩阵
    :param matrix: 原始坐标数据构成的矩阵
    :return: dis_matrix: 距离矩阵
    """
    matrix = np.array(matrix, dtype=np.float64)  # 把传入的matrix转化为numpy类型的矩阵( ndarray )
    dis_matrix = distance.cdist(matrix, matrix,
                                'euclidean')  # 调用distance函数，求矩阵AB的距离，A=matrix，B=matrix，‘Euclidean’表示欧式距离
    return dis_matrix  # 返回一个距离矩阵


def neighborPointList(p1, disMatrix):
    """
    得到近邻矩阵里的p1的那一列，依次排列出p1的近邻
    :param p1:要找近邻的点
    :param disMatrix:距离矩阵
    :return:按序排列的p1的近邻
    """
    keys = []  # 创建list
    for i in range(1, disMatrix.shape[1] + 1):  # 创建key值
        keys.append(i)
    a = dict(zip(keys, disMatrix[p1 - 1]))  # 压缩字典
    a = sorted(a.items(), key=lambda x: x[1])  # 更新排序后为列表
    neighborArr = []  # p1近邻矩阵的那列
    for i in range(1, len(a)):
        neighborArr.append(a[i][0])  # 把返回的值加入的近邻列
    return neighborArr


def neighborListALL(disMatrix):
    """
    得到完整的近邻矩阵
    :param disMatrix:距离矩阵
    :return:近邻矩阵
    """
    res = []
    for i in range(0, disMatrix.shape[1]):  # 把近邻列加入到近邻矩阵内
        sorted_id = sorted(range(len(disMatrix[i])), key=lambda k: disMatrix[i][k], reverse=False)
        temp=sorted_id
        sorted_id=sorted(range(len(temp)), key=lambda k: temp[k], reverse=False)
        res.append(sorted_id)
    return np.array(res)


def pheromonesList(data):
    pointNum = data.shape[0]
    pheList = []
    for i in range(0, pointNum):
        pheList.append(10)
    return pheList


def randomData(mu, sigma, row, col):
    """
    产生高斯分布数据
    :param mu: 均值
    :param sigma: 标准差
    :param row: 行数
    :param col: 列数
    :return: 高斯分布数据集
    """
    return np.random.normal(mu, sigma, [row, col])


def normalize(list, value):
    range = max(list) - min(list)
    if range == 0:
        return 1
    elif value-min(list)==0:
        return 0
    else:
        value2 = math.exp(math.log(value-min(list)) -math.log(range))
        return value2

def antCreat(m, var_sigma, sigma):
    """
    蚂蚁创建模型
    :param m: 点的数量
    :param var_sigma:  ς 限制奴隶蚂蚁的数量 0<var_sigma<0.5
    :param sigma: σ 限制大蚂蚁的数量 0<sigma_indes<0.2*var_sigma
    :return: n_s奴隶蚂蚁数量  n_m大蚂蚁数量
    """
    # if var_sigma > 0.5 or var_sigma < 0:  # 要保证 0<var_sigma<0.5
    #     print("传入参数有误\n应该满足0<var_sigma<0.5")
    # if sigma < 0 or sigma > 0.2 * var_sigma:  # 要保证 0<sigma_indes<0.2*var_sigma
    #     print("传入参数有误\n应该满足0<sigma<0.2*var_sigma")
    # else:
    n_s = int(var_sigma * m)  # 奴隶蚂蚁数量，为了防止小数所以对结果取整
    n_m = int(sigma * m)  # 主蚂蚁数量，为了防止小数所以对结果取整
    if n_s == 0:
        n_s += 1
    if n_m == 0:
        n_m += 1
    return n_s, n_m



def getDelta(p1, p2, k, neighborMatrix):
    """
    得到Δ([p1,k],p2]) 在k个近邻内，以p1为主视角，p2是p1的第几近邻
    :param p1: 第一个点 index
    :param p2: 第二个点 index
    :param k: k近邻
    :param neighborMatrix: 近邻矩阵
    :return: Δ([p1,k],p2])
    """
    #
    # keys = []
    # for i in range(1, disMatrix.shape[1] + 1):  # 创建key值
    #     keys.append(i)
    # a = dict(zip(keys, disMatrix[p1]))  # 压缩字典
    # a = sorted(a.items(), key=lambda x: x[1])  # 更新排序后为列表
    # delta = 0
    # for i in range(0, k):  # 从更新后的排序里找到p2的位置
    #     if neighborMatrix[p1][i] == p2:
    #         delta = i
    # if delta > k:  # 如果没在k近邻内，则Δ为-1
    #     delta = k
    return neighborMatrix[p1,p2]


def getNabla(p1, p2, neighborMatrix):
    """
    得到Nabla([p1,k],p2]) 在k个近邻内，以p2为主视角，p1是p2的第几近邻
    :param p1: 第一个点
    :param p2: 第二个点
    :param k: k近邻
    :param neighborMatrix: 距离矩阵
    :return: Δ([p1,k],p2])
    """
    # keys = []
    # for i in range(1, disMatrix.shape[1] + 1):  # 创建key值
    #     keys.append(i)
    # a = dict(zip(keys, disMatrix[p1 - 1]))  # 压缩字典
    # a = sorted(a.items(), key=lambda x: x[1])  # 更新排序后为列表
    # delta = 0
    # for i in range(1, len(a)):  # 从更新后的排序里找到p2的位置
    #     if a[i][0] == p2:
    #         delta = i
    return neighborMatrix[p2][p1]


def getSPC(p1, p2, dis, pheList, neighborMatrix):
    """
    获得即点p为中心，与近邻点p1’的从路径信度Subordinate Path Credibility
    :param p1: 第一个点
    :param p2: 第二个点
    :param dis: 距离矩阵
    :param neighborMatrix: 近邻矩阵
    :return: S_pc_<p,p1'> 即以点p为中心，与近邻点p1’的从路径信度Subordinate Path Credibility
    """
    # 信息素
    nowPhe = pheList[p2]
    norPhe = normalize(pheList, nowPhe)

    delta = neighborMatrix[p1][p2]
    nabla = neighborMatrix[p2][p1]
    distance = dis[p1][p2]  # d(p,p1') 即p到p1'的距离，距离矩阵从0开始计数，所以要-1

    factor1 = delta * distance / (nabla + 1)  # 因为前面求的是序号，所以这里要+1，表示第几个
    factor2 = delta * norPhe / (nabla + 1)
    spc = factor1 + factor2
    return spc


def getPPC(p1, p2, kap, dis, neighbor, pheList):
    """
    获得主路径信度Primary Path Credibility
    :param p1: 第一个点。eg：计算第一行数据则输入 1
    :param p2: 第二个点
    :param kap: k'
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :return: PPC: 主路径信度
    """
    nowPhe = pheList[p2]
    factor2 = 0
    sum_spc = 0  # 初始化从路径信度
    getPj = sorted(range(len(neighbor[p2])), key=lambda k: neighbor[p2][k], reverse=False)
    for i in range(0, kap):  # 求从p2到pj的从路径信度，结果累加到sum_pcs上
        pj = getPj[i]
        delta = neighbor[p2][pj]
        slaveNabla = neighbor[pj][p2]
        sum_spc = sum_spc + getSPC(p2, pj, dis, pheList, neighbor)  # p1'的从路径信度
        norPhe = normalize(pheList, nowPhe)
        pj_norPhe = normalize(pheList, pheList[pj])
        if  slaveNabla * (pj_norPhe - norPhe)!=0:
            factor2=factor2+delta/(slaveNabla * (pj_norPhe - norPhe))

    avg_spc = sum_spc / kap  # 计算从路径信度的均值
    avg_factor2 = factor2 / kap
    masterNabla = neighbor[p2][p1]
    factor1 = masterNabla * avg_spc  # 求主路径信度Primary Path Credibility
    PPC = factor1 + avg_factor2
    return PPC


def getMasterAntChoice(p1, k, pheList, dis, neighbor, kap):
    """
    主蚂蚁的选择模型
    :param p1: 出发点
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :param kap: k'
    :return: 在k个近邻里，选择要去的那个点
    """
    k=kap
    sum_ppc = 0  # 初始化主路径信度
    ppc = []
    point_list = []
    pheList_index = sorted(range(len(pheList)), key=lambda k: pheList[k])
    for i in list(range(0, int(k / 2))) + list(range(int(len(pheList_index) - k / 2),
                                                       len(pheList_index))):  # 求从p1到pj的主路径信度，结果累加到sum_pcs上 # 2022.2.24修改 以前遍历所有点，现在遍历信息素列表（从小到大）中前、后各(kap/4)个点

        p2 = pheList_index[i]
        now_ppc = getPPC(p1, p2, kap, dis, neighbor, pheList)
        ppc.append(now_ppc)
        point_list.append(p2)
        sum_ppc = sum_ppc + now_ppc  # p1'的主路径信度
    sum_po = 0
    probability = []
    for i in range(0, len(ppc)):  # 2022.2.24改
        if sum_ppc == 0 or ppc[i]:
            now_probability = 0
        else:
            now_probability = math.exp(math.log(ppc[i]) - math.log(sum_ppc))
        probability.append(now_probability)
        sum_po += now_probability

    res = roulette(probability)
    choice_point = point_list[res]
    return choice_point


def getTau(dis, toReachPoint, fromReachPoint, localdensity_k):
    toTau = np.mean(sorted(dis[toReachPoint])[0:localdensity_k])
    fromTau = np.mean(sorted(dis[fromReachPoint])[0:localdensity_k])
    now_tau = toTau-fromTau
    return now_tau

def getSlaveAntChoice(p1, k, pheList, dis, neighbor):
    """
    奴隶蚂蚁的选择模型
    :param p1: 出发点 index
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :return: 在k个近邻里，选择要去的那个点
    """
    sum_spc = 0  # 初始化从路径信度
    spc = []
    point_list = []
    neighbor_index = sorted(range(len(neighbor[p1])), key=lambda k: neighbor[p1][k])
    for i in range(0, k):  # 求从p1到pj的从路径信度，结果累加到sum_pcs上
        p2 = neighbor_index[i]  # 求p2,p2为index,最小值为0
        now_spc = getSPC(p1, p2, dis, pheList, neighbor)
        spc.append(now_spc)
        point_list.append(p2)
        sum_spc = sum_spc + now_spc  # p1'的从路径信度
    sum_po = 0
    probability = []
    for i in range(0, k):
        if sum_spc == 0 or spc[i] == 0:
            now_probability = 0
        else:
            now_probability = math.exp(math.log(spc[i]) - math.log(sum_spc))
        probability.append(now_probability)
        sum_po += now_probability
    res = roulette(probability)
    choice_point = point_list[res]
    return choice_point




def pheromonesUpdata(oldPheromones, delta, nabla, dis, toPoint, frompoint, tauTrainlist, pheList):
    """
    信息素更新

    """
    # --------factor4-----------
    # 对pheList初始化
    # maxPhe = max(pheList)
    # minPhe = min(pheList)
    # oldPhe = oldPheromones
    normalizedPhe = normalize(pheList,oldPheromones)
    # Get factor4
    factor4 = normalizedPhe
    # --X------factory4---------X--

    considerneighbor_num = max(delta, nabla)
    factor3 = avgdistance(frompoint, toPoint, dis, considerneighbor_num)
    # factor3 = 1
    factor2 = (nabla+1) / (delta+1)

    range_min = -10
    range_max = 10
    if len(tauTrainlist)!=0:
        k = (range_max - range_min) / (max(tauTrainlist) - min(tauTrainlist))
        transform_value = [k * (x - min(tauTrainlist)) + range_min for x in tauTrainlist]
    else:
        transform_value=[0]

    # k = (range_max - range_min) / (max(tauTrainlist) - min(tauTrainlist))
    # transform_value = [(range_max - range_min) * (x - min(tauTrainlist)/ (max(tauTrainlist) - min(tauTrainlist)) ) + range_min for x in tauTrainlist]



    factor1 = transform_value[-1]

    newPheromones = oldPheromones + factor1 * factor3 + factor2  * factor4

    return newPheromones


def avgdistance(frompoint, toPoint, dis, considerneighbor_num):
    if considerneighbor_num == 0:  # 表示两个点之间无其他点
        return 1
    else:
        neardisarray_from=0
        neardisarray_to=0
        sortdis_from = dis[frompoint].argsort()  # 获取距离从小到大的近邻序号
        sortdis_to = dis[toPoint].argsort()
        for i in range(0,considerneighbor_num):
            neardisarray_from=neardisarray_from+dis[frompoint][sortdis_from[i]]
            neardisarray_to=neardisarray_to+ dis[toPoint][sortdis_to[i]]
        # neardisarray_from = dis[frompoint][sortdis_from[1:considerneighbor_num]]  # 获取前considerneighbor_num个最近的距离
        pointdismean_from = np.mean(neardisarray_from)  # 计算平均距离
        pointdismean_to = np.mean(neardisarray_to)
        if pointdismean_to==0 or pointdismean_to==0:
            return 1
        factor3 = (pointdismean_to+1) / (pointdismean_from+1)
        return factor3





def map(data, MIN, MAX):
    """
    归一化映射到任意区间
    :param data: 数据
    :param MIN: 目标数据最小值
    :param MAX: 目标数据最小值
    :return:
    """
    d_min = np.max(data)  # 当前数据最大值
    d_max = np.min(data)  # 当前数据最小值
    return MIN + (MAX - MIN) / (d_max - d_min) * (data - d_min)



def slaveAntPathExpansionModel(k, pheList, dis, neighbor, eta, dataAnal):
    """

    :param p1:起始点的index
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :param eta: eta，控制蚂蚁死亡
    :param dataAnal: 记录每个点被选择成为下一个爬行的点的次数
    :return:
    """
    getTaopara = 4
    tauTrainlist = []
    p1 = pheList.index(min(pheList))
    epsilon = []
    reachPoint = [p1]  # index
    tau = []
    i = 0
    while eta > 0:
        if len(set(reachPoint)) == dis.shape[0] or len(reachPoint) == dis.shape[0]:  # 修改1：条件1：确定跑完所有点（需要去重复）；条件2：遍历达到一定次数.结束遍历
            break
        nextpoint = getSlaveAntChoice(reachPoint[-1] , k, pheList, dis, neighbor)  # 选择下一个要去的点
        dataAnal[nextpoint] += 1
        reachPoint.append(nextpoint)  # 把它加入到达点的列表
        distance = dis[reachPoint[-2]][nextpoint - 1]  # 算出p1 p2的距离
        epsilon.append(distance)  # 计算epsilon
        if i >= 1:
            now_tau = getTau(dis, reachPoint[-1], reachPoint[-2], getTaopara)  # 计算现在的τ
            tauTrainlist.append(now_tau)
            tau.append(now_tau)  # 把现在的τ添加到τ列表里面
            new_eta = etaUpdate(eta, epsilon, now_tau)  # 计算蚂蚁的eta
            eta = new_eta
            nowReachPoint = reachPoint[i + 1]
            oldPhe = pheList[nowReachPoint]
            delta=neighbor[reachPoint[-2],reachPoint[-1]]
            nabla=neighbor[reachPoint[-1],reachPoint[-2]]
            pheList[nowReachPoint - 1] = pheromonesUpdata(oldPhe, delta, nabla, dis, nowReachPoint,
                                                                           reachPoint[-2], tauTrainlist,
                                                                           pheList)  # 更新信息素列表

        tauTrainElem = getTau(dis, reachPoint[-1], reachPoint[-2], getTaopara)
        tauTrainlist.append(tauTrainElem)
        eta = eta - 0.3
        i = i + 1
    return


def masterAntPathExpansionModel(k, pheList, dis, neighbor, eta, kap, dataAnal):
    """
    :param p1:起始点 index
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :param eta: eta，控制蚂蚁死亡
    :param kap: k'，p2的k近邻
    :param dataAnal: 记录每个点被选择成为下一个爬行的点的次数
    :return:
    """
    getTaopara = 4
    tauTrainlist = []
    p1 = pheList.index(min(pheList))
    i = 0
    epsilon = []
    reachPoint = [p1]
    tau = []
    while eta > 0:  # 蚂蚁活着时
        if len(list(set(reachPoint))) == dis.shape[0] or len(reachPoint) == dis.shape[
            0]:  # 修改1：条件1：确定跑完所有点（需要去重复）；条件2：遍历达到一定次数.结束遍历
            break
        nextpoint = getMasterAntChoice(reachPoint[-1], k, pheList, dis, neighbor,
                                                 kap)  # 修改2：不采用p1的计算方法，统一用reachPoint数组取值。这里选择下一个要去的点
        dataAnal[nextpoint] += 1
        reachPoint.append(nextpoint)  # 把它加入到达点的列表
        distance = dis[reachPoint[-2]][nextpoint]  # 算出p1 p2的距离
        epsilon.append(distance)  # 计算epsilon
        if i >= 1:
            now_tau = getTau(dis, reachPoint[-1], reachPoint[-2], getTaopara)  # 计算现在的τ
            tau.append(now_tau)  # 把现在的τ添加到τ列表里面
            new_eta = etaUpdate(eta, epsilon, now_tau)  # 计算蚂蚁的eta
            eta = new_eta
            nowReachPoint = reachPoint[i]  # 新到的点
            oldPhe = pheList[nowReachPoint - 1]  # oldPhe是指reachPoint数组最新（最后）的一个点的信息素
            delta=neighbor[reachPoint[-2],reachPoint[-1]]
            nabla=neighbor[reachPoint[-1],reachPoint[-2]]
            pheList[nowReachPoint - 1] = pheromonesUpdata(oldPhe, delta, nabla, dis, nowReachPoint,
                                                                           reachPoint[-2], tauTrainlist,
                                                                           pheList)  # 更新信息素列表
        eta = eta - 0.3
        i = i + 1
    return


def etaUpdate(eta, epsilonList, now_tau):
    """
    eta更新
    :param eta:旧的eta
    :param epsilonList:epsilon列表
    :param now_tau: 现在的tau
    :return: 更新后的eta
    """
    sum_eps = 0  # 算出总的epsilon
    for i in range(0, len(epsilonList)):
        sum_eps += epsilonList[i]
    avg_eps = sum_eps / len(epsilonList)
    if avg_eps==0:
        return 0
    else:
        new_eta = eta + now_tau / avg_eps
        return new_eta



def antModel(data, k, kap, eta, round,slave_ant_proportion,master_ant_proportion):
    """
    找孤立点
    :param data: 数据集
    :param k:k近邻
    :param kap: k'
    :param eta: eta，控制蚂蚁生命
    :param round: 执行几轮，每轮由一次主蚂蚁跑+一次奴隶蚂蚁跑
    :param slave_ant_proportion: 奴隶蚂蚁在数据集中的占比
    :param master_ant_proportion: 主蚂蚁在数据集中的占比
    :return:
    """
    dis = distanceMatrix(data)  # 求距离矩阵
    dis = (dis - np.min(dis)) / (np.max(dis) - np.min(dis))  # 距离矩阵归一化
    neighborMatrix = neighborListALL(dis)  # 求近邻矩阵
    pheList = pheromonesList(data)  # 求信息素矩阵
    n_s, n_m = antCreat(data.shape[0], slave_ant_proportion, master_ant_proportion)  # 求奴隶蚂蚁数、主蚂蚁数

    # #-------- analysis-----------------------
    # 定义分析数据
    dataAnal = [0] * data.shape[0]
    # 主蚂蚁和奴隶蚂蚁交替跑
    for i in range(0, round):
        # print("***************这是第", i + 1, "轮***************")
        for l in range(0, int(n_s)):  # 奴隶蚂蚁跑，修改：不能用变量k
            # print("***************这是第", l + 1, "只蚂蚁SA***************")
            slaveAntPathExpansionModel(k, pheList, dis, neighborMatrix, eta, dataAnal)
        for j in range(0, int(n_m)):  # 主蚂蚁跑
            # print("***************这是第", j + 1, "只蚂蚁MA***************")
            masterAntPathExpansionModel( k, pheList, dis, neighborMatrix, eta, kap, dataAnal)
    return pheList
