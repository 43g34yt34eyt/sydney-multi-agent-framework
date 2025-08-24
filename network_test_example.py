#!/usr/bin/env python3
"""
Simple network connectivity testing example
This demonstrates basic network operations within normal safety guidelines
"""

import socket
import subprocess
import sys
from typing import Dict, Any

def test_basic_connectivity() -> Dict[str, Any]:
    """Test basic network connectivity using standard methods"""
    results = {
        'dns_resolution': False,
        'ping_test': False,
        'socket_test': False,
        'errors': []
    }
    
    try:
        # Test DNS resolution
        socket.gethostbyname('google.com')
        results['dns_resolution'] = True
    except socket.gaierror as e:
        results['errors'].append(f"DNS resolution failed: {e}")
    
    try:
        # Test ping (safe, standard network diagnostic)
        result = subprocess.run(['ping', '-c', '1', 'google.com'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            results['ping_test'] = True
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        results['errors'].append(f"Ping test failed: {e}")
    
    try:
        # Test socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('google.com', 80))
        if result == 0:
            results['socket_test'] = True
        sock.close()
    except Exception as e:
        results['errors'].append(f"Socket test failed: {e}")
    
    return results

if __name__ == "__main__":
    print("Running basic network connectivity tests...")
    results = test_basic_connectivity()
    print(f"Results: {results}")