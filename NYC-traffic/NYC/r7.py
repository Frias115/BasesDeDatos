#!/usr/bin/python
# -*- coding: utf-8 -*-
# 7. Diferencia entre el trafico total de entrada a Brodway frente al de salida.

import sys

data = sys.stdin.readlines()
for line in data:
    fila = line.split(', ')
    fila[-1] = fila[-1].rstrip()
    print fila