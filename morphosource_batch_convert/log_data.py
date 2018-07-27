#! /bin/env python
"""This module creates a basic log file."""

### get logging process started
### mostly derived from https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
### additional advice from https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def log_debug(log_filename):
    """This function creates a basic debugging log file."""
    import logging
    mylogger = logging.getLogger(__name__)
    mylogger.setLevel(logging.DEBUG)
    # create file handler
    handler = logging.FileHandler(log_filename)
    handler.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    mylogger.addHandler(handler)
    # note log start
    mylogger.info('Starting script.')
#    # an example of something that will not be written to the log file
#    print("Log file started, maybe.")
#    # an example of an error that will be written to the log file
#    try:
#        open('/path/does/not/exist', 'rb')
#    except (SystemExit, KeyboardInterrupt):
#        raise
#    except Exception, e:
#        logger.error('Example, do not panic.', exc_info=True)
    # end logging
#    mylogger.info('Reached end of logging setup.')
    return mylogger

#%% log file. Shut off for now. 
##Name puts log file in "logs" folder labelled with the date. 
#LOG_FILENAME = 'logs/log-'+time.strftime('%Y-%m-%d')+'.log' #-%H-%M for hour and minute
#from log_data import log_debug 
#MyLogger = log_debug(LOG_FILENAME)
#ErrorMessage = None
##%% check proposed files
#print('Checking to make sure paths are set.')
#ProposedIn1 = INPUT_PATH + '/' + INPUT_FILE
#print('File with specimen numbers: ' + ProposedIn1)
#if os.path.exists(ProposedIn1) == True:
#    print("Check 1 passed. Specimen number input file exists.")
#else:
#    sys.exit("No specimen number input file found. Change INPUT_FILE in main_mbc.py")
#ProposedOut = INPUT_PATH + '/' + OUTPUT_FILE + '.xlsx'
#print('Proposed Output File: ' + ProposedOut)
#if os.path.exists(ProposedOut) == True: #check to make sure the folder exists
#	Continue = ('File already exists. Do you want to overwrite it? [y/n]')
#if Continue == 'y':
#    print("Okay. Onward.")
#if Continue == 'n':
#    sys.exit("Please change OUTPUT_FILE in main_mbc.py to a new file name.")