import requests, statistics, math, time
from datetime import datetime
from pprint import pprint

import xmrchainapi

check_period = 240

while True:
    # get last networkinfo data
    data_info = xmrchainapi.getjson("networkinfo")
    # get last mempool data
    data_pool = xmrchainapi.getjson("mempool")
    # get last 30 txs data
    data_txs = xmrchainapi.getjson("transactions?limit=30")

    # parse networkinfo data
    height = data_info["data"]["height"]
    block_size_limit_kB = data_info["data"]["block_size_limit"] / 1024
    block_size_median_kB = data_info["data"]["block_size_median"] / 1024
    pooltxs = data_info["data"]["tx_pool_size"]
    lasthash = data_info["data"]["top_block_hash"]

    # parse mempool data
    n = 0
    num = 0
    poolsize = 0
    valid_txs = []
    invalid_txs = []
    valid_waits = []

    while n < data_pool["data"]["txs_no"]:
        timestamp = data_pool["data"]["txs"][num]["timestamp"]
        txs_size_kB = data_pool["data"]["txs"][num]["tx_size"] / 1024
        fee = data_pool["data"]["txs"][num]["tx_fee"] / float(1e12)
        ring_size = data_pool["data"]["txs"][num]["mixin"]

        tx_age = int(time.time() - timestamp)

        if ring_size >= 5:

            valid_txs.append(txs_size_kB)
            valid_waits.append([tx_age, fee, txs_size_kB])

        num = num + 1
        n = n + 1

    poolsize = sum(valid_txs)

    if len(valid_txs) == 0:
        med_small_tx_kB = 0
    elif len(valid_txs) == 1:
        med_small_tx_kB = valid_txs[0]
    else:
        med_small_tx_kB = statistics.median(valid_txs)

    # parse last 30 blocks data
    print("\n Last 30 blocks (Byte):")
    print(" ======================")
    n = 0
    num = 0
    block_sizes = []
    tph = 0
    while n < 30:
        block_size_kB = data_txs["data"]["blocks"][num]["size"] / 1024
        block_height = data_txs["data"]["blocks"][num]["height"]
        block_txs = len(data_txs["data"]["blocks"][num]["txs"])
        print(
            " Height %s: %.2f kB ( %d txs )"
            % (block_height, block_size_kB, block_txs)
        )

        block_sizes.append(block_size_kB)
        tph = block_txs + tph
        num = num + 1
        n = n + 1
    print(" ======================")

    med_30_size_kB = statistics.median(block_sizes)
    med_10_size_kB = statistics.median(block_sizes[:9])
    avg_30_size_kB = statistics.mean(block_sizes)

    # caculate and print information
    fee_lv = 0.012 * 4
    block_size_median_kB_exp = block_size_median_kB * (1 + fee_lv)
    block_mb_day = block_size_median_kB *1024 * 720 / 1048576
    block_usage = med_10_size_kB / (block_size_median_kB) * 100

    # wait block caculation
    wait_block_p = int(sum(valid_txs) / (block_size_median_kB_exp) + 1)

    # longest valid txs wait
    wait_block_longest = 1

    if len(valid_waits) != 0:
        longest_valid = " Longest valid txs wait: %s (fee: %.6f, size: %.2f kB)\n" % (
            time.strftime("%H:%M:%S", time.gmtime(valid_waits[-1][0])),
            valid_waits[-1][1],
            valid_waits[-1][2],
        )
        wait_block_longest = int(valid_waits[-1][0] / 120 + 1)
    else:
        longest_valid = " No small tx is waiting"

    # compensate with TPH (experimental method)
    wait_block_tph = int(len(valid_txs) / (tph / 60 * 2) + 1)

    wait_block = int((wait_block_p + wait_block_tph) / 2)
    wait_block_sd = int(
        statistics.pstdev([wait_block_p, wait_block_tph, wait_block_longest])
    )

    # wait block to wait time caculation
    wait_hr, wait_min = divmod((wait_block * 2), 60)

    print("\n")
    print(" Height: %d\n" % height)
    print(" Last block hash:\n %s\n" % lasthash)
    print(" Block size hard limit: %.2f kB\n" % (block_size_limit_kB))
    print(" Predicted blockchain size per day: %.2f mB\n" % block_mb_day)
    print(" Mempool txs: %d\n" % pooltxs)
    print(" Valid Mempool txs size: %.2f kB\n" % (poolsize))
    print(" Median valid tx: %.2f kB (%d txs)\n" % (med_small_tx_kB, len(valid_txs)))
    print(" Median size of 100 blocks: %.2f kB\n" % (block_size_median_kB))
    print(" Median size of last 30 blocks: %.2f kB\n" % (med_30_size_kB))
    print(" Median size of last 10 blocks: %.2f kB\n" % (med_10_size_kB))
    print(" Median usage of last 10 blocks: %.2f %%\n" % block_usage)
    print(" Approx. tx per hour (30 blocks): %d TPH\n" % tph)
    print(longest_valid)
    print(
        " Predicted block time: predict: %d, tph: %d, longest: %d\n"
        % (wait_block_p, wait_block_tph, wait_block_longest)
    )
    print(
        " Average wait time: %d +- %d blocks ( %d hr: %d min )\n"
        % (wait_block, wait_block_sd, wait_hr, wait_min)
    )

    # update thingspeak
    thingspeak_key = open("thingspeak_key.txt", "r")
    url_thingspeak = (
        "https://api.thingspeak.com/update?api_key=" + thingspeak_key.readline()
    )
    thingspeak_key.close()
    url_data = (
        "&field1=%.2f&field2=%.2f&field3=%.2f&field4=%.2f&field5=%d&field6=%d&field7=%d"
        % (
            (poolsize),
            (block_size_limit_kB),
            (avg_30_size_kB),
            block_usage,
            tph,
            (wait_block * 2),
            len(valid_txs),
        )
    )
    print("\n GET " + url_thingspeak[8:] + url_data)
    try:
        resp_thingspeak = requests.get(url=url_thingspeak + url_data, timeout=20)
    except requests.exceptions.RequestException as err:
        print(" ERROR: " + str(err))
    print(" HTTP:" + str(resp_thingspeak))
    print(" Entry:" + str(resp_thingspeak.text))

    last_check = time.time()
    update_time_stamp = str(datetime.now().isoformat(timespec="minutes"))
    print("\n %s update finished" % update_time_stamp)
    print("\n Wait for next update in %ds ..." % check_period)
    while True:
        time.sleep(10)
        if (time.time() - last_check) > check_period:
            break
