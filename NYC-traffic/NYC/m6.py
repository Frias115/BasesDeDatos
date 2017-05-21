#!/usr/bin/python
# -*- coding: utf-8 -*-
# 6. Calle que más tráfico aporta a Brodway por franja de hora.
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
            print fila[2] + ',',
            print fila[4] + ',',
            for data in range(7, len(firstLine) - 1):
                print fila[data] + ',',
            print fila[len(firstLine) - 1],
            print ''
