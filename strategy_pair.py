import numpy as np
from functions import pair_open

index1 = 7  # define item 1 as coke
index2 = 8  # define item 2 as coal
underwear = 5000000  # define balance limit
threshold_open = 1
threshold_close = 0.1


def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    position_new = detail_last_min[0]

    if timer == 0:
        memory.status = 0  # -1, stop loss; 0, ready; 1, open
        memory.s1 = np.mean(data[index1, 0:3])
        memory.s2 = np.mean(data[index2, 0:3])
        memory.vol = data[index1, 4] + data[index2, 4]
    elif timer == 1:
        memory.s1 = np.array([memory.s1, np.mean(data[index1, 0:3])])
        memory.s2 = np.array([memory.s2, np.mean(data[index2, 0:3])])
        memory.vol = np.array([memory.vol, data[index1, 4] + data[index2, 4]])
    elif 0 < timer < 60:
        memory.s1 = np.append(memory.s1, np.mean(data[index1, 0:3]))
        memory.s2 = np.append(memory.s2, np.mean(data[index2, 0:3]))
        memory.vol = np.append(memory.vol, data[index1, 4] + data[index2, 4])
    else:
        memory.s1 = np.append(memory.s1[1:59], np.mean(data[index1, 0:3]))
        memory.s2 = np.append(memory.s2[1:59], np.mean(data[index2, 0:3]))
        memory.vol = np.append(memory.vol[1:59], data[index1, 4] + data[index2, 4])
        diff = memory.s1 - memory.s2
        current_delta = np.mean(data[index1, 0:3]) - np.mean(data[index2, 0:3])
        avg5_diff = np.mean(diff[55:59])
        avg60_diff = np.mean(diff)
        std60 = np.std(diff)
        zscore = (current_delta - avg60_diff) / std60
        if avg5_diff - avg60_diff > 0:
            vib = 1
        else:
            vib = -1

        if memory.status == -1:
            if (timer - memory.stop_loss_time) % 120 == 0:
                memory.status = 0
        elif memory.status == 0:  # ready to open
            if abs(zscore) > threshold_open:
                money_pool = detail_last_min[4] - underwear
                position_new = pair_open(detail_last_min, data, info, transaction, index1, index2, money_pool, zscore, vib)
                memory.top = detail_last_min[4]
                memory.total = detail_last_min[4]
                memory.status = 1
        else:
            memory.top = np.maximum(detail_last_min[4], memory.top)
            if (detail_last_min[4] - memory.top) / memory.top < -0.08:  # stop loss
                memory.stop_loss_time = timer
                position_new[index1] = 0
                position_new[index2] = 0
                memory.status = -1
                print('stop loss')
            else:
                if threshold_close > abs(zscore) and detail_last_min[4] > memory.total * 1.0001:  # close out
                    position_new[index1] = 0
                    position_new[index2] = 0
                    memory.status = 0

    return position_new, memory


if __name__ == '__main__':
    print('Hello!\nThis demo needs no model so there is no training here')