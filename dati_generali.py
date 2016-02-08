import strings
import emoji

prodB1 = prodB2 = prodA2 = prodA3 = 0


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
        dataA.append((dataA[1] / dataA[0] - 1) * 100)
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
        dataB.append((dataB[0] / dataB[1] - 1) * 100)
        dataB.append((actualB1 / actualB2 - 1) * 100)
        dataB.append(updated_data[1])  # ora aggiornamento
        dataB.append(actualB1)  # totale di oggi B1
        dataB.append(actualB2)  # totale di oggi B2
        return dataB


def get_statistics(a_strings, b_strings):
    message = "\nRAPPORTI SU PROD ODIERNA\n"
    to_send = '%.2f' % b_strings[2] + '% ' + emoji.get_emoji(b_strings[2])
    message += "\nB1/B2: " + to_send + ' (' + b_strings[0] - b_strings[1] + ')'
    to_send = '%.2f' % a_strings[2] + '% ' + emoji.get_emoji(a_strings[2])
    message += "\nA3/A2: " + to_send + ' (' + a_strings[1] - a_strings[0] + ')'
    b2overa3 = ((b_strings[0] / 11) / (a_strings[1] / 10) - 1) * 100
    to_send = '%.2f' % b2overa3 + '% ' + emoji.get_emoji(b2overa3)
    diffb2a3 = ' (' + b_strings[0] - b_strings[1] + ')'
    message += "\nB1/A3 stringa: " + to_send + diffb2a3
    message += strings.separator
    message += "\nRAPPORTI SU PROD TOTALE\n"
    to_send = '%.2f' % b_strings[3] + '% ' + emoji.get_emoji(b_strings[3])
    message += "\nB1/B2: " + to_send
    to_send = '%.2f' % a_strings[3] + '% ' + emoji.get_emoji(a_strings[3])
    message += "\nA3/A2: " + to_send
    b2overa3 = ((b_strings[5] / 11) / (a_strings[6] / 10) - 1) * 100
    to_send = '%.2f' % b2overa3 + '% ' + emoji.get_emoji(b2overa3)
    message += "\nB1/A3 stringa: " + to_send
    return message