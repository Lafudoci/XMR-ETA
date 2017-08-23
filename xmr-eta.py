import json, requests

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
	small_tx_size=0
	txs=0
	big_txs=[]
	while n < data_pool['data']['txs_no']:
		txs_size = data_pool['data']['txs'][num]['tx_size']
		poolsize = txs_size + poolsize
		if txs_size < 20480:
			small_tx_size = txs_size + small_tx_size
		if txs_size >= 20480:
			big_txs.append ( data_pool['data']['txs'][num]['tx_size'] )
		num = num + 1
		n = n + 1
	avg_big_txs = sum(big_txs)/len(big_txs)
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

	bigs, rest = divmod(blimit/2, avg_big_txs)

	wait_block = int(small_tx_size / rest)

	if wait_block < 1:
		wait_block = 1

	wait_hr, wait_min = divmod((wait_block * 2), 60)


#	print(big_txs)
	print("\n")
	print(" Height: "+ str(height) + "\n")
	print(" Last block hash:\n "+ str(lasthash) + "\n")
	print(" Block size limit: "+ str(format(blimit/1024, '.2f')+ " kB\n"))
	print(" Mempool txs: "+ str(pooltxs) + "\n")
	print(" Mempool txs size: "+ str(format(poolsize/1024, '.2f')) + " kB\n")
	print(" Small txs size: "+ str(format(small_tx_size/1024, '.2f')) + " kB\n")
	print(" Avg. size of last 30 blocks: "+ str(format(avg_block_size/1024, '.2f')) + " kB\n")
	print(" Approx. tx speed per hour: "+ str(format(txs, '.0f')) + " TPH\n")

	print(' Average wait time: %d blocks ( %d hr: %d min )\n' % (wait_block, wait_hr, wait_min))
else:
	print(' ERROR: Data source is unavailabe.')

input(' Finished!') 
