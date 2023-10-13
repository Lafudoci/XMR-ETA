import json, requests, time


def getjson(arg):

	# get network data
	url = ('https://moneroexplorer.org/api/%s' % (arg))
	print('\n Connecting to: '+ url[7:])

	while True: 
		try:
			resp = requests.get(url = url, timeout = 20)
		except requests.exceptions.RequestException as err:
			print(' ERROR: '+ str(err))
			print(' Retry in 10s ...\n')
			time.sleep(10)
			continue

		print(' HTTP:'+ str(resp))

		
		if str(resp) == '<Response [200]>':
			try:
				jsontext = json.loads(resp.text)
			except ValueError:
				print ('Decoding JSON has failed')
				continue
		
			if jsontext['status'] == 'success':
				print(' JSON OK')
				break
			else:
				print(' ERROR:'+ jsontext['status'])
				print(' Retry in 10s ...\n')
				time.sleep(10)
				continue
		else:
			print(' Retry in 10s ...\n')
			time.sleep(10)
			continue

	return jsontext

if __name__ == '__main__':
	print(getjson('networkinfo'))
