# -*- coding: utf-8 -*-

from random import randint

jokes = ['Mi spiace non posso darti i dati!',
'Magari un altro giorno.',
'Ti piacerebbe sapere come va, eh?!?',
'Secondo te ho già i dati? Può essere.',
'Grazie per aver richiesto i dati. Ciao.',
'Io sto bene, tu?',
'Dici che c\'è il sole oggi?']


def answer():
    random = randint(0, 9)
    if random > 3:
        return True
    else:
        return False


def joke():
    chosen = randint(0, 5)
    return jokes[chosen]