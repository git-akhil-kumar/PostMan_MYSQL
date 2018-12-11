from incre_check import incre_check
def main():
	checker = incre_check(
		host = "", 		#IP address of Host
		username = "",		#Username of Mysql Server
		password = "",		#Password of Mysql Server
		database =  "",		#Database to work on
		url = 	"",		#Slack Url
		threshold = 0.9) 		#Value between 0-1 indicating the limit after which the script should send slack alerts)
	checker.runtask()	
if __name__ == '__main__':
	main()
