import json, requests, time


def getjson(arg):

	# get network data
	url = ('http://xmrchain.net/api/%s' % (arg))
	print('\n Connecting to: '+ url[7:])

	while True: 
		try:
			resp = requests.get(url = url)
		except requests.exceptions.RequestException as err:
			print(' ERROR: '+ str(err))
			print(' Retry in 10s ...\n')
			time.sleep(10)
			continue

		print(' HTTP:'+ str(resp))

		
		if str(resp) == '<Response [200]>':
			jsontext = json.loads(resp.text)
		
			if jsontext['status'] == 'success':
				print(' JSON OK')
				break
			else:
				print(' ERROR:'+ jsontext['error'])
				print(' Retry in 10s ...\n')
				time.sleep(10)
				continue
		else:
			print(' Retry in 10s ...\n')
			time.sleep(10)
			continue

	return jsontext