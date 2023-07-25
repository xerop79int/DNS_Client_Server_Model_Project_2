# server.py
import sys
import socket
import select

# Define DNS records (replace with your own domain and IP mappings)
DNS_RECORDS = {
    "example.com": "192.168.0.1",
    "google.com": "8.8.8.8",
    # Add more domain-to-IP mappings here
}

def handle_dns_request(data):
    domain = data.decode().strip()

    if domain in DNS_RECORDS:
        ip_address = DNS_RECORDS[domain]
    else:
        ip_address = "Not found"

    return ip_address.encode()

def run_dns_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", port))

    print(f"DNS Server is running on port {port}...")
    try:
        while True:
            # Use select to handle multiple clients
            readable, _, _ = select.select([server_socket], [], [], 0.1)

            for sock in readable:
                data, client_address = sock.recvfrom(1024)
                response = handle_dns_request(data)
                server_socket.sendto(response, client_address)
    except KeyboardInterrupt:
        print("DNS Server stopped.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        run_dns_server(port)
    except ValueError:
        print("Invalid port number. Please provide a valid integer port.")
        sys.exit(1)
