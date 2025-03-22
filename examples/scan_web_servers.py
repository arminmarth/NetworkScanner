#!/usr/bin/env python3
"""
Example script demonstrating how to use the network_scanner.py tool
to scan a local network for common web server ports.
"""

import sys
import os
import subprocess

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Run a sample network scan for web server ports."""
    print("Running network scan for common web server ports...")
    
    # Define the command to run
    cmd = [
        "python3", 
        "../src/network_scanner.py",
        "--subnet", "192.168.1.",
        "--ip-range", "1-10",
        "--port-range", "80,443,8080,8443",
        "--timeout", "0.5",
        "--threads", "10"
    ]
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        print("\nScan completed successfully!")
    except subprocess.CalledProcessError:
        print("\nError running the network scanner.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
