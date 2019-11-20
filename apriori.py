import pandas as pd
def load_data_set(filename):
    items_txt = pd.read_csv(filename,header=None)
    data=items_txt.values.tolist()      #将pd.read_csv读入的文本数据转换为数组，数组的每个元素都是一个字符串
    L=len(data)                         #求数组的条目数
    data_set = []
    for i in range(0,L):
        t=data[i][0].split()             #将字符串按空格差分，默认删除空格
        data_set.append(t)
    return data_set
def creat_C1(data_set):
    """"
    data_set: 所有事务的集合，每个事务是项的集合
    遍历所有的事务，生成频繁候选1项集
    Returns:
       C1: 所有频繁1项候选集的集合
    """
    C1 = set()   #class set([iterable])创建一个无序不重复的数据集,可变集合无法作为字典的key
    for t in data_set:
        for item in t:
            item_set = frozenset([item])   #返回一个冻结的集合，冻结后的集合不能再添加或删除任何元素，如参数缺省，默认生成空集合
            C1.add(item_set)             #将返回的集合作为1项集插入到集合C1中
    return C1

def is_apriori(Ck_item,Lksubl):
    """
    由于存在先验性质：任何非频繁的(k-1)项集都不是频繁k项集的子集。
    因此，如果一个候选k项集Ck的(k-1)项子集不在Lk-1中，则该候选也不可能是频繁的，
    从而可以从Ck中删除，获得压缩后的Ck。
    该函数用于判断一个频繁k项候选集是否满足先验性质
    参数：
        Ck_item：Ck中的一个频繁候选k项集
        Lksubl：Lk-1,包含所有频繁k-1项集的集合（a set which contains all frequent candidate (k-1)-itemsets.）
    return：
        True: 符合先验性质
        False: 不符合先验性质
    """
    for item in Ck_item:
        sub_Ck = Ck_item-frozenset([item])     #sub_Ck保存一个待验证的频繁候选k-1项集
        if sub_Ck not in Lksubl:
            return False
    return True

def create_Ck(Lksub1, k):
    """
    通过将所有的频繁k-1项集连接得到频繁候选k项集的集合Ck
    Args:
        Lksub1:所有屏藩k-1项集的集合
        k: 频繁k项集的项数
    Return:
        Ck: 所有频繁候选k项集的集合
    """
    Ck = set()
    len_Lksub1 = len(Lksub1)       #返回Lksubl集合的元素个数
    list_Lksub1 = list(Lksub1)     #返回保存Lksubl中元素的列表
    for i in range(len_Lksub1):    #range(len_Lksubl)返回0到len_Lksubl的整数数组
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()                     #将l1和l2按字典序排序
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]    #将所有前k-2项相同的频繁k-1项集连接产生频繁候选k项集
                # 剪枝操作
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck

def generate_Lk_by_Ck(data_set,Ck,min_support,support_data):
    """
    统计Ck中的频繁候选项是否满足最小支持度，将不满足的删除，满足的保留，得到Lk。
    参数：
        data_set：保存所有事务的数组，每个事务是数组中的一个元素
        Ck：频繁候选项集的集合
        min_support：最小支持度的阈值
        support_data:一个字典，由频繁项集和其支持度的关键字对组成
    return：
        Lk：所有频繁k项集的集合
    """
    Lk=set()              #定义Lk为可变的，非重复无序的数组
    item_count={}          #item_cout是一个字典，用于统计候选项集Ck中每个候选项集在事务集中出现的次数
    """
        统计Ck中频繁候选项集在出现在事务集中的次数，即支持计数
    """
    for t in data_set:   #遍历所有事务
        for item in Ck:  #遍历Ck中的所有频繁候选k项集
            if item.issubset(t):       #判断item是否是t的一个子集，是则返回True，否则返回False
                if item not in item_count:
                    item_count[item]=1
                else:
                    item_count[item]+=1
    t_num=float(len(data_set))       #将事物集中的事务数以float的形式返回给t_num，之所以是float型，是为了一步的除法做准备
    """
    将Ck中不小于支持度阈值的频繁候选项集保留下来，并添加到Lk中；
    使用support_data保存每个频繁k项集的支持度
    """
    for item in item_count:
        if (item_count[item]/t_num >= min_support):
            Lk.add(item)
            support_data[item]=item_count[item]/t_num
    return Lk

def generate_L(data_set,k,min_support):
    """
        生成所有的频繁项集
        参数：
            data_set：所有事务组成的列表
            k:频繁项集中的最大项数
            min_support:最小支持度的阈值
        return:
            L:保存所有Lk的列表
            support_data:一个字典，由频繁项集和其支持度的关键字对组成
    """
    support_data={}        #定义一个空字典
    C1=creat_C1(data_set)
    L1=generate_Lk_by_Ck(data_set,C1,min_support,support_data)
    Lksubl=L1.copy()
    L=[]                  #定义一个空列表
    L.append(Lksubl)
    for i in range(2,k+1):          #range(2,k+1)生成一个2到k的整数数组，包括首位端的数
        Ci=create_Ck(Lksubl,i)
        Li=generate_Lk_by_Ck(data_set,Ci,min_support,support_data)
        Lksubl=Li.copy()
        L.append(Lksubl)
    return L,support_data

def generate_big_rules(L,support_data,min_conf):
    """
        由频繁项集产生强关联规则
        参数：
            L：保存所有Lk的列表
            support_data:一个字典，由频繁项集和其支持度的关键字对组成
            min_conf:最小置信度的阈值
        returns：
            big_rules_list:一个保存所有强关联规则的列表，每个强关联规则big_rule是一个三元组[A,B,conf]表示A=>B的confidence=conf
    """
    big_rule_list=[]        #定义一个保存所有强关联规则的列表，初始化为空
    sub_set_list=[]         #定义一个保存所有频繁项集的列表，初始化为空
    for i in range(0,len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf=support_data[freq_set]/support_data[freq_set-sub_set]
                    big_rule=(freq_set-sub_set,sub_set,conf)
                    if conf>=min_conf and big_rule not in big_rule_list:
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list