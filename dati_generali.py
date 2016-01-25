import strings

prodB1 = prodB2 = prodA2 = prodA3 = 0


def production(last_update_act, last_update_avg):
    b_strings = get_updated_production(1, last_update_act)
    a_strings = get_updated_production(2, last_update_avg)
    #message = strings.last_update_msg + strings.at_time_msg + b_strings[4]
    #message += strings.separator
    message = "\nPRODUZIONI ODIERNE\n"
    #: " + " %.2f" % result + "%
    message += "\nB1: %.1f" % b_strings[0] + "\nB2: %.1f" % b_strings[1]
    message += "\nA2: %.1f" % a_strings[0] + "\nA3: %.1f" % a_strings[1]
    message += strings.separator
    message += "\nRAPPORTI SU PROD ODIERNA\n"
    message += "\nB1/B2: %.2f" % b_strings[2] + "%"
    message += "\nA2/A3: %.2f" % a_strings[2] + "%"
    message += strings.separator
    message += "\nRAPPORTI SU PROD TOTALE\n"
    message += "\nB1/B2: %.2f" % b_strings[3] + "%"
    message += "\nA2/A3: %.2f" % a_strings[3] + "%"
    return message
    #sender(chat_id, message)


def get_updated_production(mode, updated_data):
    dataB = []
    dataA = []
    if mode == 1:
        actualB1 = float(updated_data[6])
        actualB2 = float(updated_data[7])
        dataB.append(actualB1 - prodB1)
        dataB.append(actualB2 - prodB2)
        dataB.append((dataB[0] / dataB[1] - 1) * 100)
        dataB.append((actualB1 / actualB2 - 1) * 100)
        dataB.append(updated_data[1])  # ora aggiornamento
        return dataB
    elif mode == 2:
        actualA2 = float(updated_data[6])
        actualA3 = float(updated_data[7])
        dataA.append(actualA2 - prodA2)
        dataA.append(actualA3 - prodA3)
        dataA.append((dataA[0] / dataA[1] - 1) * 100)
        dataA.append((actualA2 / actualA3 - 1) * 100)
        dataA.append(updated_data[1])  # ora aggiornamento
        return dataA