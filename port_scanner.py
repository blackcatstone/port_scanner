import os, asyncio
import tkinter as tk

async def scan_port(ip, port):
    """ 비동기적으로 특정 IP와 포트에 대해 연결을 시도합니다. """
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        writer.close()
        await writer.wait_closed()
        return port, True
    except:
        return port, False

async def async_port_scanner(ip, start_port, end_port, progress_callback):
    """ 주어진 IP 주소에 대해 여러 포트를 비동기적으로 스캔합니다. """
    ports = range(start_port, end_port + 1)
    total_ports = len(ports)
    tasks = [scan_port(ip, port) for port in ports]
    open_ports = []
    completed_tasks = 0
    for future in asyncio.as_completed(tasks):
        port, is_open = await future
        completed_tasks += 1
        progress = (completed_tasks / total_ports) * 100
        progress_callback(progress, port, is_open)
        if is_open:
            open_ports.append(port)
            m = ' Port %d \t[open]' % (port,)
            log.append(m)
    return open_ports

def update_progress(progress, port, is_open):
    progress_var.set(f"Progress: {progress:.2f}%")
    window.update()

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

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    open_ports = loop.run_until_complete(async_port_scanner(ip, start_port, end_port, update_progress))
    result_var.set(f"Open ports on {ip}: {open_ports}")
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
    global ip_var, start_port_var, end_port_var, progress_var, result_var

    window.title("Port Scanner")
    window.geometry("400x320+550+200")
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

    # Buttons
    scan_button = tk.Button(window, text="Start Scan", command=start_scan)
    scan_button.place(x = 16, y = 260, width = 170)
    save_button = tk.Button(window, text="Scan Result", command=save_scan)
    save_button.place(x = 210, y = 260, width = 170)

    # Progress and Result Labels
    progress_var = tk.StringVar()
    progress_label = tk.Label(window, textvariable=progress_var)
    progress_label.place(x = 30, y = 192)

    result_var = tk.StringVar()
    result_label = tk.Label(window, textvariable=result_var)
    result_label.place(x = 30, y = 220)

if __name__ == "__main__":
    window = tk.Tk()
    init_ui(window)
    window.mainloop()