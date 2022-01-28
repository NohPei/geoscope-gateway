from .uart_sync import *
from .RBIS_UDP import *

tasks = set()

tasks.add(serialMicrosLoop())
tasks.add(RBIS_loop())

aio.run(aio.gather(*tasks))
