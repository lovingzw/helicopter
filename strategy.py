import numpy as np
from functions import trend, gradient, decision, operation, close, adjust

asset_index1 = 7  # define item 1 as coke
asset_index2 = 8  # define item 2 as coal
underwear = 9000000  # define balance limit


def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):

    position_new = detail_last_min[0]

    if timer == 0:
        memory.status = 0  # -1, stop loss; 0, ready; 1, open
        memory.asset = init_cash

    if  memory.status == -1:
        if (timer - memory.stop_loss_time) % 120 == 0:
            memory.status = 0

    if memory.status == 0:  # ready to open

        gradient1 = gradient(asset_index1, data)
        gradient2 = gradient(asset_index2, data)
        delta = gradient1 - gradient2

        if abs(delta) > 3 * transaction:  # just to ensure interest

            current_trend = trend(asset_index1, asset_index2, data)  # trend detection
            index = decision(delta, current_trend, asset_index1, asset_index2)  # item decision
            operate_index = index[0]
            target_index = index[1]
            memory.operate_price = data[operate_index, 0]
            memory.target_price = data[target_index, 0]
            memory.operate_index = operate_index
            memory.target_index = target_index
            memory.operate_time = timer
            memory.trend = current_trend

            position_new = operation(data, detail_last_min, info, operate_index, transaction, current_trend, underwear,)
            memory.position = position_new
            memory.asset = detail_last_min[2]
            memory.status = 1

    else:
        if memory.status == 1:  # adjustment (stop loss or close out)
            position_new = adjust(detail_last_min, memory, timer)

            if close(memory, timer, data):  # close out
                memory.status = 0
                position_new = np.zeros(13, dtype=np.int)

    return position_new, memory


if __name__ == '__main__':
    print('Hello!\nThis demo needs no model so there is no training here')
