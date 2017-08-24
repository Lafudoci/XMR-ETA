import json, requests, statistics, math, time

from pprint import pprint


while True:

	# get network data
	url_info = 'http://xmrchain.net/api/networkinfo'
	print('\n Connecting to: '+ url_info[7:])
	resp_info = requests.get(url=url_info)
	data_info = json.loads(resp_info.text)

	if data_info['status'] == 'success':
		print(' OK')
		height = data_info['data']['height']
		blimit = data_info['data']['block_size_limit']
		pooltxs = data_info['data']['tx_pool_size']
		lasthash = data_info['data']['top_block_hash']
	else:
		print(' ERROR:'+ data_info['error'])


	# get last mempool data
	url_pool = 'http://xmrchain.net/api/mempool'
	print('\n Connecting to: '+ url_pool[7:])
	resp_pool = requests.get(url=url_pool)
	data_pool = json.loads(resp_pool.text)

	if data_pool['status'] == 'success':
		print(' OK')
		n=0
		num=0
		poolsize=0
		small_txs=[]
		big_txs=[]
		small_fees = []
		big_fees = []
		while n < data_pool['data']['txs_no']:
			timestamp = data_pool['data']['txs'][num]['timestamp']
			txs_size = data_pool['data']['txs'][num]['tx_size']
			fee = data_pool['data']['txs'][num]['tx_fee']/float(1e12)

			age = time.strftime("%H:%M:%S", time.gmtime(int(time.time()) - timestamp))

			if txs_size < 40960:
				small_txs.append( txs_size )
				small_fees.append( [age, fee, txs_size])
			else:
				big_txs.append( txs_size )
				big_fees.append( [age, fee, txs_size])
			
			num = num + 1
			n = n + 1

		poolsize = sum(small_txs) + sum(big_txs)

		med_small_tx = statistics.median(small_txs)

		if len(big_txs) == 0:
			med_big_tx = 0
		else:
			med_big_tx = statistics.median(big_txs)



	else:
		print(' ERROR:'+ data_pool['error'])


	# get last 30 txs data
	url_txs = 'http://xmrchain.net/api/transactions?limit=30'
	print('\n Connecting to: '+ url_txs[7:])
	resp_txs = requests.get(url=url_txs)
	data_txs = json.loads(resp_txs.text)


	if data_txs['status'] == 'success':
		print(' OK')
		print('\n Last 30 blocks (Byte):')
		print(' ======================')
		n=0
		num=0
		block_size_sum=0
		txs=0
		while n<30:
			block_size = data_txs['data']['blocks'][num]['size']
			block_height = data_txs['data']['blocks'][num]['height']
			block_txs = len(data_txs['data']['blocks'][num]['txs'])

			print(' Height %s: %.2f kB ( %d txs )' % (block_height, block_size/1024, block_txs))

			txs = block_txs + txs
			block_size_sum = block_size + block_size_sum
			num = num + 1
			n = n + 1
		print(' ======================')

		avg_block_size = block_size_sum / 30

	else:
		print(' ERROR:'+ data_txs['error'])


	# caculate and print information
	if data_info['status'] and data_txs['status'] and data_pool['status'] == 'success':
	# wait time caculation
	#	wait_block = int(poolsize / avg_block_size)
		bigs = 0
		rest = 0
		smalls = 0
		if med_big_tx == 0:
			rest = sum(small_txs)
			wait_block = int( rest / (blimit/2) + 1)
		
		elif len(big_txs) == 1:
			rest = blimit/2 - med_big_tx
			wait_block = int( sum(small_txs) / rest + 1)
		
		else:
			bigs, rest = divmod(blimit/2, med_big_tx)
			wait_block = int( sum(small_txs) / rest + 1)

		wait_hr, wait_min = divmod((wait_block * 2), 60)

		block_fill = avg_block_size/(blimit/2)*100

		if rest/med_small_tx > len(small_txs):
			smalls = len(small_txs)
		else:
			smalls = int(rest/med_small_tx)

		block_mb_day = avg_block_size * 720 / 1048576

	#	pprint(small_fees)
		print('\n')
		print(' Height: %d\n' % height )
		print(' Last block hash:\n %s' % lasthash)
		print(' Block size limit: %.2f kB\n' % (blimit/1024) )
		print(' Predicted blockchain size per day: %.2f mB\n' % block_mb_day )
		print(' Mempool txs: %d\n' % pooltxs)
		print(' Mempool txs size: %.2f kB\n' % (poolsize/1024) )
		print(' Med. Small tx: %.2f kB (%d txs)\n' % (med_small_tx/1024, len(small_txs)))
		print(' Med. big tx: %.2f kB (%d txs)\n' % (med_big_tx/1024, len(big_txs)))
		print(' Half block block limit: %.2f kB\n' % (blimit/1024/2) )
		print(' Avg. of last 30 blocks: %.2f kB\n' % (avg_block_size/1024) )
		print(' Block usage: %.2f %%\n' % block_fill )
		print(' Approx. tx speed per hour: %d TPH\n' % txs)

		print(' Predicted block: %d big_txs + %d small_txs\n' % (int(bigs), int(smalls)))
		print(' Average wait time: %d blocks ( %d hr: %d min )\n' % (wait_block, wait_hr, wait_min))
		print(' Longest wait: %s (fee: %.4f, size: %.2f kB)\n' % (small_fees[-1][0], small_fees[-1][1], small_fees[-1][2]/1024))
		
		# update thingspeak
		thingspeak_key = open('thingspeak_key.txt', 'r')
		url_thingspeak = 'https://api.thingspeak.com/update?api_key='+ thingspeak_key.readline()
		thingspeak_key.close()
		url_data = '&field1=%.2f&field2=%.2f&field3=%.2ff&field4=%.2f&field5=%d&field6=%d' % ((poolsize/1024), (blimit/1024), avg_block_size, block_fill, txs, (wait_block*2))
		print('\n GET '+ url_thingspeak[8:] + url_data)
		resp_thingspeak = requests.get(url=url_thingspeak+url_data)
		print(resp_thingspeak)
		print(resp_thingspeak.text)


	else:
		print(' ERROR: Data source is unavailabe.')

	time.sleep(600)

input(' Finished!') 
