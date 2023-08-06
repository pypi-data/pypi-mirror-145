from subprocess import call
import os
# osascript -e "display notification \"test\" with title \"title\" sound name \"Blow\" "
def notify(title="Notificaton", content='content', subtitle='subtitle', sound=''):
	cmd = 'display notification "' + content + '" with title "' + title + '" ' + 'subtitle ' + '"' + subtitle + '" ' 
	if sound:
		if os.path.exists(sound):
			call(["osascript", "-e", cmd])
			call(['play', '-q', sound])
			return
		if sound == 'default':
			cmd+='sound name ' + '""'
		else:
			cmd+='sound name ' + '"' + sound + '"'
	call(["osascript", "-e", cmd])


def dialog(title='Dialog', content='content', subtitle='subtitle'):
	cmd = 'display dialog "' + content + '" with title "' + title + '" '
	x=call(['osascript', '-e', cmd])
	return not bool(x)

def run(cmd):
	call(['osascript','-e',cmd])