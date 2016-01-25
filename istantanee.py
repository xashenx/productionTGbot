import strings


def actual_production(last_update_act):
    #time = last_update_act[1]
    b1 = float(last_update_act[2])
    b2 = float(last_update_act[3])
    a2 = float(last_update_act[4])
    a3 = float(last_update_act[5])

    #message = strings.last_update_msg + strings.at_time_msg + time
    #message += strings.separator
    message = "\nPRODUZIONI ISTANTANEE\n"
    message += "\nB1: %s" % b1 + " kWh\nB2: %s" % b2 + " kWh"
    message += "\nA2: %s" % a2 + " kWh\nA3: %s" % a3 + " kWh"
    message += strings.separator

    if b1 == 0 or b2 == 0:
        b_perc = 0
    else:
        b_perc = (b1 / b2 - 1) * 100
    if a2 == 0 or a3 == 0:
        a_perc = 0
    else:
        a_perc = (a2 / a3 - 1) * 100
    message += "\nRAPPORTI SU ISTANTANEE\n"
    message += "\nB1/B2: %.2f" % b_perc + "%"
    message += "\nA2/A3: %.2f" % a_perc + "%"
    return message