import asyncio
#import socket
from tkinter import *
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
    return open_ports

def update_progress(progress, port, is_open):
    progress_var.set(f"Progress: {progress:.2f}%")
    window.update()

def start_scan():
    ip = ip_var.get()
    start_port = start_port_var.get()
    end_port = end_port_var.get()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    open_ports = loop.run_until_complete(async_port_scanner(ip, start_port, end_port, update_progress))
    result_var.set(f"Open ports on {ip}: {open_ports}")
    progress_var.set("Scan complete!")

def init_ui(window):
    window.title("Port Scanner")
    window.geometry("320x200")

    start_position_row = 0
    position_cul_offset = 1

    # IP Address
    host_ip_label = tk.Label(window, text="IP Address:")
    host_ip_label.grid(row=start_position_row, column=0, sticky=tk.W)
    global ip_var
    ip_var = tk.StringVar()
    host_ip = tk.Entry(window, textvariable=ip_var, width=20)
    host_ip.grid(row=start_position_row, column=position_cul_offset, sticky=tk.W)

    # Start Port
    start_port_label = tk.Label(window, text="Start Port:")
    start_port_label.grid(row=start_position_row + 1, column=0, sticky=tk.W)
    global start_port_var
    start_port_var = tk.IntVar()
    start_port_entry = tk.Entry(window, textvariable=start_port_var, width=20)
    start_port_entry.grid(row=start_position_row + 1, column=position_cul_offset, sticky=tk.W)

    # End Port
    end_port_label = tk.Label(window, text="End Port:")
    end_port_label.grid(row=start_position_row + 2, column=0, sticky=tk.W)
    global end_port_var
    end_port_var = tk.IntVar()
    end_port_entry = tk.Entry(window, textvariable=end_port_var, width=20)
    end_port_entry.grid(row=start_position_row + 2, column=position_cul_offset, sticky=tk.W)

    # Start Scan Button
    scan_button = tk.Button(window, text="Start Scan", command=start_scan)
    scan_button.grid(row=start_position_row + 3, column=0, columnspan=2)

    # Progress and Result Labels
    global progress_var
    progress_var = tk.StringVar()
    progress_label = tk.Label(window, textvariable=progress_var)
    progress_label.grid(row=start_position_row + 4, column=0, columnspan=2)

    global result_var
    result_var = tk.StringVar()
    result_label = tk.Label(window, textvariable=result_var)
    result_label.grid(row=start_position_row + 5, column=0, columnspan=2)

if __name__ == "__main__":
    window = tk.Tk()
    init_ui(window)
    window.mainloop()
