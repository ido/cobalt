gcc -o test -Wl,-rpath,/bgsys/drivers/ppcfloor/hlcs/lib:/home/richp/cobalt_runjob_plugin  -L/bgsys/drivers/ppcfloor/hlcs/lib -lbgsched -L/home/richp/cobalt_runjob_plugin -lcorjplugin -I/home/richp/cobalt_runjob_plugin -I/bgsys/drivers/ppcfloor/hlcs/include main.cpp
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
