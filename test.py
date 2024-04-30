'''import socket
import ipaddress
import re

port_regex = re.compile("([0-9]+){1,5}-([0-9]+){1,5}")
ip_regex1 = re.compile("^\d")
ip_regex2 = re.compile("^www\.")

while True:
    ip_addr_input = input("입력하세요 :")
    try:
        ip_regex1_valid = ip_regex1.search(ip_addr_input.replace(" ",""))
        ip_regex2_valid = ip_regex2.search(ip_addr_input.replace(" ",""))
        if ip_regex1_valid:
            ip_addr = ipaddress.ip_address(ip_addr_input)
            break
        elif ip_regex2_valid:
            ip_addr = ip_addr_input
            break
    except:
        print("wrong")
while True:
    port_min = 0
    port_max = 65535
    port_range = input("포트범위를 정해주세요 : ")
    port_range_valid = port_regex.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break
    
valid_ports = []
for port in range(port_min, port_max+1):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip_addr,port))
            valid_ports.append(port)
    except:
        print("port", port, "not open")
        pass
for port in valid_ports:
    print(f"{ip_addr_input} 주소에 {port}가 연결되었습니다")'''
    

import asyncio
import socket

async def scan_port(ip, port):
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        writer.close()
        await writer.wait_closed()
        return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return port, False

async def scan_ports(ip, start_port, end_port):
    tasks = [scan_port(ip, port) for port in range(start_port, end_port + 1)]
    results = await asyncio.gather(*tasks)
    return [port for port, is_open in results if is_open]

# 사용 예
async def main():
    target_ip = '127.0.0.1'  # 대상 IP 주소
    start_port = 1
    end_port = 10000
    open_ports = await scan_ports(target_ip, start_port, end_port)
    print(f"Open ports on {target_ip}: {open_ports}")

# 이벤트 루프 실행
if __name__ == "__main__":
    asyncio.run(main())
