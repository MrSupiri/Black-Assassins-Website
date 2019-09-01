import sqlite3
from datetime import datetime
import os
import pymysql
import gc


class database:
	def __init__(self):
		try:
			self.conn = sqlite3.connect('database/database.db')
			self.c = self.conn.cursor()
		except Exception as e:
			print(str(type(e).__name__) + " : " + str(e))

	def read(self, query, *pars):
		try:
			#query = _escape_unicode(query)
			self.c.execute(query, pars)
			return self.c.fetchall()
		except Exception as e:
			print(str(type(e).__name__) + " : " + str(e))

	def write(self, query, *pars):
		try:
			#query = _escape_unicode(query)
			self.c.execute(query, pars)
			self.conn.commit()
			return query
		except Exception as e:
			return str(str(type(e).__name__) + " : " + str(e))

	def delete(self, table, id):
		self.write("DELETE FROM '{}' WHERE id = '{}'".format(table, id))
	
	def close(self):
		self.c.close()
		self.conn.close()
		gc.collect()

class remoteDB:
	def __init__(self):
		self.conn = pymysql.connect(host="localhost",
									user = "blackassassins",
									passwd = "bAadmin34",
									db = "b3_ba")
		self.c = self.conn.cursor()
	def getadmins(self):
		try:
			self.c.execute('''SELECT name,id,guid,group_bits,ip,FROM_UNIXTIME(time_edit) FROM clients WHERE group_bits > 10 ORDER BY group_bits DESC''')
			return self.c.fetchall()
		except Exception as e:
			print(str(type(e).__name__) + " : " + str(e))
			
	def penalties(self):
		try:
			self.c.execute('''
								SELECT id,type, 
								(SELECT clients.name from clients where clients.id=client_id) as 'Player',
								reason,
								(SELECT clients.name from clients where clients.id=admin_id) as 'Admin',
								FROM_UNIXTIME(time_expire) as 'Expire Time'
								from penalties 
								WHERE (inactive != 1 and type != 'Warning' and type != 'Kick' and (SELECT clients.name from clients where clients.id=admin_id) IS NOT NULL )
								ORDER BY time_add DESC;
							''')
			return self.c.fetchall()
		except Exception as e:
			print(str(type(e).__name__) + " : " + str(e))
	
	def close(self):
		self.c.close()
		self.conn.close()
		gc.collect()
			
	
