import socket

# check if specific network ports are open on a target host
def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # wait max 2 seconds
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        print(f"[+] {host}:{port} is OPEN")
    else:
        print(f"[-] {host}:{port} is CLOSED")
if __name__ == "__main__":
    target = "google.com"
    common_ports = [80, 443, 22]  # HTTP, HTTPS, SSH
    print(f"Checking ports on {target}...")
    for p in common_ports:
        check_port(target, p)
