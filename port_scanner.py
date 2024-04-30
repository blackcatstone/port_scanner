import socket

def scan_ports(host, start_port, end_port):
    # 열려있는 포트 목록
    open_ports = []

    # 각 포트에 대해 시도
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # 연결 시도에 대한 타임아웃 설정
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)  # 포트가 열려 있으면 목록에 추가
        sock.close()

    return open_ports

# 사용 예시
hostip = input("스캔할 IP 주소를 입력하세요: ")  # 스캔할 대상 IP
if __name__ == "__main__": 
    start_port = 1
    end_port = 1004
    open_ports = scan_ports(hostip, start_port, end_port)

    if open_ports:
        print(f"열려있는 포트 목록: {hostip}: {open_ports}")
    else:
        print(f"열려있지 않는 포트 목록: {hostip}.")

