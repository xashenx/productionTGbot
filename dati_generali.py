import strings
import emoji

prodB1 = prodB2 = prodA2 = prodA3 = 0
meseB1 = meseB2 = meseA2 = meseA3 = 0
# valori di produzione prima dell'applicazione coating del 24/02/16
fixB1 = 8644.0
fixB2 = 8309.7
fixA2 = 8291.7
fixA3 = 8383.2


def production(last_update_act, last_update_avg):
    b_strings = get_updated_production(2, last_update_avg)
    a_strings = get_updated_production(1, last_update_act)
    #message = strings.last_update_msg + strings.at_time_msg + b_strings[4]
    #message += strings.separator
    message = "\nPRODUZIONI ODIERNE\n"
    #: " + " %.2f" % result + "%
    message += "\nB1: %.1f" % b_strings[0] + " kW"
    message += " (TOT. %s" % last_update_avg[6] + ")"
    message += "\nB2: %.1f" % b_strings[1] + " kW"
    message += " (TOT. %s" % last_update_avg[7] + ")"
    message += "\nA2: %.1f" % a_strings[0] + " kW"
    message += " (TOT. %s" % last_update_act[6] + ")"
    message += "\nA3: %.1f" % a_strings[1] + " kW"
    message += " (TOT. %s" % last_update_act[7] + ")"
    message += strings.separator
    message += get_statistics(a_strings, b_strings)
    return message
    #sender(chat_id, message)


def get_updated_production(mode, updated_data):
    dataB = []
    dataA = []
    if mode == 1:
        #actualB1 = float(updated_data[6])
        #actualB2 = float(updated_data[7])
        actualA2 = float(updated_data[6])
        actualA3 = float(updated_data[7])
        dataA.append(actualA2 - prodA2)
        dataA.append(actualA3 - prodA3)
        if dataA[0] != 0 and dataA[1] != 0:
            dataA.append((dataA[1] / dataA[0] - 1) * 100)
        else:
            dataA.append(0)
        dataA.append((actualA3 / actualA2 - 1) * 100)
        dataA.append(updated_data[1])  # ora aggiornamento
        dataA.append(actualA2)  # totale di oggi A2
        dataA.append(actualA3)  # totale di oggi A3
        return dataA
    elif mode == 2:
        #actualA2 = float(updated_data[6])
        #actualA3 = float(updated_data[7])
        actualB1 = float(updated_data[6])
        actualB2 = float(updated_data[7])
        dataB.append(actualB1 - prodB1)
        dataB.append(actualB2 - prodB2)
        if dataB[0] != 0 and dataB[1] != 0:
            dataB.append((dataB[0] / dataB[1] - 1) * 100)
        else:
            dataB.append(0)
        dataB.append((actualB1 / actualB2 - 1) * 100)
        dataB.append(updated_data[1])  # ora aggiornamento
        dataB.append(actualB1)  # totale di oggi B1
        dataB.append(actualB2)  # totale di oggi B2
        return dataB


def get_statistics(a_strings, b_strings):
    message = "\nRAPPORTI SU PROD ODIERNA\n"
    to_send = '%.2f' % b_strings[2] + '% ' + emoji.get_emoji(b_strings[2], 1)
    diffb1b2 = ' (%.1f' % (b_strings[0] - b_strings[1]) + 'kW)'
    message += "\nB1/B2: " + to_send + diffb1b2
    to_send = '%.2f' % a_strings[2] + '% ' + emoji.get_emoji(a_strings[2], 2)
    diffa3a2 = ' (%.1f' % (a_strings[1] - a_strings[0]) + 'kW)'
    message += "\nA3/A2: " + to_send + diffa3a2
    b1overa3 = ((b_strings[0] / 11) / (a_strings[1] / 10) - 1) * 100
    to_send = '%.2f' % b1overa3 + '% ' + emoji.get_emoji(b1overa3, 1)
    diffb1a3 = ' (%.1f' % (b_strings[0] / 11 - a_strings[1] / 10) + 'kW)'
    message += "\nB1/A3 str: " + to_send + diffb1a3
    message += strings.separator
    message += statistiche_mese(b_strings[5], b_strings[6],
    a_strings[5], a_strings[6])
    message += strings.separator
    message += "\nRAPPORTI SU PROD TOTALE\n"
    message += '             [dopo 24/02][totale]\n'
    # calcola il rapporto di produzione dal 25/02/16
    B1postFix = b_strings[5] - fixB1
    B2postFix = b_strings[6] - fixB2
    B1B2postFix = (B1postFix / B2postFix - 1) * 100
    A2postFix = a_strings[5] - fixA2
    A3postFix = a_strings[6] - fixA3
    A3A2postFix = (A3postFix / A2postFix - 1) * 100
    B1A3postFix = ((B1postFix / 11) / (A3postFix / 10) - 1) * 100
    to_send = '[%.2f' % B1B2postFix + '% ' + emoji.get_emoji(B1B2postFix, 1)
    to_send += '][%.2f' % b_strings[3] + '% ' + emoji.get_emoji(b_strings[3], 1)
    message += "\nB1/B2: " + to_send + ']'
    to_send = '[%.2f' % A3A2postFix + '% ' + emoji.get_emoji(A3A2postFix, 1)
    to_send += '][%.2f' % a_strings[3] + '% ' + emoji.get_emoji(a_strings[3], 2)
    message += "\nA3/A2: " + to_send + ']'
    b2overa3 = ((b_strings[5] / 11) / (a_strings[6] / 10) - 1) * 100
    #to_send = '[%.2f' % B1A3postFix + '% ' + emoji.get_emoji(B1A3postFix, 1)
    to_send = '[%.2f' % B1A3postFix + '%'
    #to_send += '][%.2f' % b2overa3 + '% ' + emoji.get_emoji(b2overa3, 2)
    to_send += '][%.2f' % b2overa3 + '%'
    message += "\nB1/A3 str: " + to_send + ']'
    return message


def statistiche_mese(actB1, actB2, actA2, actA3):
    message = "\nRAPPORTI SU PROD MENSILE\n"
    cmB1 = actB1 - meseB1
    cmB2 = actB2 - meseB2
    cmA2 = actA2 - meseA2
    cmA3 = actA3 - meseA3
    #print('B1: ', actB1, meseB1, cmB1)
    #print('B2: ', actB2, meseB2, cmB2)
    #print('A2: ', actA2, meseA2, cmA2)
    #print('A3: ', actA3, meseA3, cmA3)
    B1B2 = (cmB1 / cmB2 - 1) * 100
    A3A2 = (cmA3 / cmA2 - 1) * 100
    B1A3 = ((cmB1 / 11) / (cmA3 / 10) - 1) * 100
    to_send = '%.2f' % B1B2 + '% ' + emoji.get_emoji(B1B2, 1)
    message += "\nB1/B2: " + to_send
    to_send = '%.2f' % A3A2 + '% ' + emoji.get_emoji(A3A2, 2)
    message += "\nA3/A2: " + to_send
    to_send = '%.2f' % B1A3 + '% ' + emoji.get_emoji(B1A3, 2)
    message += "\nB1/A3 str: " + to_send
    return message
