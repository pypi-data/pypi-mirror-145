 # -*- coding: utf-8 -*-
def info():
	info={
"questname":"Brainfix",
"platform":"ctfshow",
"contest" : "yrb22",
"description":"muscrepwebto",
"requirements":".",
"module options":[
	{"name":"cipher","required":True,"description":"the path of the text file."},
	]
}
	return(info)

def exploit(options):
	import re, itertools
	c = open(options["cipher"], 'r').read().strip()
	for i in itertools.permutations('><+-.,[]'):
		p = c.translate(str.maketrans(''.join(i), '01234567'))
		p = ''.join([chr(int(p[i: i + 3], 8)) for i in range(0, len(p), 3)])
		flag = re.search(r'ctfshow\{[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}\}', p)
		if flag:
			return (f"{flag.group()}\n    做完了，套神称之为烂题。")

def make_wp():
	wp=f"""
根据积累和特征，得到flag。
	"""
	return(wp)