import requests, statistics, math, time

from pprint import pprint

import xmrchainapi

check_period = 240

while True:
# get last networkinfo data
	data_info = xmrchainapi.getjson('networkinfo')
# get last mempool data
	data_pool = xmrchainapi.getjson('mempool')
# get last 30 txs data
	data_txs = xmrchainapi.getjson('transactions?limit=30')


# parse networkinfo data
	height = data_info['data']['height']
	dyn_size = data_info['data']['block_size_limit']/1000*1024/2
	pooltxs = data_info['data']['tx_pool_size']
	lasthash = data_info['data']['top_block_hash']

# parse mempool data
	n=0
	num=0
	poolsize=0
	small_txs=[]
	big_txs=[]
	small_waits = []
	big_fees = []
	while n < data_pool['data']['txs_no']:
		timestamp = data_pool['data']['txs'][num]['timestamp']
		txs_size = data_pool['data']['txs'][num]['tx_size']
		fee = data_pool['data']['txs'][num]['tx_fee']/float(1e12)

		tx_age = int(time.time() - timestamp)

		if txs_size < 40960:
			small_txs.append( txs_size )
			small_waits.append( [tx_age, fee, txs_size])
		else:
			big_txs.append( txs_size )
			big_fees.append( [tx_age, fee, txs_size])
		
		num = num + 1
		n = n + 1

	poolsize = sum(small_txs) + sum(big_txs)

	if len(small_txs) == 0:
		med_small_tx = 0
	elif len(small_txs) == 1:
		med_small_tx = small_txs[0]
	else:
		med_small_tx = statistics.median(small_txs)

	if len(big_txs) == 0:
		med_big_tx = 0
	elif len(big_txs) == 1:
		med_big_tx = big_txs[0]
	else:
		med_big_tx = statistics.median(big_txs)

# parse last 30 blocks data
	print('\n Last 30 blocks (Byte):')
	print(' ======================')
	n=0
	num=0
	block_sizes=[]
	tph=0
	while n<30:
		block_size = data_txs['data']['blocks'][num]['size']
		block_height = data_txs['data']['blocks'][num]['height']
		block_txs = len(data_txs['data']['blocks'][num]['txs'])
		print(' Height %s: %.2f kB ( %d txs )' % (block_height, block_size/1024, block_txs))

		block_sizes.append(block_size)
		tph = block_txs + tph
		num = num + 1
		n = n + 1
	print(' ======================')

	med_30_size = statistics.median(block_sizes)
	avg_30_size = statistics.mean(block_sizes)


# caculate and print information

	fee_lv = 0.012 * 4
	dyn_size_exp = dyn_size * (1 + fee_lv)
	block_mb_day = dyn_size * 720 / 1048576
	block_usage = avg_30_size/(dyn_size)*100
	
# wait block caculation
	bigs = 0
	rest = 0
	smalls = 0
# predict big txs in this block
	if len(big_txs) == 0:
		bigs = 0
		rest = sum(small_txs)
		wait_block_p = int( rest / (dyn_size_exp) + 1)
	
	elif len(big_txs) == 1:
		bigs = 1
		rest = (dyn_size_exp) - med_big_tx
		wait_block_p = int( sum(small_txs) / rest + 1)
	
	else:
		bigs, rest = divmod((dyn_size_exp), med_big_tx)
		if bigs > len(big_txs):
			rest = rest + (bigs-len(big_txs))*med_big_tx
			bigs = len(big_txs)
		wait_block_p = int( sum(small_txs) / rest + 1)

# predict small txs in this block
	if len(small_txs) == 0:
		smalls = 0
	elif rest/med_small_tx > len(small_txs):
		smalls = len(small_txs)
	else:
		smalls = int(rest/med_small_tx)

# predict the block size
	this_block = bigs*med_big_tx + smalls*med_small_tx
	this_block_efficiency = this_block/dyn_size*100
	
# longest small txs wait
	if len(small_waits) != 0:
		longest_small = ' Longest small wait: %s (fee: %.4f, size: %.2f kB)\n' % (time.strftime("%H:%M:%S",time.gmtime(small_waits[-1][0])), small_waits[-1][1], small_waits[-1][2]/1024)
# compensate with longest wait (experimental method)
		wait_block_longest = int(small_waits[-1][0]/120 +1)
	else:
		longest_small = ' No small tx is waiting'

# compensate with TPH (experimental method)
	wait_block_tph = int( len(small_txs)/(tph/60*2) +1)

	wait_block = int(( wait_block_p + wait_block_tph)/2)
	wait_block_sd = int(statistics.pstdev ([wait_block_p , wait_block_tph , wait_block_longest]))

# wait block to wait time caculation
	wait_hr, wait_min = divmod((wait_block * 2), 60)


	print('\n')
	print(' Height: %d\n' % height )
	print(' Last block hash:\n %s\n' % lasthash)
	print(' Block size hard limit: %.2f kB\n' % (dyn_size*2/1000) )
	print(' Predicted blockchain size per day: %.2f mB\n' % block_mb_day )
	print(' Mempool txs: %d\n' % pooltxs)
	print(' Mempool txs size: %.2f kB\n' % (poolsize/1024) )
	print(' Med. Small tx: %.2f kB (%d txs)\n' % (med_small_tx/1024, len(small_txs)))
	print(' Med. big tx: %.2f kB (%d txs)\n' % (med_big_tx/1024, len(big_txs)))
	print(' Dynamic block size: %.2f kB\n' % (dyn_size/1024) )
	print(' Avg. of last 30 blocks: %.2f kB\n' % (avg_30_size/1024) )
	print(' Block usage: %.2f %%\n' % block_usage )
	print(' Approx. tx speed per hour: %d TPH\n' % tph)
	print( longest_small )
	print(' Predicted block txs: %d big (%.fk) + %d small (%.fk) ( %.0f%% )\n' % (int(bigs), bigs*med_big_tx/1024, int(smalls), smalls*med_small_tx/1024, this_block_efficiency))
	print(' Predicted block time: predict: %d, tph: %d, longest: %d\n' % (wait_block_p, wait_block_tph, wait_block_longest))
	print(' Average wait time: %d +- %d blocks ( %d hr: %d min )\n' % (wait_block, wait_block_sd, wait_hr, wait_min))

	
# update thingspeak
	thingspeak_key = open('thingspeak_key.txt', 'r')
	url_thingspeak = 'https://api.thingspeak.com/update?api_key='+ thingspeak_key.readline()
	thingspeak_key.close()
	url_data = '&field1=%.2f&field2=%.2f&field3=%.2f&field4=%.2f&field5=%d&field6=%d&field7=%d&field8=%d' % ((poolsize/1024), (dyn_size*2/1024), (avg_30_size/1024), block_usage, tph, (wait_block*2), len(small_txs), len(big_txs))
	print('\n GET '+ url_thingspeak[8:] + url_data)
	try:
		resp_thingspeak = requests.get(url=url_thingspeak+url_data)
	except requests.exceptions.RequestException as err:
		print(' ERROR: '+ str(err))
	
	print(' HTTP:'+ str(resp_thingspeak))
	print(' Entry:'+ str(resp_thingspeak.text))
		

	last_check = time.time()
	
	print('\n Wait for next update in %ds ...'% check_period)
	while True:
		time.sleep(1)
		if (time.time()-last_check) > check_period:
			break
