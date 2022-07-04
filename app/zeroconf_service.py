import os
import socket
from unicodedata import name
from loguru import logger
from zeroconf import IPVersion, ServiceInfo, Zeroconf

zeroconf = None
info = None


async def register_zeroconf():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    s.close()

    type = "_http._tcp.local."
    name = f"{os.getenv('DEVICE_NAME')}.{type}"
    company = os.getenv("DEVICE_COMPANY")

    port = 8000
    desc = {"url": "https://" + IPAddr + ":" + str(port), "company": company}

    info = ServiceInfo(
        type,
        name,
        addresses=[socket.inet_aton(IPAddr)],
        port=port,
        properties=desc,
        server="ash-2.local.",
    )

    zeroconf = Zeroconf()
    await zeroconf.async_register_service(info)

    zeroconf = Zeroconf(ip_version=IPVersion.All)
    logger.info("Zeroconf service started")


async def unregister_zeroconf():
    logger.info("Zeroconf service stopped")
    await zeroconf.async_unregister_service(info)
    zeroconf.close()
