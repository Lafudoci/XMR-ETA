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
#	data_txs = getjson.xmrchain('transactions?limit=30')
# get emission data
	data_emission = getjson.moneroblocks('get_stats')


# parse networkinfo data
	height = data_info['data']['height']
	dyn_size = data_info['data']['block_size_limit']/1000*1024/2
	pooltxs = data_info['data']['tx_pool_size']
	lasthash = data_info['data']['top_block_hash']

# parse mempool data
	n=0
	num=0
	poolsize=0
	waits=[]

	block_predict = open(str(height)+str('-%s'% time.strftime("%H%M%S",time.gmtime(time.time())))+'.txt', 'w')
	#block_predict.write('Time: %s\n'% time.strftime("%H%M%S",time.gmtime(time.time())))
	block_predict.write('mempool:\n')

	while n < data_pool['data']['txs_no']:
		timestamp = data_pool['data']['txs'][num]['timestamp']
		txs_size = data_pool['data']['txs'][num]['tx_size']
		fee = data_pool['data']['txs'][num]['tx_fee']/float(1e12)
		tx_hash = data_pool['data']['txs'][num]['tx_hash']

		tx_age = int(time.time() - timestamp)

		waits.append( (tx_age, fee, txs_size, fee/txs_size, tx_hash))
		

		block_predict.write(str((tx_age, fee, txs_size, fee/txs_size, tx_hash))+'\n')
		


		poolsize = poolsize + txs_size

		num = num + 1
		n = n + 1


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
	block_predict.write('\nFirst fill:\n')
	while n < len(waits):

# fill the block by fee/size order calls "first fill" list and sum size and fee
		if fill + waits[num][2] <= dyn_size:
			block_fee = block_fee + waits[num][1]
			fill = fill + waits[num][2]
			first_fill.append((fill, block_fee, waits[num][4]))

			block_predict.write(str((fill, block_fee, waits[num][4]))+'\n')

# if fill meets the dynamic size then build a "post-fill" list
		else:
			block_finish = False	
			
			fill_exp = (fill + waits[num][2])
	
			penalty = ( fill_exp / dyn_size - 1)**2

			

			post_fill.append((waits[num][1], waits[num][2], waits[num][1] - penalty, waits[num][4]))

		num = num + 1
		n = n + 1

	print('\n First fill:')
	pprint (first_fill)



	if block_finish == False:
		
# sort post-fill list order in ( fee-penalty )
		post_fill.sort(key=itemgetter(2), reverse=True)
		print('\n post fill:')
		pprint(post_fill)
		

		fee_add = 0
		fill_add = 0
		penalty_add = 0
		fill_gain = []
		n=0
		num=0
		block_predict.write('\nfill_gain:\n')
		while n < len(post_fill):

# caculate the progression size and penalty list calls "Fill & Gain"
			fee_add = fee_add + post_fill[num][0]
			fill_add = fill_add + post_fill[num][1]
			penalty_add = ( (fill + fill_add) / dyn_size - 1)**2

			fill_gain.append(((fill+fill_add), (fee_add - penalty_add), post_fill[num][3]))

			
			block_predict.write(str(((fill+fill_add), (fee_add - penalty_add), post_fill[num][3]))+'\n')
			num = num + 1
			n = n + 1

		print('\n Fill & Gain:')
		pprint (fill_gain)

# sort the Fill & Gain list and find the best solution
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

# use best solution's size as final block size
# add best solution's fee to first fill's fee
			fill = fianal_add[0]
			block_fee = block_fee + fianal_add[1]


	else:
		print('\n Block is not full yet!')
			


# wait block to wait time caculation
	#wait_hr, wait_min = divmod((wait_block * 2), 60)


	print('\n')
	print(' Height: %d\n' % height )

	print(' Mempool txs: %d\n' % pooltxs)

	print(' Dynamic block size: %.2f kB\n' % (dyn_size/1024) )

	print(' Time: %.f' % time.time())
	print(' Time: %s'% time.strftime("%H:%M:%S",time.gmtime(time.time())))
	print('\n Height %d prediction:\n' % height )
	print (' Size %.2f kb, fee: %.4f xmr, load: %.2f%%\n' % (fill/1024, block_fee, fill/dyn_size*100))

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
	

	block_predict.write('\nSize: %.2f kb, fee: %.4f xmr, load: %.2f%%\n' % (fill/1024, block_fee, fill/dyn_size*100)+'\n')
	block_predict.close()

# update loop timer
	last_check = time.time()
	print('\n Wait for next update in %ds ...'% check_period)
	while True:
		time.sleep(1)
		if (time.time()-last_check) > check_period:
			break
