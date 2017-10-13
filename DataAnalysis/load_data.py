# _*_ coding:utf-8 _*_
import re
import h5py
from base_dir import dataPath

future_name_list = ['A.DCE', 'AG.SHF', 'AU.SHF', 'I.DCE', 'IC.CFE', 'IF.CFE', 'IH.CFE',
                    'J.DCE', 'JM.DCE', 'M.DCE', 'RB.SHF', 'Y.DCE', 'ZC.CZC']
# 日期，用做参考
# date_list = ['2017-07-17', '2017-07-18', '2017-07-19', '2017-07-20', '2017-07-21', '2017-07-24',
#              '2017-07-25', '2017-07-26', '2017-07-27', '2017-07-28', '2017-07-31', '2017-08-01',
#              '2017-08-02', '2017-08-03', '2017-08-04', '2017-08-07', '2017-08-08', '2017-08-09',
#              '2017-08-10', '2017-08-11', '2017-08-14', '2017-08-15', '2017-08-16', '2017-08-17',
#              '2017-08-18', '2017-08-21', '2017-08-22', '2017-08-23', '2017-08-24', '2017-08-25',
#              '2017-08-28', '2017-08-29', '2017-08-30', '2017-08-31', '2017-09-01', '2017-09-04',
#              '2017-09-05', '2017-09-06', '2017-09-07', '2017-09-08', '2017-09-11', '2017-09-12',
#              '2017-09-13', '2017-09-14', '2017-09-15', '2017-09-18', '2017-09-19', '2017-09-20',
#              '2017-09-21', '2017-09-22', '2017-09-25', '2017-09-26', '2017-09-27', '2017-09-28',
#              '2017-09-29']

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


def get_gradient_list():
    gradient = get_gradient()
    gradient_list = {}
    futures = list(gradient.keys())
    date_list = list(gradient[futures[0]].keys())
    date_list.sort()
    print(date_list)
    for future in futures:
        gradient_list[future] = []
        for date in date_list:
            gradient_list[future].append(gradient[future][date])
    return gradient_list