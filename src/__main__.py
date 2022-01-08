from .pignet import *

logger.info("## Starting full capture system")
aio.run(maintain_mqtt(pignet))
