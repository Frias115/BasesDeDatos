#!/usr/bin/python
# -*- coding: utf-8 -*-
# 4. Hora del dia con mas trafico por calle.

import sys

# TODO: PREGUNTAR SI TAMBIEN HAY QUE TENER EN CUENTA DATE

data = sys.stdin.readlines()
for line in data:
    fila = line.split(', ')
    fila[-1] = fila[-1].rstrip()
    print fila