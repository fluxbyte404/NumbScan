import socket # for networking purposes
import threading # for multithreading

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



# main function is the entry point of the program and it will be called when the program is run
def main():
    threads = []

    print(f"{YELLOW}\n[*] Scanning {target} from port {start_port} to {end_port}...\n{RESET}")

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))#args must be a tuple to pass arguments to the function
        threads.append(t)#add the thread to the list
        t.start() #start the thread

    for t in threads: 
        t.join() #wait for all the threads to complete

    print(f"{GREEN}\nScan complete, ports {start_port} to {end_port} were scanned.{RESET}")



# scan_port function scans the target port and checks if it is open
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPv4 and SOCK_STREAM for TCP
        sock.settimeout(1) # wait for 1 second to check if the port is open
        result = sock.connect_ex((target, port)) # connect to the target port and check if it is open
        if result == 0: # if the result is 0 then the port is open
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




# grab_banner function grabs the banner from the target port
def grab_banner(sock):
    try:
        sock.settimeout(2) # wait for 2 seconds to grab the banner
        return sock.recv(1024).decode().strip() # receive the banner and strip any whitespace
    except:
        return ""



# if the script is run directly, it will call the main function, but if it is imported as a module, it will not call the main function
if __name__ == "__main__":
    main()
