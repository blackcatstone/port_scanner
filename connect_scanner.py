import asyncio
import tkinter as tk

async def tcp_connect_scanner(ip, port):
    """ 비동기적으로 특정 IP와 포트에 대해 연결을 시도합니다. """
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=15.0)
        writer.close()
        await writer.wait_closed()
        return port, True
    except:
        return port, False