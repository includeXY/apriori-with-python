import numpy as np
import apriori as ap

"""
    测试
"""
filename='D:\study\Data Mining\上机实验数据文件.txt'                       #测试实验文本数据
data_set=ap.load_data_set(filename)
#data_set = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
#            ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
#            ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]     #测试课本例6.3
L,support_data=ap.generate_L(data_set,3,0.15)                                   #k=3,支持度=0.15
big_rule_list=ap.generate_big_rules(L,support_data,0.7)                        #置信度=0.7
for Lk in L:
    if len(Lk)!=0:
        print('='*50)
        print('frequent '+str(len(list(Lk)[0]))+'-itemsets\t\tsupport')
        print('='*50)
        for freq_set in Lk:
            print (freq_set,support_data[freq_set])
print('='*50)
if len(big_rule_list) == 0:
    print('No Big Rules!')
else:
    print('Big Rules')
    for item in  big_rule_list:
        print (item[0],'=>',item[1],'conf: ',item[2])
