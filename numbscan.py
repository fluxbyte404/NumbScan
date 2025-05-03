import socket
import threading

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m" 

print(f"""{RED}
  _   _                 _     _____                 
 | \ | |               | |   / ____|                
 |  \| |_   _ _ __ ___ | |__| (___   ___ __ _ _ __  
 | . ` | | | | '_ ` _ \| '_ \\___ \ / __/ _` | '_ \ 
 | |\  | |_| | | | | | | |_) |___) | (_| (_| | | | |
 |_| \_|\__,_|_| |_| |_|_.__/_____/ \___\__,_|_| |_|
                                                     {RESET}""")

target = input("Enter the IP address to scan: ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))

print_lock = threading.Lock()

def grab_banner(sock):
    try:
        sock.settimeout(2)
        return sock.recv(1024).decode().strip()
    except:
        return ""

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            banner = grab_banner(sock)

            with print_lock:
                print(f"{RED}[+] Port {port} is OPEN | Service: {service} | Banner: {banner if banner else 'N/A'}{RESET}")

        sock.close()
    except:
        pass

def main():
    threads = []

    print(f"{YELLOW}\n[*] Scanning {target} from port {start_port} to {end_port}...\n{RESET}")

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"{GREEN}\nScan complete, ports {start_port} to {end_port} were scanned.{RESET}")

if __name__ == "__main__":
    main()
