import os
import socket
from tkinter import *

window = Tk()

# IP, Port
host_ip = Entry(window, width=20)
host_start_port = Entry(window, width=20)
host_end_port = Entry(window, width=20)

# Progress Label
progress_port_scan_label = Label(window, text="스캔 정보를 입력해주세요.")

def start_scan():
    # 열려있는 포트 목록
    open_ports = []
    
    # 각 포트에 대해 시도
    for port in range(int(host_start_port.get()), int(host_end_port.get()) + 1):

        progress_port_scan_label.config(text="Port in progress: "+str(port))
        window.update()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # 연결 시도에 대한 타임아웃 설정
        result = sock.connect_ex((host_ip.get(), port))

        if result == 0:
            open_ports.append(port)  # 포트가 열려 있으면 목록에 추가

        sock.close()

    progress_port_scan_label.config(text='완료!')
    window.update()

    # Log
    log_directory = os.path.dirname(os.path.realpath(__file__)) + "\\log"

    if (os.path.exists(log_directory) == False):
        os.mkdir(log_directory)

    log_full_path = log_directory + "\\scan_log(" + host_ip.get() + ", " + host_start_port.get() + "~" + host_end_port.get() + ").txt"

    with open(log_full_path, 'w') as file:
        file.write("*** Open Port List ***\n")

        for port in open_ports:
            file.write(str(port))
            file.write('\n')

def init_ui():
    window.title("Port Scanner")
    window.geometry("320x200+100+100")
    window.resizable(False, False)

    start_position_row = 5
    position_row_offset = 5
    start_position_cul = 10
    position_cul_offset = 10
    
    # IP
    host_ip_label = Label(window, text="IP")
    host_ip_label.grid(column=start_position_cul, row=start_position_row)

    host_ip.grid(column=start_position_cul+position_cul_offset, row=start_position_row)

    # Start Port Start
    host_start_port_label = Label(window, text="Start Port")
    host_start_port_label.grid(column=start_position_cul, row=start_position_row+position_row_offset)

    host_start_port.grid(column=start_position_cul+position_cul_offset, row=start_position_row+position_row_offset)

    # End Port End
    host_start_port_label = Label(window, text="End Port")
    host_start_port_label.grid(column=start_position_cul, row=start_position_row+(position_row_offset*2))
      
    host_end_port.grid(column=start_position_cul+position_cul_offset, row=start_position_row+(position_row_offset*2))

    # Start Button
    start_scan_button = Button(window, text="Scan", command=start_scan)
    start_scan_button.grid(column=start_position_cul, row=start_position_row+(position_row_offset*3))

    # Progress Port Scan Label
    progress_port_scan_label.grid(column=start_position_cul, row=start_position_row+(position_row_offset*4))


if __name__ == "__main__": 
    init_ui()

    window.mainloop()