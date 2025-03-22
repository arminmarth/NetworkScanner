#!/usr/bin/env python3
"""
NetworkScanner - A tool to scan networks for open ports and conduct web enumeration

This script allows users to scan IP ranges for open ports, with configurable
parameters for target networks, port ranges, and connection timeouts.

Author: Armin Marth
Version: 1.1.0
Last Updated: 2025-03-22
"""

import socket
import argparse
import sys
import concurrent.futures
import time
from datetime import datetime

def scan_port(ip, port, timeout):
    """
    Scan a single IP and port combination.
    
    Args:
        ip (str): The IP address to scan
        port (int): The port number to scan
        timeout (float): Connection timeout in seconds
        
    Returns:
        tuple: (ip, port, is_open) where is_open is a boolean
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((ip, port))
        is_open = (result == 0)
        return (ip, port, is_open)
    except socket.error as e:
        return (ip, port, False)
    finally:
        sock.close()

def scan_network(subnet, ip_range, port_range, timeout, threads):
    """
    Scan a network range for open ports.
    
    Args:
        subnet (str): The subnet prefix (e.g., "192.168.1.")
        ip_range (range): Range of IP addresses to scan
        port_range (range): Range of ports to scan
        timeout (float): Connection timeout in seconds
        threads (int): Number of concurrent threads to use
        
    Returns:
        list: List of tuples (ip, port) for open ports
    """
    open_ports = []
    total_scans = len(ip_range) * len(port_range)
    scans_completed = 0
    
    print(f"Starting scan of {len(ip_range)} IPs across {len(port_range)} ports ({total_scans} total scans)")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    start_time = time.time()
    
    # Create a list of all scan tasks
    scan_tasks = []
    for ip_suffix in ip_range:
        ip = f"{subnet}{ip_suffix}"
        for port in port_range:
            scan_tasks.append((ip, port, timeout))
    
    # Use ThreadPoolExecutor to run scans concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, ip, port, timeout) for ip, port, timeout in scan_tasks]
        
        for future in concurrent.futures.as_completed(futures):
            scans_completed += 1
            ip, port, is_open = future.result()
            
            # Print progress every 50 scans
            if scans_completed % 50 == 0 or scans_completed == total_scans:
                percent_complete = (scans_completed / total_scans) * 100
                elapsed_time = time.time() - start_time
                print(f"Progress: {scans_completed}/{total_scans} ({percent_complete:.1f}%) - Elapsed time: {elapsed_time:.1f}s", 
                      end='\r', file=sys.stderr)
            
            if is_open:
                open_ports.append((ip, port))
                print(f"\nFound open port: {ip} | Port {port} is open")
    
    print(f"\nScan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total scan time: {time.time() - start_time:.2f} seconds")
    
    return open_ports

def main():
    """Main function to parse arguments and run the network scanner."""
    parser = argparse.ArgumentParser(description='Network Port Scanner')
    parser.add_argument('-s', '--subnet', default='192.168.1.', 
                        help='Subnet to scan (e.g., 192.168.1.)')
    parser.add_argument('-i', '--ip-range', default='1-255',
                        help='IP range to scan (e.g., 1-255 or 1,2,3,4)')
    parser.add_argument('-p', '--port-range', default='1-1024',
                        help='Port range to scan (e.g., 1-1024 or 22,80,443)')
    parser.add_argument('-t', '--timeout', type=float, default=0.5,
                        help='Connection timeout in seconds (default: 0.5)')
    parser.add_argument('-w', '--threads', type=int, default=50,
                        help='Number of concurrent threads (default: 50)')
    parser.add_argument('-o', '--output', help='Output file to save results')
    
    args = parser.parse_args()
    
    # Parse IP range
    try:
        if ',' in args.ip_range:
            ip_range = [int(x) for x in args.ip_range.split(',')]
        elif '-' in args.ip_range:
            start, end = map(int, args.ip_range.split('-'))
            ip_range = range(start, end + 1)
        else:
            ip_range = [int(args.ip_range)]
    except ValueError:
        print("Error: Invalid IP range format. Use '1-255' or '1,2,3,4'")
        return 1
    
    # Parse port range
    try:
        if ',' in args.port_range:
            port_range = [int(x) for x in args.port_range.split(',')]
        elif '-' in args.port_range:
            start, end = map(int, args.port_range.split('-'))
            port_range = range(start, end + 1)
        else:
            port_range = [int(args.port_range)]
    except ValueError:
        print("Error: Invalid port range format. Use '1-1024' or '22,80,443'")
        return 1
    
    # Validate subnet format
    if not args.subnet.endswith('.'):
        args.subnet += '.'
    
    # Run the scan
    open_ports = scan_network(args.subnet, ip_range, port_range, args.timeout, args.threads)
    
    # Print summary
    print(f"\nScan Summary:")
    print(f"  Subnet: {args.subnet}")
    print(f"  IP Range: {args.ip_range}")
    print(f"  Port Range: {args.port_range}")
    print(f"  Open Ports Found: {len(open_ports)}")
    
    # Save results to file if specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(f"# Network Scan Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Subnet: {args.subnet}, IP Range: {args.ip_range}, Port Range: {args.port_range}\n\n")
                
                if open_ports:
                    for ip, port in open_ports:
                        f.write(f"{ip},{port}\n")
                else:
                    f.write("# No open ports found\n")
            
            print(f"Results saved to {args.output}")
        except IOError as e:
            print(f"Error saving results to file: {e}")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(130)
