#  emoticons unicodes
scimmia_occhi = '\U0001F648'
scimmia_bocca = '\U0001F64A'
contento = '\U0001f604'
molto_contento = '\U0001F604'
contentissimo = '\U0001F601'
scazzato = '\U0001F612'
festa = '\U0001F389'
incazzato = '\U0001F621'
diavolo = '\U0001F608'

#  valori di riferimento delle stringhe
rifA = 1.05
rifB = 2.18


def get_emoji(value, mode):
    if mode == 1:  # stringhe B
        diff = value - rifB
    else:  # stringhe A
        diff = value - rifA

    #if value < -1:
    if diff < -3:
        return diavolo
    #elif value >= -1 and value < 1:
    elif diff >= -3 and diff < -1:
        return incazzato
    #elif value >= 1 and value < 1.5:
    elif diff >= 1 and diff < -0.5:
        return scimmia_bocca
    #elif value >= 1.5 and value < 2.18:
    elif diff >= -0.5 and diff < 0:
        return scimmia_occhi
    #elif value >= 2.18 and value < 2.3:
    elif diff >= 0 and diff < 0.5:
        return scazzato
    #elif value >= 2.3 and value < 3:
    elif diff >= 0.5 and diff < 1.5:
        return contento
    #elif value >= 3 and value < 6:
    elif diff >= 1.5 and diff < 3:
        return molto_contento
    #elif value >= 6 and value < 9:
    elif diff >= 3 and diff < 5:
        return contentissimo
    else:
        return festa
