# _*_ coding:utf-8 _*_
import re
import h5py
from base_dir import dataPath

future_name_list = ['A.DCE', 'AG.SHF', 'AU.SHF', 'I.DCE', 'IC.CFE', 'IF.CFE', 'IH.CFE',
                    'J.DCE', 'JM.DCE', 'M.DCE', 'RB.SHF', 'Y.DCE', 'ZC.CZC']


def compute_gradient_in_one_file(final_result, raw_data):
    raw_data_keys = list(raw_data.keys())
    # 遍历所有矩阵
    for i in range(0, raw_data_keys.__len__()):
        time = raw_data_keys[i]
        # 提取日期
        time_match = re.match('(\d+.*\d+) .*', time)
        if time_match:
            date = time_match.group(1)
        data_matrix = raw_data[time][:]
        # 遍历矩阵中的每一行
        for j in range(0, future_name_list.__len__()):
            futureName = future_name_list[j]
            if futureName not in final_result:
                final_result[futureName] = {}
            if date not in final_result[futureName]:
                final_result[futureName][date] = []
            # 求收益率, 放入对应list
            open_price = data_matrix[j, 0]
            close_price = data_matrix[j, 3]
            final_result[futureName][date].append((close_price - open_price) / (open_price))
    return final_result


# 返回值是一个字典
# key = futureName
# value是每天的变化率
def get_gradient():
    final_result = {}
    raw_data1 = h5py.File(dataPath + 'data_format2_20170717_20170915.h5', 'r')
    raw_data2 = h5py.File(dataPath + 'data_format2_20170918_20170922.h5', 'r')
    raw_data3 = h5py.File(dataPath + 'data_format2_20170925_20170929.h5', 'r')
    final_result = compute_gradient_in_one_file(final_result, raw_data1)
    final_result = compute_gradient_in_one_file(final_result, raw_data2)
    final_result = compute_gradient_in_one_file(final_result, raw_data3)
    return final_result