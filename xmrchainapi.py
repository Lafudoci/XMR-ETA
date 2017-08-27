import json, requests


def getjson(arg):

	# get network data
	url = ('http://xmrchain.net/api/%s' % (arg))
	print('\n Connecting to: '+ url[7:])

	while True: 
		try:
			resp = requests.get(url = url)
		except requests.exceptions.RequestException as err:
			print('error: '+ err)
			print('Retry in 20s ...')
			time.sleep(20)
			contunue
		break
	print(' HTTP:'+ str(resp))

	return json.loads(resp.text)