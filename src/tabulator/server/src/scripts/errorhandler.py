def errorhandler(errorString):
	f = open("tab.txt", "w+")
	f.write(errorString)
	f.close()