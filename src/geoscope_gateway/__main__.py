from .pignet import logger, aio, pignet, maintain_mqtt

logger.info("## Starting full capture system")
aio.run(maintain_mqtt(pignet))
