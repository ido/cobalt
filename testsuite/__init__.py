import logging

def setup ():
    logging.disable(999)

def teardown ():
    logging.disable(0)
