import json, requests

from pprint import pprint

# get network data
url_info = 'http://xmrchain.net/api/networkinfo'
print("\n Connecting to: "+ url_info[7:])
resp_info = requests.get(url=url_info)
data_info = json.loads(resp_info.text)

if data_info['status'] == 'success':
	print(' OK')
	height = str(data_info['data']['height'])
	blimit = str(data_info['data']['block_size_limit'])
	pooltxs = str(data_info['data']['tx_pool_size'])
	lasthash = str(data_info['data']['top_block_hash'])
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
	txs=0
	while n < data_pool['data']['txs_no']:
		txs_size = data_pool['data']['txs'][num]['tx_size']
		poolsize = txs_size + poolsize
		num = num + 1
		n = n + 1
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
	block_sizes=0
	txs=0
	while n<30:
		block_size = data_txs['data']['blocks'][num]['size']
		block_height = data_txs['data']['blocks'][num]['height']
		block_txs = len(data_txs['data']['blocks'][num]['txs'])

		print(" Height "+ str(block_height) + ": " + str(block_size) + " ( " + str(block_txs) + " txs )")
		
		txs = block_txs + txs
		block_sizes = block_size + block_sizes
		num = num + 1
		n = n + 1
	print(" ======================")

	avg_size = format(block_sizes/25/1024, '.2f')
	tph = format(txs, '.0f')
else:
	print(' ERROR:'+ data_txs['error'])



# print information
if data_info['status'] and data_txs['status'] and data_pool['status'] == 'success':
	print("\n")
	print(" Height: "+ height + "\n")
	print(" Block size limit: "+ blimit + "\n")
	print(" Mempool txs: "+ pooltxs + "\n")
	print(" Mempool txs size: "+ str(format(poolsize/1024, '.2f')) + "kB\n")
	print(" Last block hash:\n "+ lasthash + "\n")
	print(" Avg. size of last 25 blocks: "+ str(avg_size) + " kB\n")
	print(" Approx. tx speed per hour: "+ str(tph) + " TPH\n")
else:
	print(' ERROR: Data source is unavailabe.')

input(' Finished!') 
