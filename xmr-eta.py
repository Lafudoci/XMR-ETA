import json, requests

from pprint import pprint


url_info = 'http://xmrchain.net/api/networkinfo'
print("\n Connecting to: "+ url_info[7:])
resp_info = requests.get(url=url_info)
data_info = json.loads(resp_info.text)

if data_info['status'] == 'success':
	print(' OK')
	height = str(data_info['data']['height'])
	blimit = str(data_info['data']['block_size_limit'])
	poolsize = str(data_info['data']['tx_pool_size'])
	lasthash = str(data_info['data']['top_block_hash'])
else:
	print(' ERROR:'+ data_info['error'])


url_txs = 'http://xmrchain.net/api/transactions'
print("\n Connecting to: "+ url_txs[7:])
resp_txs = requests.get(url=url_txs)
data_txs = json.loads(resp_txs.text)


if data_txs['status'] == 'success':
	print(' OK')
	print("\n Last 25 blocks (Byte):")
	print(" ======================")
	n=0
	num=0
	sizes=0
	txs=0
	while n<25:
		block_size = data_txs['data']['blocks'][num]['size']
		block_height = data_txs['data']['blocks'][num]['height']
		block_txs = len(data_txs['data']['blocks'][num]['txs'])

		print(" Height "+ str(block_height) + ": " + str(block_size) + " ( " + str(block_txs) + " txs )")
		
		txs = block_txs + txs
		sizes = block_size + sizes
		num = num + 1
		n = n + 1
	print(" ======================")

	avg_size = format(sizes/25/1024, '.2f')
	tph = format(txs/50*60, '.0f')

	print("\n")
	print(" Height: "+ height + "\n")
	print(" Block size limit: "+ blimit + "\n")
	print(" Mempool size: "+ poolsize + "\n")
	print(" Last block hash:\n "+ lasthash + "\n")
	print(" Avg. size of last 25 blocks: "+ str(avg_size) + " kB\n")
	print(" Approx. tx speed per hour: "+ str(tph) + " TPH\n")
else:
	print(' ERROR:'+ data_txs['error'])


input(' Finished!') 
