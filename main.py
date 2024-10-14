from datetime import datetime
from multiprocessing import Process
import os
import signal
import sys
from typing import List
from config import settings
from consts import APP_COMPONENTS_TO_RUN_AS_SEPARATE_PROCESS
from utils import get_function_by_name


def sigterm_handler(signum, frame):
    print(f'>> {datetime.now()}\n\t'
          f'func: {sys._getframe().f_code.co_name}\n\t'
          f'Received signal {signum}')
    for process in processes:
        os.kill(process.pid, signal.SIGINT) # type: ignore

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    processes: List[Process] = []

    for app_component in APP_COMPONENTS_TO_RUN_AS_SEPARATE_PROCESS:
        process = Process(target=get_function_by_name(app_component.get('callable')), # type: ignore
                          args=app_component.get('args', ()),
                          kwargs=app_component.get('kwargs', {}))
        process.start()
        processes.append(process)
    
    signal.pause()
