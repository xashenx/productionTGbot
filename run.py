#!/usr/bin/env python3

import time
import telepot
import os.path
import istantanee
import strings
import dati_generali
import medie
import random_answer

last_update_avg = []
last_update_act = []
valid_act_file = False
valid_avg_file = False
result = False


def get_last_update(mode):
    global last_update_act, last_update_avg, valid_act_file, valid_avg_file
    global result
    with open(strings.data_path) as f:
        path = f.read().strip()
    day = time.strftime("%d").lstrip('0')
    month = time.strftime("%m").lstrip('0')
    # controlla la validità del file
    if mode == 1:
        file_name = month + " giorno " + day + "_" + month + " istantanee.log"
    else:
        file_name = month + " giorno " + day + "_" + month + " medie.log"
    valid_file = check_file_validity(path + file_name, mode)

    # se è valido, estrapola i dati
    if valid_file:
        #fileHandle = open(path + file_name, "r")
        #lineList = fileHandle.readlines()
        #fileHandle.close()

        #position = -1
        #msg = lineList[position]
        #msg = msg.replace('   ', 'z')
        #msg = msg.replace(',', '.')
        #msg = msg.split('z')

        #cond_a = len(msg) < 8
        #if not cond_a:
            #cond_b = is_the_string_valid(msg)
        #while cond_a or cond_b:
            #position -= 1
            #msg = lineList[position]
            #msg = msg.replace('   ', 'z')
            #msg = msg.replace(',', '.')
            #msg = msg.split('z')
            #cond_a = len(msg) < 8
            #if not cond_a:
                #cond_b = is_the_string_valid(msg)
        #if not cond_a and not cond_b:
            #msg[7] = msg[7].replace('\n', '')
            #msg[6] = str(float(msg[6]))
            #msg[7] = str(float(msg[7]))
            #if mode == 1:
                #last_update_act = msg
                #valid_act_file = valid_file
            #elif mode == 2:
                #last_update_avg = msg
                #valid_avg_file = valid_file
            result = True  # sono presenti dei dati aggiornati!
    else:
        result = False


def check_file_validity(fileToCheck, mode):
    global last_update_act, last_update_avg, valid_act_file, valid_avg_file

    cond_1 = os.path.isfile(fileToCheck)  # il file esiste
    cond_2 = True  # trovata una riga valida
    if cond_1 and os.stat(fileToCheck).st_size > 0:  # il file contiene dati
        fileHandle = open(fileToCheck, "r")
        lineList = fileHandle.readlines()
        fileHandle.close()
        position = -1
        while position > -6 and cond_2 and (len(lineList) + position) > 1:
            msg = lineList[position]
            position -= 1
            msg = msg.replace('   ', 'z')
            msg = msg.replace(',', '.')
            msg = msg.split('z')
            if not len(msg) < 8:
                cond_2 = is_the_string_valid(msg)
                if not cond_2:
                    msg[7] = msg[7].replace('\n', '')
                    msg[6] = str(float(msg[6]))
                    msg[7] = str(float(msg[7]))
                    if mode == 1:
                        last_update_act = msg
                        valid_act_file = True
                    elif mode == 2:
                        last_update_avg = msg
                        valid_avg_file = True
                else:
                    if mode == 1:
                        valid_act_file = False
                    elif mode == 2:
                        valid_avg_file = False
    return cond_1 and not cond_2


def is_the_string_valid(line):
        cond_b = line[2].startswith('Error') or line[3].startswith('Error')
        cond_c = line[4].startswith('Error') or line[5].startswith('Error')
        cond_d = line[6].startswith('Error') or line[7].startswith('Error')
        cond_e = len(line[6]) < 6 or len(line[7]) < 6
        return cond_b or cond_c or cond_d or cond_e


