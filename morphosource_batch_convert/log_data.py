#! /bin/env python
### get logging process started
### mostly derived from https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
### additional advice from https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/

import logging, time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler
LOG_FILENAME = 'logs/log-'+time.strftime('%Y-%m-%d')+'.log' #-%H-%M for hour and minute
handler = logging.FileHandler(LOG_FILENAME)
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# create console handler with a higher log level
chandler = logging.StreamHandler()
chandler.setLevel(logging.ERROR)

# add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(chandler)

# note log start
logger.info('Starting script.')

# an example of something that will not be written to the log file
print("Log file started, maybe.")

# an example of an error that will be written to the log file
try:
    open('/path/to/does/not/exist', 'rb')
except (SystemExit, KeyboardInterrupt):
    raise
except Exception, e:
    logger.error('Example, do not panic.', exc_info=True)

# end logging
logger.info('Reached end of logging script.')