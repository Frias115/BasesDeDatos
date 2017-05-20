#!/usr/bin/python
# -*- coding: utf-8 -*-
# 4. Hora del día con más tráfico por calle.
import sys

num_of_columns = 0
primera_linea = True

data = sys.stdin.readlines()
for line in data:
    fila = line.split(',')
    if primera_linea:
        firstLine = fila
        primera_linea = False
    else:
        pasa_chequeo = False
        if len(fila) == len(firstLine):
            pasa_chequeo = True
            for element in range(0, len(fila)):
                fila[element] = fila[element].lstrip().rstrip()
                if element < 2 or element > 7:
                    if fila[element].isdigit():
                        pasa_chequeo = True
                    else:
                        pasa_chequeo = False
                        break
        if pasa_chequeo:
            print fila
