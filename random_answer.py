# -*- coding: utf-8 -*-

from random import randint
import time

jokes = ['Mi spiace non posso darti i dati!',
'Magari un altro giorno.',
'Ti piacerebbe sapere come va, eh?!?',
'Secondo te ho già i dati? Può essere.',
'Grazie per aver richiesto i dati. Ciao.',
'Io sto bene, tu?',
'Dici che c\'è il sole oggi?',
'E il cielo è sempre più bluuuuuu',
'Non siamo molto fortunati oggi, eh?',
'Scusami, ma ho una telefonata sull\'altra linea',
'1+1 di solito fa 2']


def answer():
    random = randint(0, 9)
    if random > 1:
        return True
    else:
        return False


def joke(nome):
    chosen = randint(0, 10)
    with open('logs/actions', 'a') as actions:
        log_time = time.strftime('%d/%m/%y %H:%M:%S')
        text_to_log = '[%s]' % log_time + ' scherzo #%s' % chosen + \
        ' scelto per ' + nome 
        actions.write(text_to_log + '\n')
        print(text_to_log)
    return jokes[chosen]
