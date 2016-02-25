import strings
import emoji


def actual_averages(last_update_avg):
    #time = last_update_avg[1]
    b1 = float(last_update_avg[2])
    b2 = float(last_update_avg[3])
    a2 = float(last_update_avg[4])
    a3 = float(last_update_avg[5])

    #message = strings.last_update_msg + strings.at_time_msg + time
    #message += strings.separator
    message = "\nPRODUZIONI MEDIE\n"
    message += "\nB1: %s" % b1 + " kWh\nB2: %s" % b2 + " kWh"
    message += "\nA2: %s" % a2 + " kWh\nA3: %s" % a3 + " kWh"
    message += get_statistics(b1, b2, a2, a3)
    return message


def get_statistics(b1, b2, a2, a3):
    a_perc = b_perc = b1a3_perc = 0
    if not (b1 == 0 or b2 == 0):
        b_perc = (b1 / b2 - 1) * 100
        if not a3 == 0:
            b1a3_perc = ((b1 / 11) / (a3 / 10) - 1) * 100
    if not (a2 == 0 or a3 == 0):
        a_perc = (a3 / a2 - 1) * 100

    message = strings.separator
    message += "\nRAPPORTI SU MEDIE\n"
    message += "\nB1/B2: %.2f" % b_perc + "% " + emoji.get_emoji(b_perc, 1)
    message += "\nA3/A2: %.2f" % a_perc + "% " + emoji.get_emoji(a_perc, 2)
    message += "\nB1/A3 stringa: %.2f" % b1a3_perc
    message += "% " + emoji.get_emoji(b1a3_perc, 2)
    return message