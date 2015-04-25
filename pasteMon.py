import requests
import argparse
import time
from models import Paste, Content, session


def monitor_paste(paste):
	user_agent = {"User-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
	base_url = 'http://pastebin.com/raw.php?i='
	full_url = base_url + paste
	try:
		resp = requests.get(full_url, headers=user_agent)
		command = resp.text
		return command
	except Exception, e:
		print '%s is unavailble. %s error received' %(paste, e)
		return


def getPastes():
	try:
		return session.query(Paste).all()
	except TypeError as error:
		return 'no connection to database'


def getCommand(paste):
	try:
		return session.query(Content).filter(Content.paste_fk == paste).order_by(-Content.id).first()
	except TypeError as error:
		return 'no connection to database'

def main():
	parser = argparse.ArgumentParser(description='Tool to monitor pastebin pastes')
	parser.add_argument('-p', '--paste', help='add paste to monitor')
	parser.add_argument('--monitor', action='store_true', help='monitor pastes')
	args = parser.parse_args()
	if args.paste:
		desc = raw_input('Enter a description for this paste: ')
		new_paste = Paste(paste_id=args.paste, desc=desc)
		session.add(new_paste)
		session.commit()
	if args.monitor:
		while True:
			for result in getPastes():
				paste_content = getCommand(result.paste_id)
				command = monitor_paste(result.paste_id)
				if paste_content == None or command != paste_content.paste_body:
					print 'paste has been updated:\t%s' %command
					content_update = Content(paste_body=command, paste_fk=result.paste_id)
					session.add(content_update)
					session.commit()
				else:
					print 'paste has not been updated'
			time.sleep(60)


if __name__ == '__main__':
	main()

#http://stackoverflow.com/questions/10770377/howto-create-db-mysql-with-sqlalchemy
#https://github.com/moranned/page-monitor/blob/master/models.py
