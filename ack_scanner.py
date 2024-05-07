from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP

async def ack_scanner(ip, port):
    resp = sr1(IP(dst=ip) / TCP(dport=port, flags="A"), timeout=10.0)
    
    if resp is None:
        return port, True
    else:
        if resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x4:
                return port, False
        elif resp.haslayer(ICMP):
            if int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                return port, True