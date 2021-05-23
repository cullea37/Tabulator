def auth():
	import requests
	from __main__ import app
	path = app.root_path
	authurl = "https://api.doremir.com/v1/token/create-token"
	authheader = {'User-Agent': 'curl/7.64.1', 'cache-control': 'no-cache', 'content-type': 'application/json'}
	authpayload = {"clientId":     "5f8da9f5f21c8a668ae25f95", "clientSecret": "6b6aa5d7-2fd3-4414-b80f-17090b6fb2c6"}

	resauth = requests.post(authurl, headers = authheader, json = authpayload)

	authresult = resauth.text
	print (authresult)
	print ("authresult\n\n")
	f = open(path+"/scripts/auth.text", "w")
	f.write(authresult)