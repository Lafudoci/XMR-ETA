import requests, getjson, statistics, math, time
from pprint import pprint
from operator import itemgetter, attrgetter  

check_period = 240

while True:
# get last networkinfo data
	data_info = getjson.xmrchain('networkinfo')
# get last mempool data
	data_pool = getjson.xmrchain('mempool')
# get last 30 txs data
	data_txs = getjson.xmrchain('transactions?limit=30')
# get emission data
	data_emission = getjson.moneroblocks('get_stats')


# parse networkinfo data
	height = data_info['data']['height']
	dyn_size = data_info['data']['block_size_limit']/2
	pooltxs = data_info['data']['tx_pool_size']
	lasthash = data_info['data']['top_block_hash']

# parse mempool data
	n=0
	num=0
	poolsize=0
	small_txs=[]
	big_txs=[]
	waits=[]
	small_waits=[]
	big_waits=[]
	while n < data_pool['data']['txs_no']:
		timestamp = data_pool['data']['txs'][num]['timestamp']
		txs_size = data_pool['data']['txs'][num]['tx_size']
		fee = data_pool['data']['txs'][num]['tx_fee']/float(1e12)

		tx_age = int(time.time() - timestamp)

		waits.append( (tx_age, fee, txs_size, fee/txs_size))
		
		poolsize = poolsize + txs_size

		num = num + 1
		n = n + 1

	poolsize = sum(small_txs) + sum(big_txs)


# parse last 30 blocks data
	# print('\n Last 30 blocks (Byte):')
	# print(' ======================')
	n=0
	num=0
	block_sizes=[]
	tph=0
	while n<30:
		block_size = data_txs['data']['blocks'][num]['size']
		block_height = data_txs['data']['blocks'][num]['height']
		block_txs = len(data_txs['data']['blocks'][num]['txs'])
		#print(' Height %s: %.2f kB ( %d txs )' % (block_height, block_size/1024, block_txs))

		block_sizes.append(block_size)
		tph = block_txs + tph
		num = num + 1
		n = n + 1
	# print(' ======================')

	med_30_size = statistics.median(block_sizes)
	avg_30_size = statistics.mean(block_sizes)


# caculate and print information

# base reward caculation
	M = 2**64 - 1
	A = int(data_emission['total_emission'])
	base_reward = max( 0.6, math.floor( (M - A) / 2**19 )) / 10**12

# dynamic size expasion base on fee
	# fee_lv = 0.012 * 4
	# dyn_size_exp = dyn_size * (1 + fee_lv)
	# block_mb_day = dyn_size * 720 / 1048576
	# block_usage = avg_30_size/(dyn_size)*100

# sort mempool txs by fee / size
	waits.sort(key=itemgetter(3,0), reverse=True)
	print('\n Waits in mempool:')
	pprint (waits)

	block_fee = 0
	fill=0
	n=0
	num=0
	post_fill=[]
	first_fill=[]
	block_finish = True
	while n < len(waits):

		if fill + waits[num][2] <= dyn_size:
			block_fee = block_fee + waits[num][1]
			fill = fill + waits[num][2]
			first_fill.append((fill, block_fee))
		else:
			block_finish = False	
			
			fill_exp = (fill + waits[num][2])
	
			penalty = ( fill_exp / dyn_size - 1)**2

			post_fill.append((waits[num][1], waits[num][2], waits[num][1] - penalty))

		num = num + 1
		n = n + 1

	print('\n First fill:')
	pprint (first_fill)



	if block_finish == False:
		

		post_fill.sort(key=itemgetter(2), reverse=True)
		print('\n post fill:')
		pprint(post_fill)
		

		fee_add = 0
		fill_add = 0
		penalty_add = 0
		fill_gain = []
		n=0
		num=0
		while n < len(post_fill):

			fee_add = fee_add + post_fill[num][0]
			fill_add = fill_add + post_fill[num][1]
			penalty_add = ( (fill + fill_add) / dyn_size - 1)**2

			fill_gain.append(((fill+fill_add), (fee_add - penalty_add)))
			num = num + 1
			n = n + 1

		print('\n Fill & Gain:')
		pprint (fill_gain)

		fill_gain.sort(key=itemgetter(1), reverse=True)

		print('\n Fill & Gain sorted:')
		pprint (fill_gain)

		if fill_gain[0][1] < 0:
			print( 'There are nothing worth adding')
		else:
			fianal_add =[]
			fianal_add = fill_gain[0]

			print('\n Final adds:')
			pprint (fianal_add)

			fill = fianal_add[0]
			block_fee = block_fee + fianal_add[1]


	else:
		print('\n Block is not full yet!')
			
	
# wait block caculation
	# bigs = 0
	# rest = 0
	# smalls = 0
# predict big txs in this block
# 	if len(big_txs) == 0:
# 		bigs = 0
# 		rest = sum(small_txs)
# 		wait_block_p = int( rest / (dyn_size_exp) + 1)
	
