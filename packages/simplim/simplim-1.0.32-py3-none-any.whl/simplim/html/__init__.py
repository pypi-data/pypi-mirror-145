def MakeTag(tag, value, style = ''):
	return '<' + tag + ' style=\" ' + style + '\">' + value + '</'+tag+'>' 

def MakeHtml(head, body):
	return '<!DOCTYPE html><html>' + head + body + '</html>'

def MakeHead(dict_ = {}, title = ''):
	head = MakeTag('title', title)
	if dict_:
		for key in dict_:
			head += MakeTag(key, dict_[key])
	return MakeTag('head', head)

def AddUp(dict_, br = ''):
	result = ''
	if br:
		br = '<br>'
	for tag in dict_:
		result += tag + br
	return result

def MakeBody(dict_ = {}):
	body = ''
	if dict_:
		for key in dict_:
			body += MakeTag(key, dict_[key][0], dict_[key][1]) + '<br>'
	return MakeTag('body', body)
	
def Html(title = '', head_dict = {}, body_dict = {}, path = None):
	html = MakeHtml(MakeHead(head_dict, title), MakeBody(body_dict))
	if path:
		open(path,'w').write(html)
	else:
		return html

def SimpleHtml(head_dict = {}, body_dict = {}, path = None):
	html = MakeHtml(AddUp(head_dict), AddUp(body_dict, 1))
	if path:
		open(path,'w').write(html)
	else:
		return html


	