def check_auth(chat_id):
        with open('data/auth_client') as f:
            mylist = f.read().splitlines()
        return chat_id in mylist


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    from_string = 'da %s' % msg['from']['first_name']
    print('Ricevuto comando: %s' % command, from_string)
    if not check_auth(str(chat_id)):
        message = 'Mi dispiace, non posso eseguire il comando.\n'
        sender(chat_id, message)
        print('chat_id non riconosciuto %s' % chat_id, '%s' % from_string)
        return
    elif not (valid_act_file and valid_avg_file):
        # aggiorniamo i dati in possesso per vedere se ora abbiamo dati validi
        get_last_update(1)
        get_last_update(2)

    if msg['from']['first_name'] == 'Fabrizio' and not random_answer.answer():
        message = random_answer.joke()
        sender(chat_id, message)
    elif not (valid_act_file and valid_avg_file and result):
        # se non sono ancora validi, comunicarlo all'utente'
        if not result:
            message = 'Non sono presenti dati aggiornati per soddisfare' + \
            ' la richiesta!'
        else:
            message = 'E\' stato riscontrato un problema coi dati.\n'
            message += 'Riprova più tardi!.\n'
        sender(chat_id, message)
    elif not check_auth(str(chat_id)):
        message = 'Mi dispiace, non posso eseguire il comando.\n'
        sender(chat_id, message)
        print('chat_id non riconosciuto %s' % chat_id, '%s' % from_string)
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
    elif command == '/produzione':
        message = "B1: %s\n" % dati_generali.prodB1
        message += "B2: %s\n" % dati_generali.prodB2
        message += "A2: %s\n" % dati_generali.prodA2
        message += "A3: %s\n" % dati_generali.prodA3
        sender(chat_id, message)
    elif command == '/statistiche':
        # prelevo i dati aggiornati
        get_last_update(1)
        get_last_update(2)
        # recupera statistiche riferite alle produzioni totali e odierne
        b_strings = dati_generali.get_updated_production(2, last_update_avg)
        a_strings = dati_generali.get_updated_production(1, last_update_act)
        message = dati_generali.get_statistics(a_strings, b_strings)
        # recupera statistiche riferite alle istantanee
        b1 = float(last_update_act[2])
        b2 = float(last_update_act[3])
        a2 = float(last_update_act[4])
        a3 = float(last_update_act[5])
        message += istantanee.get_statistics(b1, b2, a2, a3)
        # recupera statistiche riferite alle medie
        b1 = float(last_update_avg[2])
        b2 = float(last_update_avg[3])
        a2 = float(last_update_avg[4])
        a3 = float(last_update_avg[5])
        message += medie.get_statistics(b1, b2, a2, a3)
        sender(chat_id, message)
    elif command == '/aiuto':
        message = 'I comandi disponibili sono i seguenti:\n'
        message += '\n\\rileva - effettua rilevazione dei dati'
        message += '\n\imposta [STRINGA] [VALORE] - fissa il VALORE di produ'
        message += 'zione della STRINGA da cui valutare i dati'
        sender(chat_id, message)
    elif command == '/start':
        message = 'Grazie per aver iniziato ad usare MontaltoBot!\n'
        sender(chat_id, message)
    elif command == '/fine':
        get_last_update(1)
        get_last_update(2)
        cmd = [0, 'B1', last_update_avg[6]]
        set_production(cmd)
        message = 'Produzione B1 impostata a: ' + last_update_avg[6] + '\n'
        cmd = [0, 'B2', last_update_avg[7]]
        set_production(cmd)
        message += 'Produzione B2 impostata a: ' + last_update_avg[7] + '\n'
        cmd = [0, 'A2', last_update_act[6]]
        set_production(cmd)
        message += 'Produzione A2 impostata a: ' + last_update_act[6] + '\n'
        cmd = [0, 'A3', last_update_act[7]]
        set_production(cmd)
        message += 'Produzione A3 impostata a: ' + last_update_act[7] + '\n'
        message += 'Produzioni aggiornate!\n'
        sender(chat_id, message)
    else:
        sender(chat_id, strings.command_not_found)


#def check_command(command):
    #ist_commands = ['/istantanee',]
    #avg_commands = ['/medie']
    #complete_commands = ['/statistiche','/completo']
    #other_commands = ['/start','/fine','/aiuto','/produzione','/imposta']


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
        #dati_generali.prodB1 = float(command[2])
        line = 1
    elif command[1] == 'B2':
        #dati_generali.prodB2 = float(command[2])
        line = 2
    elif command[1] == 'A2':
        #dati_generali.prodA2 = float(command[2])
        line = 3
    elif command[1] == 'A3':
        #dati_generali.prodA3 = float(command[2])
        line = 4
    data[line] = command[1] + ',' + command[2] + '\n'

    # and write everything back
    with open('data/produzioni', 'w') as prod_file:
        prod_file.writelines(data)
    prod_file.close()


def update_production_variables():
    with open('data/produzioni', 'r') as prod_file:
        # leggo i dati di produzione del giorno precedente dal file
        data = prod_file.readlines()
        dati_generali.prodB1 = float(data[1].split(',')[1])
        dati_generali.prodB2 = float(data[2].split(',')[1])
        dati_generali.prodA2 = float(data[3].split(',')[1])
        dati_generali.prodA3 = float(data[4].split(',')[1])


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
automatic_update_done = False
end_of_day = False
wakeup_interval = 10
get_last_update(1)
get_last_update(2)

while 1:
    time.sleep(wakeup_interval)
    ora = time.strftime('%H')
    minuti = time.strftime('%M')
    orario = ora + ':' + minuti
    if orario == '8:00':
        wakeup_interval = 20
    elif orario == '20:00':
        wakeup_interval = 50

    if int(ora) > 8 and int(ora) < 20:  # manda aggiornamento solo tra 8 e 18
        valid_files = valid_act_file and valid_avg_file
        if not valid_files:
            get_last_update(1)
            get_last_update(2)
            valid_files = valid_act_file and valid_avg_file
        if ("00" in minuti) and not automatic_update_done and valid_files:
            print("invio aggiornamento automatico delle ore %s" % orario)
            get_last_update(1)
            get_last_update(2)
            message = 'Aggiornamento orario delle %s\n' % orario
            message += strings.last_update_msg + strings.at_time_msg
            message += last_update_act[1]
            message += strings.separator
            dati = dati_generali.production(last_update_act, last_update_avg)
            message += dati
            sender('-108582578', message)
            automatic_update_done = True
        elif ("01" in minuti) and automatic_update_done:
            automatic_update_done = False
        end_of_day = False
    # TODO verificare quando istantanee tutte a 0 (su 2/3 check)
    # e chiudere la giornata (aumentare intervallo di wakeup?)
    #print(last_update_act[3])
    #if last_update_act[3] == '0.0':
        #print("asdasdasd")
    if int(ora) > 19 and not end_of_day:  # giornata è finita aggiorna prod
        get_last_update(1)
        get_last_update(2)
        cmd = [0, 'B1', last_update_avg[6]]
        set_production(cmd)
        cmd = [0, 'B2', last_update_avg[7]]
        set_production(cmd)
        cmd = [0, 'A2', last_update_act[6]]
        set_production(cmd)
        cmd = [0, 'A3', last_update_act[7]]
        set_production(cmd)
        end_of_day = True
        valid_act_file = False
        valid_avg_file = False
    if orario == '00:05':
        update_production_variables()
        print('Fine giornata. Produzione aggiornata!')
