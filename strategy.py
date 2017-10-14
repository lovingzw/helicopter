import numpy as np
from functions import average, gradient

asset_index1 = 7  # define item 1 as coke
asset_index2 = 8  # define item 2 as coal
toss = 2000000


def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):

    position_new = detail_last_min[0]

    if timer == 0:
        memory.status = 0

    if memory.status == 0:

        gradient1 = gradient(asset_index1, data)
        gradient2 = gradient(asset_index2, data)
        diff = gradient1 - gradient2

        if abs(diff) > 3 * transaction:  # just to ensure interest

            if average(gradient1, gradient2) >= 0:  # determine the trend
                trend = 1
            else:
                trend = -1
            if (diff > 0 and trend == 1) or (diff < 0 and trend == -1):  # determine which one to operate
                operate_index = asset_index2
                target_index = asset_index1
            else:
                operate_index = asset_index1
                target_index = asset_index2

            avg_price = np.mean(data[operate_index, 0:3])
            lot_value = avg_price * info.unit_per_lot[operate_index] * info.margin_rate[operate_index]
            volume = np.round(toss / (lot_value * (1. + transaction)))

            if detail_last_min[1] > 3000000:
                if trend == 1:
                    position_new[operate_index] = volume
                else:
                    position_new[operate_index] = -volume

            memory.operate_price = data[operate_index, 0]
            memory.target_price = data[target_index, 0]
            memory.volume = volume
            memory.operate_index = operate_index
            memory.target_index = target_index
            memory.asset_operate = detail_last_min[1]
            memory.operate_time = timer
            memory.trend = trend
            memory.position = position_new
            memory.status = 1

    else:
        if detail_last_min[1] / memory.asset_operate < 0.9:  # stop loss
            memory.status = 0
            position_new = np.zeros(13, dtype=np.int)
        else:
            duration = timer - memory.operate_time
            operate_slope = (data[memory.operate_index, 3] - memory.operate_price) / (memory.operate_price * duration)
            target_slope = (data[memory.target_index, 3] - memory.target_price) / (memory.target_price * duration)
            if (operate_slope >= 2 * target_slope and memory.trend == 1) or (
                            operate_slope <= 2 * target_slope and memory.trend == -1):
                memory.status = 0
                position_new = np.zeros(13, dtype=np.int)


    return position_new, memory


if __name__ == '__main__':
    print('Hello!\nThis demo needs no model so there is no training here')
