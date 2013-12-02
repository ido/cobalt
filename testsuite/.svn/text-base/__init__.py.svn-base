import logging

def setup ():
    if not globals().has_key("DISABLE_LOGGING") or globals()["DISABLE_LOGGING"] == True:
        logging.disable(999)

def teardown ():
    logging.disable(0)
