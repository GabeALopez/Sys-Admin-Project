import psutil
import time

def collect_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent
    bytes_recv = net.bytes_recv

    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time

    # TODO: Replace print statements with statements to send data to server

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Disk Usage: {disk_usage}%")
    print(f"Network - Bytes Sent: {bytes_sent}, Bytes Received: {bytes_recv}")
    print(f"System Uptime: {uptime:.2f} seconds")

while True:
    collect_system_stats()
    time.sleep(10)
