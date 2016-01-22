import sys
import time
import random
import datetime
import telepot
import time
import os.path

prodB1 = 4442.7
prodB2 = 4290.2

def production(chat_id):
	day = time.strftime("%d").lstrip('0')
	month = time.strftime("%m").lstrip('0')
	file_name = month + " giorno " + day + "_" + month + " medie.txt"

	if os.path.isfile(file_name):
		fileHandle = open (file_name,"r" )
		lineList = fileHandle.readlines()
		fileHandle.close()

		str = lineList[-2]
		str = lineList[-1]
		str = str.replace('   ','z')
		str = str.replace(',','.')
		str = str.split('z')
		if (len(str)<8):
			str = lineList[-2]
			str = str.replace('   ','z')
			str = str.replace(',','.')
			str = str.split('z')

		print(str)
		result = float((float(float(prodB1) - float(str[6]))/float(float(prodB2) - float(str[7]))-1)*100)
		print("%.2f%%" % result)
		bot.sendMessage(chat_id, "Ultimo aggiornamento: " + str[0] + " alle ore " + str[1])
		bot.sendMessage(chat_id, "Confronto produzioni odierne: " + "%.2f" % result + "%")
	else :
		bot.sendMessage(chat_id, "Mi spiace,\n il file di produzione non presente!")

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)
    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/prod':
        production(chat_id)

bot = telepot.Bot('137481181:AAGGl_Sqd86Qs2TT4W5xTTgjaGoZxrjxlVI')
bot.notifyOnMessage(handle)
print('I am listening ...')

while 1:
    time.sleep(10)