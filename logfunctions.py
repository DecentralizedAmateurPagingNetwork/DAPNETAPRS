import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.DEBUG):
	handler = logging.FileHandler(log_file)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)

	return(logger)

# main logger
logger = setup_logger('main_logger', '/var/log/dapaprs_main.log')

# dapnet logger
dapnet_logger = setup_logger('dapnet_logger', '/var/log/dapaprs_dapnet.log')

# aprs logger
aprs_logger = setup_logger('aprs_logger','/var/log/dapaprs_aprs.log')
