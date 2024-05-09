import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

import asyncio
from scapy.all import IP, TCP, sr1, ICMP, RandShort

async def null_scanner(ip, port):
    """비동기로 특정 IP와 포트에 대해 NULL 스캔."""
    response = sr1(IP(dst=ip) / TCP(sport=RandShort(), dport=port, flags=""), timeout=1)
     
    if response is None:
        return port, "Open or Filtered"
    else:
        if response.haslayer(TCP):
            if response.getlayer(TCP).flags == 0x04:
                return port, "Closed"
        elif response.haslayer(ICMP):
            if int(response.getlayer(ICMP).type) == 3 and int(response.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                return port, "Filtered"
