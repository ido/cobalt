#!/usr/bin/pytho#!/usr/bin/python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import pybgsched
from pybgsched import getComputeHardware
pybgsched.init("../bg.properties")
h = getComputeHardware()
m = h.getMidplane('R00-M0')
m.getState()
m.getInUse()
str(m)
nb = m.getNodeBoard(3)
str(nb)
nb.getQuadrant()
nbv = pybgsched.getNodeBoards('R00-M0')


print(nbv)
