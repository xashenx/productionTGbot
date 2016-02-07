#emoticons unicodes
scimmia_occhi = '\U0001F648'
scimmia_bocca = '\U0001F64A'
contento = '\U0001f604'
molto_contento = '\U0001F604'
contentissimo = '\U0001F601'
scazzato = '\U0001F612'
festa = '\U0001F389'
incazzato = '\U0001F621'
diavolo = '\U0001F608'


def get_emoji(value):
    if value < -1:
        return diavolo
    elif value >= -1 and value < 1:
        return incazzato
    elif value >= 1 and value < 1.5:
        return scimmia_bocca
    elif value >= 1.5 and value < 2.18:
        return scimmia_occhi
    elif value >= 2.18 and value < 2.3:
        return scazzato
    elif value >= 2.3 and value < 3:
        return contento
    elif value >= 3 and value < 6:
        return molto_contento
    elif value >= 6 and value < 9:
        return contentissimo
    else:
        return festa