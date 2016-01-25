import time
import random
import datetime
import telepot
import os.path

last_update_msg = "Ultimo aggiornamento"
at_time_msg = " alle ore "
no_data_file = "Mi spiace,\n il file di produzione non presente!"
command_not_found = "Mi spiace,\nil comando non è stato riconosciuto!"
stringList = ['B1', 'B2', 'A2', 'A3']
data_path = 'data/data_path'
separator = '\n---------------------------------------------------'


def production(chat_id):
    b_strings = get_updated_production(1)
    a_strings = get_updated_production(2)
    message = last_update_msg + at_time_msg + b_strings[4]
    message += separator
    message += "\nPRODUZIONI ODIERNE\n"
    #: " + " %.2f" % result + "%
    message += "\nB1: %.1f" % b_strings[0] + "\nB2: %.1f" % b_strings[1]
    message += "\nA2: %.1f" % a_strings[0] + "\nA3: %.1f" % a_strings[1]
    message += separator
    message += "\nRAPPORTI SU PROD ODIERNA\n"
    message += "\nB1/B2: %.2f" % b_strings[2] + "%"
    message += "\nA2/A3: %.2f" % a_strings[2] + "%"
    message += separator
    message += "\nRAPPORTI SU PROD TOTALE\n"
    message += "\nB1/B2: %.2f" % b_strings[3] + "%"
    message += "\nA2/A3: %.2f" % a_strings[3] + "%"
    sender(chat_id, message)

    #print("DEBUG: " + path + "/" + file_name)
    #sender(chat_id, no_data_file)


def get_updated_production(mode):
    with open(data_path) as f:
        path = f.read().strip()
    day = time.strftime("%d").lstrip('0')
    month = time.strftime("%m").lstrip('0')
    if mode == 1:
        dataB = []
        file_name = month + " giorno " + day + "_" + month + " istantanee.log"
    else:
        dataA = []
        file_name = month + " giorno " + day + "_" + month + " medie.log"

    if os.path.isfile(path + "/" + file_name):
        fileHandle = open(path + "/" + file_name, "r")
        lineList = fileHandle.readlines()
        fileHandle.close()

        msg = lineList[-2]
        msg = lineList[-1]
        msg = msg.replace('   ', 'z')
        msg = msg.replace(',', '.')
        msg = msg.split('z')
        if (len(msg) < 8):
            msg = lineList[-2]
            msg = msg.replace('   ', 'z')
            msg = msg.replace(',', '.')
            msg = msg.split('z')
        if mode == 1:
            dataB.append(float(float(msg[6]) - prodB1))
            dataB.append(float(float(msg[7]) - prodB2))
            dataB.append(float((dataB[0] / dataB[1] - 1) * 100))
            dataB.append(float(float(msg[6]) / float(msg[7]) - 1) * 100)
            dataB.append(msg[1])  # ora aggiornamento
            return dataB
        else:
            dataA.append(float(float(msg[6]) - prodA2))
            dataA.append(float(float(msg[7]) - prodA3))
            dataA.append(float((dataA[0] / dataA[1] - 1) * 100))
            dataA.append(float(float(msg[6]) / float(msg[7]) - 1) * 100)
            dataA.append(msg[1])  # ora aggiornamento
            return dataA
    else:
        return data


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Ricevuto comando: %s' % command)
    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1, 6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/rileva':
        production(chat_id)
    elif command.startswith("/imposta", 0, 14):
        length = len(command)
        cmd = command.split(' ')
        if length == 14 or len(cmd) < 3:
            message = "Sintassi comando: '/imposta (stringa) (valore)'"
            sender(chat_id, message)
        elif cmd[1] not in stringList:
            message = "Le stringhe disponibili sono: B1, B2, A2, A3"
            sender(chat_id, message)
        else:
            try:
                float(cmd[2])
                set_production(cmd)
                message = "Produzione di %s" % cmd[1]
                message += " aggiornata a %.1f" % float(cmd[2])
                sender(chat_id, message)
            except ValueError:
                message = "Valore '%s' non valido!" % cmd[2]
                sender(chat_id, message)
    elif command == '/aiuto':
        message = 'I comandi disponibili sono i seguenti:\n'
        message += '\n\\rileva - effettua rilevazione dei dati'
        message += '\n\imposta [STRINGA] [VALORE] - fissa il VALORE di produ'
        message += 'zione della STRINGA da cui valutare i dati'
        sender(chat_id, message)
    else:
        sender(chat_id, command_not_found)


def sender(chat_id, message):
    bot.sendMessage(chat_id, message)


def set_production(command):
    global prodB1, prodB2, prodA2, prodA3
    # with is like your try .. finally block in this case
    with open('data/produzioni', 'r') as prod_file:
        # read a list of lines into data
        data = prod_file.readlines()
    prod_file.close()

    # now change the 2nd line, note that you have to add a newline
    if command[1] == 'B1':
        prodB1 = float(command[2])
        line = 1
    elif command[1] == 'B2':
        prodB2 = float(command[2])
        line = 2
    elif command[1] == 'A2':
        prodA2 = float(command[2])
        line = 3
    elif command[1] == 'A3':
        prodA3 = float(command[2])
        line = 4
    data[line] = command[1] + ',' + command[2] + '\n'

    # and write everything back
    with open('data/produzioni', 'w') as prod_file:
        prod_file.writelines(data)
    prod_file.close()


api_token_path = 'data/api.token'
with open(api_token_path) as f:
    apitoken = f.read().strip()

with open('data/produzioni', 'r') as prod_file:
    # read a list of lines into data
    data = prod_file.readlines()
prodB1 = float(data[1].split(',')[1])
prodB2 = float(data[2].split(',')[1])
prodA2 = float(data[3].split(',')[1])
prodA3 = float(data[4].split(',')[1])

bot = telepot.Bot(apitoken)
bot.notifyOnMessage(handle)
print('In ascolto')

while 1:
    time.sleep(10)