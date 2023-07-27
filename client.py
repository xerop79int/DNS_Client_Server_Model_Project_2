# client.py
import sys
import socket
import time

def query_dns_server(server_ip, server_port, domain):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, server_port)

    try:
        query = domain.encode()
        client_socket.sendto(query, server_address)
        response, _ = client_socket.recvfrom(4096)  # Increase buffer size for potential larger responses
        response_size = len(response)
        ip_address = response.decode().strip()

        # Check for truncated response (TC bit set) and retry over TCP if necessary
        while response_size >= 512 and "TC" in ip_address:
            client_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(server_address)
            client_socket.sendall(query)
            response = client_socket.recv(4096)
            response_size = len(response)
            ip_address = response.decode().strip()

        return ip_address, response_size
    except socket.timeout:
        return "DNS server is not responding", 0
    except:
        return "Check the server IP and port are correct and check if the server is running", 0
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python client.py <server_ip> <server_port> <domain> <timeout(optional)>")
        sys.exit(1)

    server_ip = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Usage: python client.py <server_ip> <server_port> <domain> <timeout(optional)>")
        sys.exit(1)
    domain_name = sys.argv[3]
    ip_address = query_dns_server(server_ip, server_port, domain_name)
    
    if len(sys.argv) == 5:
        timeout = sys.argv[4]
        time.sleep(int(timeout))

    if ip_address == 'Not found':
        print(f"{domain_name} is not found")
    elif ip_address == 'Check the server IP and port are correct and check if the server is running':
        print(ip_address)
    else:
        print(f"{domain_name} resolves to: {ip_address[0]} with Response Size: {ip_address[1]}")
