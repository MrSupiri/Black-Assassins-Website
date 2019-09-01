import xml.etree.ElementTree as ET
import dateutil.parser as dparser
import datetime
import re

_reColor = re.compile(r'\^[0-9a-z]')
def getstatus():
	tree = ET.parse('b3_status.xml')
	root = tree.getroot()

	game = root[0].attrib

	items = {}

	items.update( {'Server IP':game['Ip']+':'+game['Port'] } )
	items.update( {'Map':game['Map'][3:].title() } )
	if str(game['Type']) == 'sd':
		gametype = 'Search & Destroy'
	else:
		gametype = game['Type']
	items.update( {'GameType': gametype } )
	items.update( {'Online Players':game['OnlinePlayers']+' / '+root[0][22].attrib['Value'] } )
	items.update( {'Total Rounds':game['Rounds'] } )
	items.update( {'UpTime': root[0][8].attrib['Value'] } )
	items.update( {'Mod': root[0][12].attrib['Value'] } )
	items.update( {'Map Start Time': root[0][28].attrib['Value'] } )

	clients = []
	for client in root[1]:
		if str(client.attrib['State']) == '0':
			state = 'Alive'
		else:
			state = 'Dead'
			
		ptime = dparser.parse(client.attrib['Updated'])
		ntime = datetime.datetime.now()
		
		stime = str(int((ntime-ptime).total_seconds())% 60).zfill(2)
		mtime = str(int((ntime-ptime).total_seconds()// 60 % 60)).zfill(2)
		htime = str(int((ntime-ptime).total_seconds()// 3600 % 24 )).zfill(2)
		
		
		if htime == '00':
			time = '{}:{}'.format(mtime,mtime)
		else:
			time = '{}:{}:{}'.format(htime,mtime,mtime)
		
		
		level = int(client.attrib['Level'])
		
		if level == 0:
			level = 'Guest'
		elif level == 1:
			level = 'User'
		elif level == 2:
			level = 'Regular'
		elif level == 20:
			level = 'Moderator'
		elif level == 40:
			level = 'Admin'
		elif level == 60:
			level = 'Full Admin'
		elif level == 80:
			level = 'Senior Admin'
		elif level == 100:
			level = 'Super Admin'
		
		
		try:
			clients.append([client.attrib['CID'].zfill(2),client.attrib['Name'],client.attrib['Score'],state,client.attrib['DBID'],client.attrib['IP'],level,time])
		except:
			pass
	try:
		hostname = re.sub(_reColor, '', root[0][23].attrib['Value']).strip()
	except:
		hostname = ""
		
	return items,sorted(clients),root.attrib,hostname