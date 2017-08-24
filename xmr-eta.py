import json, requests, statistics 

from pprint import pprint

# get network data
url_info = 'http://xmrchain.net/api/networkinfo'
print("\n Connecting to: "+ url_info[7:])
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
url_pool = 'https://xmrchain.net/api/mempool'
print("\n Connecting to: "+ url_pool[7:])
resp_pool = requests.get(url=url_pool)
data_pool = json.loads(resp_pool.text)

if data_pool['status'] == 'success':
	print(' OK')
	n=0
	num=0
	poolsize=0
	small_txs=[]
	big_txs=[]
	while n < data_pool['data']['txs_no']:
		txs_size = data_pool['data']['txs'][num]['tx_size']
		poolsize = txs_size + poolsize
		if txs_size < 40960:
			small_txs.append ( data_pool['data']['txs'][num]['tx_size'] )
		else:
			big_txs.append ( data_pool['data']['txs'][num]['tx_size'] )
		num = num + 1
		n = n + 1
	med_small_tx = statistics.median(small_txs)
	if len(big_txs) == 0:
		med_big_tx = 0
	else:
		med_big_tx = statistics.median(big_txs)
else:
	print(' ERROR:'+ data_pool['error'])


# get last 30 txs data
url_txs = 'https://xmrchain.net/api/transactions?limit=30'
print("\n Connecting to: "+ url_txs[7:])
resp_txs = requests.get(url=url_txs)
data_txs = json.loads(resp_txs.text)


if data_txs['status'] == 'success':
	print(' OK')
	print("\n Last 30 blocks (Byte):")
	print(" ======================")
	n=0
	num=0
	block_size_sum=0
	txs=0
	while n<30:
		block_size = data_txs['data']['blocks'][num]['size']
		block_height = data_txs['data']['blocks'][num]['height']
		block_txs = len(data_txs['data']['blocks'][num]['txs'])

		print(" Height "+ str(block_height) + ": " + str(block_size) + " ( " + str(block_txs) + " txs )")

		txs = block_txs + txs
		block_size_sum = block_size + block_size_sum
		num = num + 1
		n = n + 1
	print(" ======================")

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

	block_fill = format((avg_block_size/(blimit/2))*100, '.2f')

	if rest/med_small_tx > len(small_txs):
		smalls = len(small_txs)
	else:
		smalls = int(rest/med_small_tx)

	block_mb_day = avg_block_size * 720 / 1048576


#	print(big_txs)
	print("\n")
	print(" Height: "+ str(height) + "\n")
	print(" Last block hash:\n "+ str(lasthash) + "\n")
	print(" Block size limit: %s kB\n" % (str(format(blimit/1024, '.2f') )))
	print(" Predicted blockchain size per day: %s mB\n" % (str(format(block_mb_day, '.2f') )))
	print(" Mempool txs: "+ str(pooltxs) + "\n")
	print(" Mempool txs size: "+ str(format(poolsize/1024, '.2f')) + " kB\n")
	print(" Med. Small tx: %.2f kB (%d txs)\n" % (med_small_tx/1024, len(small_txs)))
	print(" Med. big tx: %2f kB (%d txs)\n" % (med_big_tx/1024, len(big_txs)))
	print(" Half block block limit: %s kB\n" % (str(format(blimit/1024/2, '.2f') )))
	print(" Avg. of last 30 blocks: "+ str(format(avg_block_size/1024, '.2f')) + " kB\n")
	print(' Block usage: ' + str(block_fill) + '%\n')
	print(" Approx. tx speed per hour: "+ str(format(txs, '.0f')) + " TPH\n")

	print(' Predicted block: %d big_txs + %d small_txs\n' % (int(bigs), int(smalls)))
	print(' Average wait time: %d blocks ( %d hr: %d min )\n' % (wait_block, wait_hr, wait_min))
else:
	print(' ERROR: Data source is unavailabe.')

input(' Finished!') 
