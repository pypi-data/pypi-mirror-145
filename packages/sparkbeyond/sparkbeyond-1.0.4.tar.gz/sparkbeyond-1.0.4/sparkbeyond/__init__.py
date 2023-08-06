import logging

logging.basicConfig(level=logging.INFO, format=f'%(message)s')
logger = logging.getLogger()
logger.warning('\n'
               'WARNING\n'
               '=======\n'
               'This is a dummy placeholder for the SparkBeyond Python SDK. \n'
               'The actual SDK can be installed directly from your Discovery Platform server.\n'
               'For further information, please contact support@sparkbeyond.com\n'
               )
