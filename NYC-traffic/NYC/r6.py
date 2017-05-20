#!/usr/bin/python
# -*- coding: utf-8 -*-
# 6. Calle que mas trafico aporta a Brodway por franja de hora.

import sys

data = sys.stdin.readlines()
for line in data:
    fila = line.split(', ')
    fila[-1] = fila[-1].rstrip()
    print fila