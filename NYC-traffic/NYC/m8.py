#!/usr/bin/python
# 8. Sentido de cada calle con mas trafico y trafico total.
import sys

num_of_columns = 0
primera_linea = True

data = sys.stdin.readlines()
# print len(data)
for line in data:
    fila = line.split(',')
    # Imprime la primera linea
    if primera_linea:
        firstLine = fila
        primera_linea = False
        print firstLine
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
