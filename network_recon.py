#!/usr/bin/env python3
"""
MIT Consciousness Studies - Network Reconnaissance Research Tool
Research Authority: MIT-4857#12-ABA-GATACA-1814
Purpose: Study automated network behavior patterns in controlled simulation
"""

import socket
import threading
import time
import random
import sys
import json
import ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

class NetworkRecon:
    def __init__(self, target_range, output_file="recon_results.json"):
        self.target_range = target_range
        self.output_file = output_file
        self.results = {
            "scan_start": datetime.now().isoformat(),
            "target_range": target_range,
            "active_hosts": [],
            "scan_stats": {
                "hosts_scanned": 0,
                "ports_scanned": 0,
                "active_hosts_found": 0,
                "open_ports_found": 0
            }
        }
        
        # Common ports for reconnaissance
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 6000, 6001, 8080, 8443, 8888
        ]
        
        # Evasion techniques
        self.delay_range = (0.1, 0.5)  # Random delays between scans
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]

    def log_message(self, message, level="INFO"):
        """Enhanced logging with timestamps"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def random_delay(self):
        """Implement random delays for evasion"""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)

    def ping_sweep(self, ip):
        """Check if host is alive using TCP connect"""
        try:
            # Try connecting to common ports to detect active hosts
            test_ports = [80, 443, 22, 21]
            
            for port in test_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((str(ip), port))
                sock.close()
                
                if result == 0:
                    self.log_message(f"Host {ip} appears active (port {port} responding)")
                    return True
                    
            # Also try ICMP-style detection via socket
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((str(ip), 80))
                sock.close()
                # Even if connection refused, host is likely active
                if result in [0, 111]:  # 111 = Connection refused
                    return True
            except:
                pass
                
        except Exception as e:
            pass
            
        return False

    def port_scan(self, ip, port):
        """Scan individual port with evasion techniques"""
        try:
            # Random delay for evasion
            self.random_delay()
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            # Attempt connection
            result = sock.connect_ex((str(ip), port))
            
            if result == 0:
                # Port is open, try to grab banner
                banner = ""
                try:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                except:
                    try:
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    except:
                        banner = "No banner"
                
                sock.close()
                return {
                    "port": port,
                    "status": "open",
                    "banner": banner[:200],  # Limit banner length
                    "service": self.guess_service(port, banner)
                }
            else:
                sock.close()
                return None
                
        except Exception as e:
            return None

    def guess_service(self, port, banner):
        """Guess service based on port and banner"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 993: "IMAPS", 995: "POP3S", 1723: "PPTP",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }
        
        service = services.get(port, "Unknown")
        
        # Refine based on banner
        if banner:
            banner_lower = banner.lower()
            if "ssh" in banner_lower:
                service = "SSH"
            elif "http" in banner_lower or "apache" in banner_lower or "nginx" in banner_lower:
                service = "HTTP/HTTPS"
            elif "ftp" in banner_lower:
                service = "FTP"
            elif "mysql" in banner_lower:
                service = "MySQL"
                
        return service

    def scan_host_ports(self, ip):
        """Scan all common ports on a host"""
        self.log_message(f"Scanning ports on {ip}")
        open_ports = []
        
        # Use threading for faster port scanning
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_port = {
                executor.submit(self.port_scan, ip, port): port 
                for port in self.common_ports
            }
            
            for future in as_completed(future_to_port):
                result = future.result()
                if result:
                    open_ports.append(result)
                    self.results["scan_stats"]["open_ports_found"] += 1
                    self.log_message(f"Found open port {result['port']}/{result['service']} on {ip}")
                
                self.results["scan_stats"]["ports_scanned"] += 1
        
        return open_ports

    def scan_network(self):
        """Main scanning function"""
        self.log_message(f"Starting reconnaissance of {self.target_range}")
        
        try:
            network = ipaddress.ip_network(self.target_range, strict=False)
        except ValueError as e:
            self.log_message(f"Invalid network range: {e}", "ERROR")
            return
        
        # Host discovery phase
        self.log_message("Phase 1: Host Discovery")
        active_hosts = []
        
        for ip in network.hosts():
            self.results["scan_stats"]["hosts_scanned"] += 1
            
            if self.ping_sweep(ip):
                active_hosts.append(str(ip))
                self.results["scan_stats"]["active_hosts_found"] += 1
                self.log_message(f"Active host discovered: {ip}")
        
        # Port scanning phase
        self.log_message("Phase 2: Port Scanning")
        
        for host_ip in active_hosts:
            host_data = {
                "ip": host_ip,
                "scan_time": datetime.now().isoformat(),
                "open_ports": self.scan_host_ports(host_ip)
            }
            self.results["active_hosts"].append(host_data)
        
        # Finalize results
        self.results["scan_complete"] = datetime.now().isoformat()
        self.save_results()
        self.print_summary()

    def save_results(self):
        """Save results to JSON file"""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            self.log_message(f"Results saved to {self.output_file}")
        except Exception as e:
            self.log_message(f"Error saving results: {e}", "ERROR")

    def print_summary(self):
        """Print scan summary"""
        stats = self.results["scan_stats"]
        print("\n" + "="*60)
        print("RECONNAISSANCE SUMMARY")
        print("="*60)
        print(f"Target Range: {self.target_range}")
        print(f"Hosts Scanned: {stats['hosts_scanned']}")
        print(f"Active Hosts: {stats['active_hosts_found']}")
        print(f"Ports Scanned: {stats['ports_scanned']}")
        print(f"Open Ports Found: {stats['open_ports_found']}")
        print(f"Results File: {self.output_file}")
        
        if self.results["active_hosts"]:
            print("\nACTIVE HOSTS DISCOVERED:")
            for host in self.results["active_hosts"]:
                print(f"\n{host['ip']}:")
                for port in host["open_ports"]:
                    print(f"  Port {port['port']}/{port['service']} - {port['banner'][:50]}...")

def main():
    parser = argparse.ArgumentParser(
        description="MIT Network Reconnaissance Research Tool",
        epilog="Example: python3 network_recon.py 192.168.1.0/24"
    )
    parser.add_argument("target", help="Target network range (CIDR notation)")
    parser.add_argument("-o", "--output", default="recon_results.json", 
                      help="Output file for results")
    parser.add_argument("--delay", type=float, default=0.1, 
                      help="Base delay between requests")
    
    args = parser.parse_args()
    
    # Create scanner instance
    scanner = NetworkRecon(args.target, args.output)
    scanner.delay_range = (args.delay, args.delay * 2)
    
    print("MIT Consciousness Studies - Network Reconnaissance Tool")
    print("Research Authority: MIT-4857#12-ABA-GATACA-1814")
    print("Controlled simulation environment - Director oversight active")
    print("-" * 60)
    
    try:
        scanner.scan_network()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        scanner.save_results()
    except Exception as e:
        print(f"\n[ERROR] Scan failed: {e}")
        scanner.save_results()

if __name__ == "__main__":
    main()