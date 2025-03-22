#!/usr/bin/env python3
"""
Simple Port Scanner - A lightweight tool to scan networks for open ports

This script provides a simple implementation of a port scanner using
socket connections to identify open ports on a network.

Author: Armin Marth
Version: 1.0.0
Last Updated: 2025-03-22
"""

import socket
import argparse
import sys


def scan_port(ip, port, timeout=0.1):
    """
    Scan a single IP and port combination.
    
    Args:
        ip (str): The IP address to scan
        port (int): The port number to scan
        timeout (float): Connection timeout in seconds
        
    Returns:
        bool: True if port is open, False otherwise
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((ip, port))
        return result == 0
    except socket.error:
        return False
    finally:
        sock.close()


def scan_subnet(subnet, start_ip, end_ip, start_port, end_port, timeout=0.1):
    """
    Scan a subnet range for open ports.
    
    Args:
        subnet (str): The subnet prefix (e.g., "192.168.1.")
        start_ip (int): First IP in range to scan
        end_ip (int): Last IP in range to scan
        start_port (int): First port in range to scan
        end_port (int): Last port in range to scan
        timeout (float): Connection timeout in seconds
        
    Returns:
        list: List of tuples (ip, port) for open ports
    """
    open_ports = []
    
    for ip in range(start_ip, end_ip + 1):
        full_ip = f"{subnet}{ip}"
        
        for port in range(start_port, end_port + 1):
            if scan_port(full_ip, port, timeout):
                open_ports.append((full_ip, port))
                print(f"IP: {full_ip} | Port {port} is open")
    
    return open_ports


def main():
    """Main function to parse arguments and run the port scanner."""
    parser = argparse.ArgumentParser(description='Simple Port Scanner')
    parser.add_argument('-s', '--subnet', default='192.168.1.',
                        help='Subnet to scan (e.g., 192.168.1.)')
    parser.add_argument('-i', '--ip-range', default='1-255',
                        help='IP range to scan (e.g., 1-255)')
    parser.add_argument('-p', '--port-range', default='1-1024',
                        help='Port range to scan (e.g., 1-1024)')
    parser.add_argument('-t', '--timeout', type=float, default=0.1,
                        help='Connection timeout in seconds (default: 0.1)')
    
    args = parser.parse_args()
    
    # Parse IP range
    try:
        if '-' in args.ip_range:
            start_ip, end_ip = map(int, args.ip_range.split('-'))
        else:
            start_ip = end_ip = int(args.ip_range)
    except ValueError:
        print("Error: Invalid IP range format. Use '1-255'")
        return 1
    
    # Parse port range
    try:
        if '-' in args.port_range:
            start_port, end_port = map(int, args.port_range.split('-'))
        else:
            start_port = end_port = int(args.port_range)
    except ValueError:
        print("Error: Invalid port range format. Use '1-1024'")
        return 1
    
    # Validate subnet format
    if not args.subnet.endswith('.'):
        args.subnet += '.'
    
    # Run the scan
    print(f"Scanning subnet {args.subnet} with IP range {start_ip}-{end_ip} and ports {start_port}-{end_port}")
    open_ports = scan_subnet(args.subnet, start_ip, end_ip, start_port, end_port, args.timeout)
    
    # Print summary
    print(f"\nScan Summary:")
    print(f"  Subnet: {args.subnet}")
    print(f"  IP Range: {start_ip}-{end_ip}")
    print(f"  Port Range: {start_port}-{end_port}")
    print(f"  Open Ports Found: {len(open_ports)}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(130)
