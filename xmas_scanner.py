import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from scapy.layers.inet import IP, TCP, ICMP
from scapy.all import *

async def xmas_scanner(ip, port):
    response = sr1(IP(dst=ip) / TCP(sport=RandShort(), dport=port, flags="FPU"), timeout=1)
    
    if response is None:
        return port, "Open or Filtered"
    else:
        if response.haslayer(TCP):
            if response.getlayer(TCP).flags == 0x04:
                return port, "Closed"
        elif response.haslayer(ICMP):
            if int(response.getlayer(ICMP).type) == 3 and int(response.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                return port, "Filtered"