from limits import limits
import re
import requests
import mysql.connector
import json
import time
class incre_check:
	def __init__(self,host,username,password,database,url,threshold):
		self.mysql_host = host
		self.mysql_username = username
		self.mysql_password = password
		self.mysql_database = database
		self.slack_url = url
		self.threshold = int(threshold)
	def getLimits(self):
		Limits = {'tinyint':limits.TINYINT,'tinyint unsigned':limits.TINYINT_UNSIGNED,'smallint':limits.SMALLINT,'smallint unsigned':limits.SMALLINT_UNSIGNED,'mediumint':limits.MEDIUMINT,'mediumint unsigned':limits.MEDIUMINT_UNSIGNED,'int':limits.INT,'int unsigned':limits.INT_UNSIGNED,'bigint':limits.BIGINT,'bigint unsigned':limits.BIGINT_UNSIGNED}
		return Limits
	def getAutoIncVal(self,my_sql_cursor,columns_list,table):
		my_sql_cursor.execute('select Max('+columns_list[0][0]+') from '+table)
		curr_val = my_sql_cursor.fetchall()
		curr_auto_inc_val = 0
		if curr_val[0][0] != None:
			curr_auto_inc_val = int(curr_val[0][0])
		return curr_auto_inc_val
	def getMaxValForDataType(self,columns_list):
		Limits = self.getLimits()
		data_type = re.sub(r'\(.*\)', '', columns_list[0][1])
		max_val = Limits[str(data_type)].value
		return max_val
	def alertSlack(self,table,amount_full):
		notification_json = {"text":"Alert "+table+" is "+str(int(amount_full*100))+" % full"}
		requests.post(self.slack_url,data=json.dumps(notification_json))
	def checker(self):
		my_sql_con = mysql.connector.connect(host=self.mysql_host,database=self.mysql_database,user=self.mysql_username,passwd=self.mysql_password)
		my_sql_cursor = my_sql_con.cursor()
		my_sql_cursor.execute("show tables")
		tables_list = my_sql_cursor.fetchall()
		for i in tables_list:
			my_sql_cursor.execute('show columns from '+str(i[0])+' where Extra="auto_increment"')
			columns_list = my_sql_cursor.fetchall()
			if len(columns_list) > 0:
				curr_auto_inc_val = self.getAutoIncVal(my_sql_cursor,columns_list,str(i[0]))
				max_val = self.getMaxValForDataType(columns_list)						
				amount_full = float(curr_auto_inc_val)/float(max_val)
				if amount_full-self.threshold>=0.0:
					self.alertSlack(str(i[0]),amount_full)
		my_sql_con.close()
	def runtask(self):
		while True:
			self.checker()
			time.sleep(float(5))
