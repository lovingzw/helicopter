import numpy as np

index1 = 7  # define item as coke
underwear = 5000000  # define balance limit
vol_threshold = 1.8
zscore_threshold = 0.68
partition = 0.9


def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    position_new = detail_last_min[0]

    if timer == 0:
        memory.status = 0  # -1, stop loss; 0, ready; 1, open
        memory.s1 = np.mean(data[index1, 0:3])
        memory.vol = data[index1, 4]
    elif timer == 1:
        memory.s1 = np.array([memory.s1, np.mean(data[index1, 0:3])])
        memory.vol = np.array([memory.vol, data[index1, 4]])
    elif 0 < timer < 60:
        memory.s1 = np.append(memory.s1, np.mean(data[index1, 0:3]))
        memory.vol = np.append(memory.vol, data[index1, 4])
    else:
        current_price = np.mean(data[index1, 0:3])
        current_vol = data[index1, 4]
        memory.s1 = np.append(memory.s1[1:59], current_price)
        memory.vol = np.append(memory.s1[1:59], current_vol)

        avg10_price = np.mean(memory.s1[-10:-1])
        avg10_vol = np.mean(memory.vol[-10:-1])
        avg60_price = np.mean(memory.s1)
        avg60_vol = np.mean(memory.vol)
        std60_price = np.std(memory.s1)
        std60_vol = np.std(memory.vol)
        zscore_price = (current_price - avg60_price) / std60_price
        zscore_vol = (current_vol - avg60_vol) / std60_vol
        trigger1 = current_vol > avg60_vol * vol_threshold  # volume
        trigger2 = abs(zscore_vol) > zscore_threshold  # volume
        trigger3 = abs(zscore_price) > zscore_threshold  # price

        if trigger1 and trigger2 and trigger3:
            if current_price > avg10_price:
                trend = 1
            else:
                trend = -1
        else:
            trend = 0

        if memory.status == -1:  # hold after stop loss
            if (timer - memory.stop_loss_time) % 120 == 0:
                memory.status = 0
        elif memory.status == 0:  # ready to open
            if trend != 0 and detail_last_min[4] > underwear:
                money_pool = (detail_last_min[1] - underwear) * partition
                lot_value = current_price * info.unit_per_lot[index1] * info.margin_rate[index1]
                position_new[index1] = trend * np.floor(money_pool / (lot_value * (1. + transaction)))
                memory.top = detail_last_min[4]
                memory.total = detail_last_min[4]
                memory.status = 1
                memory.trend = trend
        else:
            memory.top = np.maximum(detail_last_min[4], memory.top)
            if (detail_last_min[4] - memory.top) / memory.top < -0.08:  # stop loss
                memory.stop_loss_time = timer
                position_new[index1] = 0
                memory.status = -1
                print('stop loss')
            else:
                if trend == 0:  # close out
                    position_new[index1] = 0
                    memory.status = 0

    return position_new, memory


if __name__ == '__main__':
    print('Hello!\nThis demo needs no model so there is no training here')