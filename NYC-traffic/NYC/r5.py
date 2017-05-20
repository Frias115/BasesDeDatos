#!/usr/bin/python
# -*- coding: utf-8 -*-
# 5. Calle que mas trafico aporta a Brodway y trafico total aportado.

import sys

data = sys.stdin.readlines()
for line in data:
    fila = line.split(', ')
    fila[-1] = fila[-1].rstrip()
    print fila