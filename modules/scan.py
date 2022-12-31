from concurrent.futures import ThreadPoolExecutor
import json
import os
import platform
import psutil
from socket import AF_INET, SOCK_STREAM, socket
from scapy.all import ARP, Ether, ICMP, IP, sr1, srp


class NetworkScanner:
    def __init__(self, target_network):
        self.target_network = target_network

    def host_discovery(self):
        """Performs a network scan by sending ARP requests range of IP addresses."""
        ips = []
        ans, unans = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.target_network), timeout=5
        )
        for sent, received in ans:
            ips.append(received.psrc)
        return ips

    def test_port_number(self, host, port):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.settimeout(3)
            try:
                sock.connect((host, port))
                return True
            except:
                return False

    def port_scan(self, host, ports):
        """Performs a port scan"""
        poorten = []
        with ThreadPoolExecutor(len(ports)) as executor:
            results = executor.map(self.test_port_number, [
                                   host] * len(ports), ports)
            for port, is_open in zip(ports, results):
                if is_open:
                    poorten.append(port)
            return poorten

    def os_detection(self, target):
        """Performs a OS detection by sending a TCP SYN packet to port 80."""

        res = sr1(IP(dst=target) / ICMP(id=100), timeout=5)
        if res:
            if IP in res:
                ttl = res.getlayer(IP).ttl
                if ttl == 64:
                    os = "Linux"
                elif ttl == 128:
                    os = "Windows"
                else:
                    os = "Other"
                return os
            else:
                return "Not found"
        else:
            return "Not found"


class Localhost:
    def get_system_name(self):
        system_name = platform.system()
        return system_name

    def get_hostname(self):
        hostname = platform.node()
        return hostname

    def get_username(self):
        os_name = platform.system()
        if os_name == "Windows":
            user_name = os.getlogin()
        else:
            user_name = os.uname().username
        return user_name

    def get_cpu_usage(self):
        cpu_usage = psutil.cpu_percent()
        return cpu_usage

    def get_memory_usage(self):
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.used / 1024**2
        return memory_usage

    def get_network_usage(self):
        network_info = psutil.net_io_counters()
        bytes_sent = network_info.bytes_sent
        bytes_received = network_info.bytes_recv
        return bytes_sent, bytes_received

    def get_disk_usage(self):
        disk_info = psutil.disk_usage("/")
        disk_usage = disk_info.used / 1024**3
        return disk_usage


def run():
    results = []

    network_scanner = NetworkScanner("192.168.0.0/24")
    hosts = network_scanner.host_discovery()
    for index, host in enumerate(hosts):
        ports = network_scanner.port_scan(str(host), range(1024))
        os = network_scanner.os_detection(host)
        res = {f"Host{index}": {"IP": host, "Open ports": ports, "OS": os}}
        results.append(res)

    localhost = Localhost()
    system_name = localhost.get_system_name()
    hostname = localhost.get_hostname()
    username = localhost.get_username()
    cpu_usage = localhost.get_cpu_usage()
    memory_usage = localhost.get_memory_usage()
    bytes_sent, bytes_received = localhost.get_network_usage()
    disk_usage = localhost.get_disk_usage()

    res = {
        "Localhost": {
            "System name": system_name,
            "Hostname": hostname,
            "Username": username,
            "CPU usage (%)": cpu_usage,
            "Memory usage (MB)": memory_usage,
            "Network usage": {
                "Bytes sent": bytes_sent,
                "Bytes received": bytes_received,
            },
            "Disk usage (GB)": disk_usage,
        }
    }
    results.append(res)
    data = json.dumps(results)
    return data
