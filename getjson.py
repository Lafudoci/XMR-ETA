import json, requests, time


def xmrchain(arg):

	# get network data
	url = ('http://xmrchain.net/api/%s' % (arg))
	print('\n Connecting to: '+ url[8:])

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
				print(' ERROR:'+ jsontext['error'])
				print(' Retry in 10s ...\n')
				time.sleep(10)
				continue
		else:
			print(' Retry in 10s ...\n')
			time.sleep(10)
			continue

	return jsontext


def moneroblocks(arg):

	# get network data
	url = ('http://moneroblocks.info/api/%s' % (arg))
	print('\n Connecting to: '+ url[8:])

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
			break
			# if jsontext['status'] == 'success':
			# 	print(' JSON OK')
			# 	break
			# else:
			# 	print(' ERROR:'+ jsontext['error'])
			# 	print(' Retry in 10s ...\n')
			# 	time.sleep(10)
			# 	continue
		else:
			print(' Retry in 10s ...\n')
			time.sleep(10)
			continue

	return jsontext