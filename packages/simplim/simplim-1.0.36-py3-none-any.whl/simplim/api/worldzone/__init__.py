import os, re, time
from simplim.premium import simdict
timezone_path = os.path.join(os.path.dirname(__file__),'all.json')
timezone = simdict(timezone_path)

time_string='2020/10/11|20:30:12'

class PatternError(Exception):
	def __init__(self, string):
		self.string = string
	def __str__(self):
		return self.string

def format_time_old(form = 'YYYY/MM/DD|hh:mm:ss'):
	keywords = ['Y','M','D','h','m','s']
	breakers = ['/','\|',':']
	rpa=dict()
	cursor = 0
	while True:
		mark = False
		for wd in keywords+breakers:
			r = re.search('^'+wd+wd+'*', form)
			if r:
				if wd in keywords:
					rpa[wd] = [cursor, r.end()+cursor]
				cursor = r.end()+cursor
				form = form[r.end():]
				mark = True
				break
		if not mark:
			break
	if rpa:
		return rpa
	return None

def format_time(form = 'YYYY/MM/DD|hh:mm:ss'):
	keywords = ['Y','M','D','h','m','s']
	breakers = ['/','\|',':']
	rpa=dict()
	for wd in keywords:
		r = re.search(wd+wd+'*', form)
		if r:
			rpa[wd] = [r.start(), r.end()]
	if rpa:
		return rpa
	return None

def get_time(time, pattern='YYYY/MM/DD|hh:mm:ss'):
	rts = {
		's':.0,
		'm':0,
		'h':0,
		'Y':0,
		'M':0,
		'D':0
	}
	if type(pattern)==str:
		try:
			pattern = format_time(pattern)
		except:
			raise PatternError('invalid pattern1')
			return
	if type(pattern)!=dict:
		raise PatternError('invalid pattern2'+str(pattern))
		return
	for keyword in pattern:
		if keyword == 's':
			rts[keyword] = float(time[pattern[keyword][0]:pattern[keyword][1]])
		else:
			rts[keyword] = int(time[pattern[keyword][0]:pattern[keyword][1]])
	return rts
def get_zone_config(zone):
	symbol = timezone[zone][0]
	z = timezone[zone][1:].split(':')
	hours, minutes = z[0], ':' in timezone[zone] and z[1]
	return symbol+hours,symbol+str(int(minutes))


def is_leap_year(year):
	if not year%4 and (year%100 or not year%400) and (year-4000)%8000:
		return True
	return False

def rectify_time(time):
	month_config = [0, 31, 28+is_leap_year(time['Y']), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	new_time = time.copy()
	
	if new_time['s'] < 0:
		new_time['m']-=1
		new_time['s']+=60
	elif new_time['s'] >= 60:
		new_time['m']+=1
		new_time['s']-=60

	if new_time['m'] < 0:
		new_time['h']-=1
		new_time['m']+=60
	elif new_time['m'] >= 60:
		new_time['h']+=1
		new_time['m']-=60

	if new_time['h'] < 0:
		new_time['D']-=1
		new_time['h']+=24
	elif new_time['h'] >= 24:
		new_time['D']+=1
		new_time['h']-=24

	days_of_the_month = month_config[new_time['M']]
	last_month = 12 if new_time['M']==1 else new_time['M']-1
	days_of_last_month = month_config[last_month]
	
	if days_of_the_month != 0:
		if new_time['D']>days_of_the_month:
			new_time['M']+=1
			new_time['D']-=days_of_the_month
		elif new_time['D']<=0:
			new_time['M']-=1
			new_time['D']=days_of_last_month
		
		if new_time['M'] == 0:
			new_time['M']=12
			new_time['Y']-=1
		elif new_time['M']>12:
			new_time['M']=1
			new_time['Y']+=1
	
	return new_time

def transform_from(zone, time):
	new_time = time.copy()
	hours, minutes = get_zone_config(zone)
	new_time['h']=eval(str(time['h'])+'-'+hours)
	new_time['m']=eval(str(time['m'])+'-'+minutes)
	return rectify_time(new_time)

def transform_to(zone, time):
	new_time = time.copy()
	hours, minutes = get_zone_config(zone)
	new_time['h']=eval(str(time['h'])+hours)
	new_time['m']=eval(str(time['m'])+minutes)
	return rectify_time(new_time)

def transform(from_zone, to_zone, time):
	return transform_to(to_zone, transform_from(from_zone, time))

def generate_time(time, form = 'YYYY/MM/DD|hh:mm:ss'):
	pattern = format_time(form)
	string = form
	# keywords = ['Y','M','D','h','m','s']
	for keyword in pattern:
		length = pattern[keyword][1]-pattern[keyword][0]
		s = str(time[keyword])
		s = s if len(s)!=1 else '0'+s
		string = string.replace(keyword*length, s)
	return string

def localtime():
	now = time.localtime()
	new_time = {
		'Y':0,
		'M':0,
		'D':0,
		'h':0,
		'm':0,
		's':.0
	}
	cnt = 0
	for keyword in new_time:
		new_time[keyword] = now[cnt]
		cnt+=1
	return new_time

def get_weekday_by_timestamp(timestamp):
	return (int((timestamp+3600*8)/3600/24)%7+4)%7

def get_weekday(time_):
	return get_weekday_by_timestamp(time.mktime(time.strptime(generate_time(time_),'%Y/%m/%d|%H:%M:%S')))

x = {'s': 2, 'm': 2, 'h': 23, 'Y': 2020, 'M': 2, 'D': 29}
