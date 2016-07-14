# coding=utf-8
# Copyright (c) 2016 - Dmall Shanghai-Tech <sh-it@dmall.com>

from __future__ import print_function
from builtins import range
from airflow.operators import PythonOperator, BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta
import conf

SOURCE_ENV = conf.FRAPPE_DIR + '/env/bin/activate'
RUN_DIR = conf.FRAPPE_DIR + '/sites'
IMPORT_MAIN_ITEM_DATA_PY_PATH = \
    conf.AIRFLOW_DIR + '/dags/sap_sync_verify/verify_store_item.py'
SYNC_DATE = conf.DATE_TO_SYNC if not conf.DEFAULT_SYN_DATE else datetime.now().strftime('%Y%m%d')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2016, 6, 24),
    'email': ['xxx@dmall.com',],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    dag_id='sap_sync_verify',
    default_args=default_args,
    schedule_interval="@daily")


templated_command = """
    source {{ params.source_path }}
    cd {{ params.run_dir }}
    pwd
    echo start
    python {{params.py_path}}
    echo end
"""

verify_store_item = BashOperator(
    task_id='import_merchandise_data',
    bash_command=templated_command,
    params={
        'source_path': SOURCE_ENV,
        'run_dir': RUN_DIR,
        'py_path': IMPORT_MAIN_ITEM_DATA_PY_PATH,
        'xml_dir': conf.LOCAL_DATA_DIR + '/%s/' % SYNC_DATE
    },
    dag=dag)