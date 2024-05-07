import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

import asyncio
from scapy.all import IP, TCP, sr1, RandShort

async def null_scanner(ip, port):
    """비동기로 특정 IP와 포트에 대해 NULL 스캔."""
    response = sr1(IP(dst=ip) / TCP(sport=RandShort(), dport=port, flags=""), timeout=1)
     
    if response is None:
        return port, True  # 필터링 또는 열려 있음
    elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14:
        return port, False  # 닫혀 있음
    else:
        return port, True  # 필터링 또는 열려 있음