# 	elif len(big_txs) == 1:
# 		bigs = 1
# 		rest = (dyn_size_exp) - med_big_tx
# 		wait_block_p = int( sum(small_txs) / rest + 1)
	
# 	else:
# 		bigs, rest = divmod((dyn_size_exp), med_big_tx)
# 		if bigs > len(big_txs):
# 			rest = rest + (bigs-len(big_txs))*med_big_tx
# 			bigs = len(big_txs)
# 		wait_block_p = int( sum(small_txs) / rest + 1)

# # predict small txs in this block
# 	if len(small_txs) == 0:
# 		smalls = 0
# 	elif rest/med_small_tx > len(small_txs):
# 		smalls = len(small_txs)
# 	else:
# 		smalls = int(rest/med_small_tx)

# # predict the block size
# 	this_block = bigs*med_big_tx + smalls*med_small_tx
# 	this_block_load = this_block/dyn_size*100
	
# # longest small txs wait
# 	if len(small_waits) != 0:
# 		longest_small = ' Longest small wait: %s (fee: %.4f, size: %.2f kB)\n' % (time.strftime("%H:%M:%S",time.gmtime(small_waits[-1][0])), small_waits[-1][1], small_waits[-1][2]/1024)
# # compensate with longest wait (experimental method)
# 		wait_block_longest = int(small_waits[-1][0]/120 +1)
# 	else:
# 		longest_small = ' No small tx is waiting'

# # compensate with TPH (experimental method)
# 	wait_block_tph = int( len(small_txs)/(tph/60*2) +1)

# 	wait_block = int(( wait_block_p + wait_block_tph)/2)
# 	wait_block_sd = int(statistics.pstdev ([wait_block_p , wait_block_tph , wait_block_longest]))

# wait block to wait time caculation
	#wait_hr, wait_min = divmod((wait_block * 2), 60)


	print('\n')
	print(' Height: %d\n' % height )
	# print(' Last block hash:\n %s\n' % lasthash)
	# print(' Base block reward: %.2f XMR\n' % base_reward)
	# print(' Block size hard limit: %.2f kB\n' % (dyn_size*2/1024) )
	# print(' Predicted blockchain size per day: %.2f mB\n' % block_mb_day )
	print(' Mempool txs: %d\n' % pooltxs)
	# print(' Mempool txs size: %.2f kB\n' % (poolsize/1024) )
	# print(' Med. Small tx: %.2f kB (%d txs)\n' % (med_small_tx/1024, len(small_txs)))
	# print(' Med. big tx: %.2f kB (%d txs)\n' % (med_big_tx/1024, len(big_txs)))
	print(' Dynamic block size: %.2f kB\n' % (dyn_size/1024) )
	# print(' Avg. of last 30 blocks: %.2f kB\n' % (avg_30_size/1024) )
	# print(' Block load: %.2f %%\n' % block_usage )
	# print(' Approx. tx speed per hour: %d TPH\n' % tph)
	# print( longest_small )
	# print(' Predicted block txs: %d big (%.fk) + %d small (%.fk) ( %.0f%% )\n' % (int(bigs), bigs*med_big_tx/1024, int(smalls), smalls*med_small_tx/1024, this_block_load))
	# print(' Predicted block time: predict: %d, tph: %d, longest: %d\n' % (wait_block_p, wait_block_tph, wait_block_longest))
	# print(' Average wait time: %d +- %d blocks ( %d hr: %d min )\n' % (wait_block, wait_block_sd, wait_hr, wait_min))

	print('\n Height %d prediction:\n' % height )
	print (' Method2: %.2f kb, fee: %.4f xmr, load: %.2f%%\n' % (fill/1024, block_fee, fill/dyn_size*100))

# update thingspeak
	# thingspeak_key = open('thingspeak_key.txt', 'r')
	# url_thingspeak = 'https://api.thingspeak.com/update?api_key='+ thingspeak_key.readline()
	# thingspeak_key.close()
	# url_data = '&field1=%.2f&field2=%.2f&field3=%.2f&field4=%.2f&field5=%d&field6=%d&field7=%d&field8=%d' % ((poolsize/1024), (dyn_size/1024), (avg_30_size/1024), block_usage, tph, (wait_block*2), len(small_txs), len(big_txs))
	# print('\n GET '+ url_thingspeak[8:] + url_data)
	# try:
	# 	resp_thingspeak = requests.get(url=url_thingspeak+url_data)
	# except requests.exceptions.RequestException as err:
	# 	print(' ERROR: '+ str(err))
	
	# print('\n HTTP:'+ str(resp_thingspeak))
	# print(' Entry:'+ str(resp_thingspeak.text))
		
# update loop timer
	last_check = time.time()
	print('\n Wait for next update in %ds ...'% check_period)
	while True:
		time.sleep(1)
		if (time.time()-last_check) > check_period:
			break
