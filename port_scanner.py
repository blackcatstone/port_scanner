import os
from connect_scanner import *
from xmas_scanner import *

def update_progress(progress):
    progress_var.set(f"Progress: {progress:.2f}%")
    window.update()

async def async_port_scanner(ip, start_port, end_port, port_scanner_callback, progress_callback):
    ports = range(start_port, end_port + 1)
    total_ports = len(ports)
    tasks = [port_scanner_callback(ip, port) for port in ports]
    open_ports = []
    completed_tasks = 0
    for future in asyncio.as_completed(tasks):
        port, is_open = await future
        completed_tasks += 1
        progress = (completed_tasks / total_ports) * 100
        progress_callback(progress)
        if is_open:
            open_ports.append(port)
    return open_ports

def start_scan():
    ip = ip_var.get()
    start_port = start_port_var.get()
    end_port = end_port_var.get()

    # log
    global log
    log = [] # clear the log
    log.extend([
        '*** Open Port List ***\n',
        f' IP:     \t{ip}',
        f' Ports:   \t[ {start_port} ~ {end_port} ]\n'
    ])

    result_list_box.delete(0, "end")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    open_ports = []
    selected_value = selected_radio_value.get()

    if selected_value == 1:   # TCP Connect
        open_ports = loop.run_until_complete(async_port_scanner(ip, start_port, end_port, tcp_connect_scanner, update_progress))
    # elif selected_value == 2:
    #     tcp ack scan
    # elif selected_value == 3:
    #     null scan
    elif selected_value == 4: # Xmas
        open_ports = loop.run_until_complete(async_port_scanner(ip, start_port, end_port, xmas_scanner, update_progress))

    for port in open_ports:
        log.append(' Port %d \t[open]' % (port,))
        result_list_box.insert("end", port)
    
    progress_var.set("Scan complete!")

def save_scan():
    ip = ip_var.get()   
    start_port = start_port_var.get()
    end_port = end_port_var.get()

    # save the log
    log_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log")

    if (os.path.exists(log_directory) == False):
        os.mkdir(log_directory)

    log_full_path = os.path.join(log_directory, "scan_log(" + str(ip) + ", " + str(start_port) + "~" + str(end_port) + ").txt")

    with open(log_full_path, 'w') as file:
        file.write('\n'.join(log)) 

def init_ui(window):
    # 전역 변수 선언
    global ip_var, start_port_var, end_port_var, selected_radio_value, progress_var, result_list_box

    window.title("Port Scanner")
    window.geometry("400x360+550+200")
    window.resizable(False, False)

    # 안내 문구
    L11 = tk.Label(window, text = "스캔 정보를 입력하세요.",  font=("Helvetica", 20))
    L11.place(x = 20, y = 20)

    # IP Address
    host_ip_label = tk.Label(window, text="IP Address:")
    host_ip_label.place(x = 30, y = 70)
    ip_var = tk.StringVar()
    host_ip = tk.Entry(window, textvariable=ip_var, width=20)
    host_ip.place(x = 180, y = 70)

    # Start Port
    start_port_label = tk.Label(window, text="Start Port:")
    start_port_label.place(x = 30, y = 110)
    start_port_var = tk.IntVar()
    start_port_entry = tk.Entry(window, textvariable=start_port_var, width=20)
    start_port_entry.place(x = 180, y = 110)

    # End Port
    end_port_label = tk.Label(window, text="End Port:")
    end_port_label.place(x = 30, y = 150)
    end_port_var = tk.IntVar()
    end_port_entry = tk.Entry(window, textvariable=end_port_var, width=20)
    end_port_entry.place(x = 180, y = 150)

    # Radio Button
    selected_radio_value = tk.IntVar()
    tcp_connect_radio_button = tk.Radiobutton(window, text="TCP Conn", value=1, variable=selected_radio_value)
    tcp_connect_radio_button.place(x=16, y=200)
    tcp_ack_radio_button = tk.Radiobutton(window, text="TCP Ack", value=2, variable=selected_radio_value)
    tcp_ack_radio_button.place(x=106, y=200)
    null_radio_button = tk.Radiobutton(window, text="Null", value=3, variable=selected_radio_value)
    null_radio_button.place(x=196, y=200)
    xmas_radio_button = tk.Radiobutton(window, text="Xmas", value=4, variable=selected_radio_value)
    xmas_radio_button.place(x=286, y=200)

    # Buttons
    scan_button = tk.Button(window, text="Scan", command=start_scan)
    scan_button.place(x = 16, y = 230, width = 170)
    save_button = tk.Button(window, text="Scan Result", command=save_scan)
    save_button.place(x = 200, y = 230, width = 170)

    # Progress and Result Labels
    progress_var = tk.StringVar()
    progress_label = tk.Label(window, textvariable=progress_var)
    progress_label.place(x = 30, y = 170)

    # Result List Box
    result_frame = tk.Frame(window)
    result_frame.place(x = 16, y = 260, width = 350, height = 80)
    result_list_box = tk.Listbox(result_frame, width=100, height=6)
    result_list_box.place(x=0, y=0)
    result_scroll_bar = tk.Scrollbar(result_frame)
    result_scroll_bar.pack(side="right", fill="y")
    result_list_box.config(yscrollcommand=result_scroll_bar.set)
    result_scroll_bar.config(command=result_list_box.yview)

if __name__ == "__main__":
    window = tk.Tk()
    init_ui(window)
    window.mainloop()