import time
import random
import datetime
import telepot
import os.path
import istantanee
import strings
import dati_generali
import medie

last_update_avg = []
last_update_act = []


def get_last_update(mode):
    global last_update_act, last_update_avg
    with open(strings.data_path) as f:
        path = f.read().strip()
    day = time.strftime("%d").lstrip('0')
    month = time.strftime("%m").lstrip('0')
    if mode == 1:
        file_name = month + " giorno " + day + "_" + month + " istantanee.log"
    else:
        file_name = month + " giorno " + day + "_" + month + " medie.log"
    if os.path.isfile(path + file_name):
        fileHandle = open(path + file_name, "r")
        lineList = fileHandle.readlines()
        fileHandle.close()

        position = -1
        msg = lineList[position]
        msg = msg.replace('   ', 'z')
        msg = msg.replace(',', '.')
        msg = msg.split('z')

        cond_a = len(msg) < 8
        if not cond_a:
            cond_b = is_the_string_valid(msg)
        while cond_a or cond_b:
            position -= 1
            msg = lineList[position]
            msg = msg.replace('   ', 'z')
            msg = msg.replace(',', '.')
            msg = msg.split('z')
            cond_a = len(msg) < 8
            if not cond_a:
                cond_b = is_the_string_valid(msg)
        msg[7] = msg[7].replace('\n', '')
        msg[6] = str(float(msg[6]))
        msg[7] = str(float(msg[7]))
        if mode == 1:
            last_update_act = msg
        elif mode == 2:
            last_update_avg = msg


def is_the_string_valid(line):
        cond_b = line[2].startswith('Error') or line[3].startswith('Error')
        cond_c = line[4].startswith('Error') or line[5].startswith('Error')
        cond_d = line[6].startswith('Error') or line[7].startswith('Error')
        cond_e = len(line[6]) < 6 or len(line[7]) < 6
        return cond_b or cond_c or cond_d or cond_e


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Ricevuto comando: %s' % command)
    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1, 6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/generali':
        get_last_update(1)
        get_last_update(2)
        message = strings.last_update_msg + strings.at_time_msg
        message += last_update_act[1]
        message += strings.separator
        message += dati_generali.production(last_update_act, last_update_avg)
        sender(chat_id, message)
    elif command.startswith("/imposta", 0, 14):
        length = len(command)
        cmd = command.split(' ')
        if length == 14 or len(cmd) < 3:
            message = "Sintassi comando: '/imposta (stringa) (valore)'"
            sender(chat_id, message)
        elif cmd[1] not in strings.stringList:
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
    elif command == '/istantanee':
        get_last_update(1)
        message = strings.last_update_msg + strings.at_time_msg
        message += last_update_act[1]
        message += strings.separator
        message += istantanee.actual_production(last_update_act)
        sender(chat_id, message)
    elif command == '/medie':
        get_last_update(2)
        message = strings.last_update_msg + strings.at_time_msg
        message += last_update_avg[1]
        message += strings.separator
        message += medie.actual_averages(last_update_avg)
        sender(chat_id, message)
    elif command == '/completo':
        get_last_update(1)
        get_last_update(2)
        message = strings.last_update_msg + strings.at_time_msg
        message += last_update_act[1]
        message += strings.separator
        message += dati_generali.production(last_update_act, last_update_avg)
        message += strings.separator
        message += medie.actual_averages(last_update_avg)
        message += strings.separator
        message += istantanee.actual_production(last_update_act)
        sender(chat_id, message)
    #elif command == '/statistiche':
        #message = message
        #sender(chat_id, message)
    elif command == '/aiuto':
        message = 'I comandi disponibili sono i seguenti:\n'
        message += '\n\\rileva - effettua rilevazione dei dati'
        message += '\n\imposta [STRINGA] [VALORE] - fissa il VALORE di produ'
        message += 'zione della STRINGA da cui valutare i dati'
        sender(chat_id, message)
    elif command == '/start':
        message = 'Grazie per aver iniziato ad usare MontaltoBot!\n'
        sender(chat_id, message)
    else:
        sender(chat_id, strings.command_not_found)


def sender(chat_id, message):
    bot.sendMessage(chat_id, message)


def set_production(command):
    #global prodB1, prodB2, prodA2, prodA3
    # with is like your try .. finally block in this case
    with open('data/produzioni', 'r') as prod_file:
        # read a list of lines into data
        data = prod_file.readlines()
    prod_file.close()

    # now change the 2nd line, note that you have to add a newline
    if command[1] == 'B1':
        dati_generali.prodB1 = float(command[2])
        line = 1
    elif command[1] == 'B2':
        dati_generali.prodB2 = float(command[2])
        line = 2
    elif command[1] == 'A2':
        dati_generali.prodA2 = float(command[2])
        line = 3
    elif command[1] == 'A3':
        dati_generali.prodA3 = float(command[2])
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
dati_generali.prodB1 = float(data[1].split(',')[1])
dati_generali.prodB2 = float(data[2].split(',')[1])
dati_generali.prodA2 = float(data[3].split(',')[1])
dati_generali.prodA3 = float(data[4].split(',')[1])

bot = telepot.Bot(apitoken)
bot.notifyOnMessage(handle)
print('In ascolto')

while 1:
    time.sleep(10)
    #print(last_update_act)
    #print(last_update_avg)