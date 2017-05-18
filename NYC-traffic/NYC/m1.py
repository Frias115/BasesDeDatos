#!/usr/bin/python
# -*- coding: utf-8 -*-
# 1. Tráfico total por calle.

import sys
import string

num_of_columns = 0
primera_linea = True

data = sys.stdin.readlines()
print len(data)
for line in data:
    fila = line.split(',')
    # Imprime la primera linea
    if primera_linea:
        firstLine = fila
        primera_linea = False
        print len(firstLine), firstLine
    else:
        pasa_chequeo = False
        if len(fila) == len(firstLine):
            pasa_chequeo = True
        for element in range(0, len(fila)):
            fila[element] = fila[element].lstrip().rstrip()
            if element < 2 or element > 7:
                if fila[element].replace('.', 'e').isdigit():
                    pasa_chequeo = True
                else:
                    pasa_chequeo = False
                    break
        if pasa_chequeo:
            print fila
