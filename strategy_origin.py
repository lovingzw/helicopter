import numpy as np
from functions import trend, gradient, decision, operation, close, peak_update

asset_index1 = 7  # define item 1 as coke
asset_index2 = 8  # define item 2 as coal
underwear = 5000000  # define balance limit


def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    if timer == 0:
        memory.status = 0  # -1, stop loss; 0, ready; 1, open

    position_new = detail_last_min[0]

    if memory.status == -1:
        if (timer - memory.stop_loss_time) % 120 == 0:
            memory.status = 0
    elif memory.status == 0:  # ready to open

        grd = [0, 0]
        grd[0] = gradient(asset_index1, data)
        grd[1] = gradient(asset_index2, data)
        delta = grd[0] - grd[1]

        if abs(delta) > 3 * transaction:  # just to ensure interest

            current_trend = trend(asset_index1, asset_index2, grd, data)  # trend detection
            index = decision(delta, current_trend, asset_index1, asset_index2)  # item decision
            operate_index = index[0]
            target_index = index[1]
            memory.operate_price = np.mean(data[operate_index, 0:3])
            memory.target_price = np.mean(data[target_index, 0:3])
            memory.operate_index = operate_index
            memory.target_index = target_index
            memory.operate_time = timer
            memory.trend = current_trend

            position_new = operation(data, detail_last_min, info, operate_index, transaction, current_trend, underwear)
            memory.position = position_new
            memory.top = detail_last_min[4] - underwear
            memory.total = detail_last_min[4]
            memory.status = 1
    else:
        memory.top = peak_update(detail_last_min, memory)
        if (detail_last_min[4] - memory.top) / memory.top < -0.1:  # stop loss
            position_new = np.zeros(13, dtype=np.int)
            memory.stop_loss_time = timer
            memory.status = -1
            print("stop loss")

        if close(detail_last_min, memory, timer, data):  # close out
            position_new = np.zeros(13, dtype=np.int)
            memory.status = 0
            if timer > 8300:
                print('deal')

    return position_new, memory


if __name__ == '__main__':
    print('Hello!\nThis demo needs no model so there is no training here')