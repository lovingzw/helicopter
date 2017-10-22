import numpy as np


def gradient(x, data):  # input index, output current gradient
    g = (data[x, 3] - data[x, 0]) / data[x, 0]
    return g


def trend(a, b, g, data):  # trend detection needs improvement
    w1 = data[a, 4] / (data[a, 4] + data[b, 4])
    w2 = data[b, 4] / (data[a, 4] + data[b, 4])
    t = (w1 * g[0] + w2 * g[1]) / 2
    if t >= 0:
        tr = 1
    else:
        tr = -1
    return tr


def decision(d, trd, a, b):
    if (d > 0 and trd == 1) or (d < 0 and trd == -1):  # determine which one to operate
        operate_index = b
        target_index = a
    else:
        operate_index = a
        target_index = b
    index = [operate_index, target_index]
    return index


def operation(data, detail_last_min, info, operate_index, transaction, trd, underwear):
    p = detail_last_min[0]
    avg_price = np.mean(data[operate_index, 0:3])
    lot_value = avg_price * info.unit_per_lot[operate_index] * info.margin_rate[operate_index]

    money_pool = detail_last_min[1] - underwear
    volume = np.round(money_pool / (lot_value * (1. + transaction)))
    if detail_last_min[4] > underwear:
        if trd == 1:
            p[operate_index] = volume
        else:
            p[operate_index] = -volume
    return p


def adjust(detail_last_min, memory, timer):
    p = detail_last_min[0]
    if (detail_last_min[4] - memory.top) / memory.top < -0.1:  # stop loss
        memory.status = -1
        memory.stop_loss_time = timer
        p = np.zeros(13, dtype=np.int)
        print("stop loss")
    return p


def peak_update(detail_last_min, memory):
    return np.maximum(detail_last_min[2], memory.top)


def close(detail_last_min, memory, timer, data):
    c = False
    duration = timer - memory.operate_time
    s1 = (data[memory.operate_index, 3] - memory.operate_price) / (memory.operate_price * duration)
    s2 = (data[memory.target_index, 3] - memory.target_price) / (memory.target_price * duration)
    flag1 =  (s1 >= 2 * s2 and memory.trend == 1) or (s1 <= 2 * s2 and memory.trend == -1)
    #flag2 = detail_last_min[4] > memory.total
    if flag1:
         c = True
    return c


def pair_close(detail_last_min, zscore):
    p = detail_last_min[0]
    if abs(zscore < 0.1):
        p = np.zeros(13,dtype=int)
    return p


def pair_open(detail_last_min, data, info, transaction, index1, index2, money_pool, zscore, vibr):
    p = detail_last_min[0]
    avg_price1 = np.mean(data[index1, 0:3])
    lot_value1 = avg_price1 * info.unit_per_lot[index1] * info.margin_rate[index1]
    avg_price2 = np.mean(data[index2, 0:3])
    lot_value2 = avg_price2 * info.unit_per_lot[index2] * info.margin_rate[index2]
    if vibr == 1:
        if zscore > 0:
            p[index1] = -np.floor((money_pool * 0.45) / (lot_value1 *(1. + transaction)))
            p[index2] = np.floor((money_pool * 0.55) / (lot_value2 * (1. + transaction)))
        else:
            p[index1] = np.floor((money_pool * 0.55) / (lot_value1 * (1. + transaction)))
            p[index2] = -np.floor((money_pool * 0.45) / (lot_value2 * (1. + transaction)))
    else:
        if zscore > 0:
            p[index1] = -np.floor((money_pool * 0.55) / (lot_value1 * (1. + transaction)))
            p[index2] = np.floor((money_pool * 0.45) / (lot_value2 * (1. + transaction)))
        else:
            p[index1] = np.floor((money_pool * 0.45) / (lot_value1 * (1. + transaction)))
            p[index2] = -np.floor((money_pool * 0.55) / (lot_value2 * (1. + transaction)))
    return p




def buy(position, index, amount_cash, data, info, transaction):
    """
    Buy certain amount of lots for one future
    :param position: list,current position
    :param index: int, one certain future index
    :param amount_cash: double, amount of cash to buy
    :param data: pandas.dataframe, data for current minute bar
    :param info: pandas.dataframe, information matrix
    :param transaction: double, transaction fee
    :return: returns nothing
    """
    # Get execution price of this minute
    avg_price = np.mean(data[index, 0:3])

    # Get the value of one lot so that you can get how many lots you can buy in total
    lot_value = avg_price * info.unit_per_lot[index] * info.margin_rate[index]

    position[index] = np.floor(amount_cash / (lot_value * (1. + transaction)))

    return True


def sell(position, index):
    """
    Sell all lots for one future
    :param position: list,current position
    :param index: int, one certain future index
    """
    position[index] = 0
