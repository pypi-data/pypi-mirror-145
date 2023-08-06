# -*- coding: utf-8 -*-

import time
from ekr import EventKernel, Event

ekr = EventKernel()
ekr.assign(ekr.default_worker, 'hello')
ekr.start()



while 1:
    ekr.push(Event(dest='hello'))
    time.sleep(1)

