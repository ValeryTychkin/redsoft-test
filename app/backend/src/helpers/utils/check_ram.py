import datetime
import json
from ctypes import c_char_p
from multiprocessing import Process, Manager

import psutil


class RamStatisticsDaemon(Process):
    """
    Класс процесса по получению информации по RAM памяти
    """
    def __init__(self):
        super().__init__(daemon=True)
        manager = Manager()
        self.result = manager.Value(c_char_p, "")

    def run(self):
        cur_mem = psutil.virtual_memory()
        result = {k: getattr(cur_mem, k) for k in cur_mem._fields}
        result['date'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        self.result.value = json.dumps(result)

    def get_result(self) -> dict:
        return json.loads(self.result.value)
