#frappe dir and site name
SITE_NAME = 'sjerp.dmall.io'
FRAPPE_DIR = '/home/ubuntu/frappe-bench'
#airflow dir
AIRFLOW_DIR = '/home/ubuntu/airflow'
#lcoal data dir
LOCAL_DATA_DIR = '/home/ubuntu/data'

#sync sap date
DEFAULT_SYN_DATE = True
DATE_TO_SYNC = ''

import logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    )
