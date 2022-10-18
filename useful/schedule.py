import time
from multiprocessing.context import Process

import schedule

from useful.vip_checker import check_vip


def try_check_vip():
    schedule.every().day.at("00:00").do(check_vip)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_timer_process():
    process = Process(target=try_check_vip, args=())
    process.start()
