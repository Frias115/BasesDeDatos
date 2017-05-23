#!/usr/bin/python
# -*- coding: utf-8 -*-
# 7. Diferencia entre el trafico total de entrada a Brodway frente al de salida.
import sys

num_of_columns = 0
primera_linea = True

data = sys.stdin.readlines()
for line in data:
    fila = line.split(',')
    # Parsing file attributes
    if primera_linea:
        firstLine = fila
        primera_linea = False
    else:
        pasa_chequeo = False
        # If the row's length is the same as the first line's,continue
        if len(fila) == len(firstLine):
            pasa_chequeo = True
            # Remove first and last spaces of every element
            for element in range(0, len(fila)):
                fila[element] = fila[element].lstrip().rstrip()
                # Check if elements ranging from 2 to 7 are digits
                if element < 2 or element > 7:
                    if fila[element].isdigit():
                        pasa_chequeo = True
                    else:
                        pasa_chequeo = False
                        break
        # If all of the above conditions are met, proceed to print data


        if pasa_chequeo:
            # Only printing rows that go to Broadway and come from Broadway
            if fila[3] == "BROADWAY" or fila[4] == 'BROADWAY':
                # Prining street that goes to broadway
                print fila[3] + ',',
                # Prining street that comes from broadway
                print fila[4] + ',',
                # Print data until last position
                for data in range(7, len(firstLine) - 1):
                    print fila[data] + ',',
                # Print last position
                print fila[len(firstLine) - 1],
                print ''
