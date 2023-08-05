import subprocess
import json
import sys
import simplim
import re
import os

module_path = os.path.join(os.path.dirname(__file__), '')

temp_path = os.path.join(module_path, 'temp')

class App():
	def __init__(self, appn, hous, mins, secs, pcnt):
		self.appn = appn
		self.hous = hous
		self.mins = mins
		self.secs = secs
		self.pcnt = pcnt
		self.allT = hous * 3600 + mins * 60 + secs


def call(cmd):
	apps = []
	subp = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
	time = subp.stdout.readline().decode()
	line = subp.stdout.readline().decode()
	line = subp.stdout.readline().decode()
	while line:
		print(line)
		# cuts = re.search('    ', line[10:])
		# appn = line[re.search('\S',line[:10 + cuts.start()]).start():10 + cuts.start()]
		nsta = re.search('\S',line).start()
		nend = nsta + re.search('\ ?\ ?\ ?\ ?\ ?\ ?\ ?\ ?\ ?\d?\d?h? ?\d?\d?m? ?\d\ds', line[nsta:]).start()
		
		appn = line[nsta:nend]
		info = line[nend:]

		secs = int(re.search('\d\ds', info)[0][:-1])
		mins = re.search('\d\dm', info)
		if mins:
			mins = int(mins[0][:-1])
		else:
			mins = 0
		hous = re.search('\d?\dh', info)
		if hous:
			hous = int(hous[0][:-1])
		else:
			hous = 0
		pcnt = re.search('(\d)(\d)?\.\d%', info)[0]

		apps.append(App(appn, hous, mins, secs, pcnt))
		line = subp.stdout.readline().decode()
	return apps

def out(cmd, clean=1):
	temp = os.path.join(temp_path, simplim.gettemp() + '.json')
	os.system(cmd + ' -O ' + temp)
	list_ = json.load(open(temp))
	list_out = []
	for dict_ in list_:
		list_out.append(simplim.easyclassify(dict_))
	if clean:
		cleantemp()
	return list_out

def cleantemp():
	os.system('sudo rm -r ' + temp_path)
	os.system('mkdir ' + temp_path)

