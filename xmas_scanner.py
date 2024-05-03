import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from scapy.layers.inet import IP, TCP
from scapy.all import *

async def xmas_scanner(ip, port):
    response = sr1(IP(dst=ip) / TCP(sport=RandShort(), dport=port, flags="FPU"), timeout=1)
    
    if response is None:
        return port, True
    else:
        return port, False