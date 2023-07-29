# server.py
import sys
import socket
import select


# the named.root file contains the DNS_RECORDS dictionary
domain_to_ipv4 = {}
domain_to_ipv6 = {}

# Read the data from the file
file_path = "named.root"
with open(file_path, 'r') as file:
    lines = file.readlines()

# Process the lines to find the domain and its corresponding IPv4 address
for line in lines:
    # Split the line into columns based on tab ('\t') separator
    columns = line.strip().split('\t')

    # Check if the line contains A record (IPv4) for a domain
    if columns[3] == "A":
        domain = columns[0]  # The domain is in the first column
        ipv4_address = columns[4]  # The IPv4 address is in the fifth column
        # Add the domain and its corresponding IPv4 address to the dictionary
        domain_to_ipv4[domain] = ipv4_address
    if columns[3] == "AAAA":
        domain = columns[0]
        ipv6_address = columns[4]
        domain_to_ipv6[domain] = ipv6_address

def handle_dns_request(data):
    domain = data.decode().strip()
    # read the named.root file to get the DNS records
    # ipv4_address = domain_to_ipv4.get(domain
    ipv4_address = domain_to_ipv4.get(domain, "Not found")
    ipv6_address = domain_to_ipv6.get(domain, "Not found")
    if ipv4_address == "Not found":
        return ipv6_address.encode()
    else:
        ipv4_address = f'IPV4: {ipv4_address} IPV6: {ipv6_address}'	
    return ipv4_address.encode()

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
