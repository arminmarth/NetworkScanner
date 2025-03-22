# NetworkScanner

A powerful Python tool for scanning networks to identify open ports and conduct web enumeration.

## Features

- **IP Range Scanning**: Scan entire subnets or specific IP addresses
- **Port Range Scanning**: Scan specific ports or port ranges
- **Multithreaded**: Fast scanning with configurable thread count
- **Timeout Control**: Adjustable connection timeout settings
- **Progress Reporting**: Real-time scan progress updates
- **Results Export**: Save scan results to file for further analysis

## Installation

No installation required beyond Python 3.6+. The script uses only standard library modules.

```bash
# Clone the repository
git clone https://github.com/arminmarth/NetworkScanner.git
cd NetworkScanner

# Make the script executable
chmod +x network_scanner.py
```

## Usage

```bash
./network_scanner.py [options]
```

### Command Line Options

```
  -h, --help            Show this help message and exit
  -s SUBNET, --subnet SUBNET
                        Subnet to scan (e.g., 192.168.1.)
  -i IP_RANGE, --ip-range IP_RANGE
                        IP range to scan (e.g., 1-255 or 1,2,3,4)
  -p PORT_RANGE, --port-range PORT_RANGE
                        Port range to scan (e.g., 1-1024 or 22,80,443)
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds (default: 0.5)
  -w THREADS, --threads THREADS
                        Number of concurrent threads (default: 50)
  -o OUTPUT, --output OUTPUT
                        Output file to save results
```

### Examples

Scan a local network for common ports:
```bash
./network_scanner.py --subnet 192.168.1. --port-range 22,80,443,8080
```

Scan a specific IP for all ports from 1 to 65535:
```bash
./network_scanner.py --ip-range 10 --subnet 192.168.1. --port-range 1-65535
```

Scan multiple IPs with a longer timeout and save results:
```bash
./network_scanner.py --subnet 10.0.0. --ip-range 1,2,3,4,5 --timeout 1.0 --output results.txt
```

## Performance Tips

- Adjust the `--threads` parameter based on your system capabilities
- Use smaller port ranges for faster scans
- Increase timeout for scanning over high-latency networks
- Decrease timeout for faster scans on local networks

## Security and Ethical Use

This tool is intended for network administrators and security professionals to scan networks they own or have explicit permission to scan. Unauthorized scanning of networks may violate laws and regulations.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
