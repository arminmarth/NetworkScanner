import socket

start_port = 79
end_port = 81
subnet = "10.0.2."
targets = range(1,255)

for ip in targets:
    subs = subnet+str(ip)

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)

        result = sock.connect_ex((subs, port))
        if result == 0:
            print(f"IP: {subs} | Port {port} is open")

        sock.close()
