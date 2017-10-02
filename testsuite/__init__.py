import logging
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

def setup ():
    if not globals().has_key("DISABLE_LOGGING") or globals()["DISABLE_LOGGING"] == True:
        logging.disable(999)

def teardown ():
    logging.disable(0)
