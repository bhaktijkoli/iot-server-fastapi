import socket
from loguru import logger
from zeroconf import IPVersion, ServiceInfo, Zeroconf

zeroconf = None
info = None


def register_zeroconf():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    s.close()

    port = 8000
    desc = {'url': 'http://' + IPAddr + ":" +
            str(port), 'company': 'KoiReader'}

    info = ServiceInfo(
        "_http._tcp.local.",
        "IoT Edge Device._http._tcp.local.",
        addresses=[socket.inet_aton(IPAddr)],
        port=port,
        properties=desc,
        server="ash-2.local.",
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    zeroconf = Zeroconf(ip_version=IPVersion.All)
    logger.info("Zeroconf service started")


def unregister_zeroconf():
    logger.info("Zeroconf service stopped")
    zeroconf.unregister_service(info)
    zeroconf.close()
