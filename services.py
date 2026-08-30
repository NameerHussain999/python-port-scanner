import socket

def get_service(port):
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def grab_banner(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)


        sock.connect((target_ip, port))

        try:
            banner = sock.recv(1024).decode(errors = "ignore").strip()

            if banner:
                sock.close()
                return banner


        except socket.timeout:
            pass

        sock.close()

    except(socket.timeout, ConnectionRefusedError, OSError):
        pass

    return "No banner"

def detect_service(target_ip, port, service):

    banner = grab_banner(target_ip, port)

    if banner != "No banner":
        return service, banner

    if port in [80, 8080, 8000, 8888]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)

            sock.connect((target_ip, port))

            request = (
                "HEAD / HTTP/1.1\r\n"
                f"HOST: {target_ip}\r\n"
                "Connection: close\r\n\r\n"
            )

            sock.sendall(request.encode())

            response = sock.recv(2048).decode(errors = "ignore")
            sock.close()

            if response.startswith("HTTP/"):
                first_lines = response.split("\r\n")

                server = "HTTP server"

                for line in first_lines:
                    if line.lower().startswith("server:"):
                        server = line.split(":", 1)[1].strip()
                        break

                return "http", server

        except (socket.timeout, ConnectionRefusedError, OSError):
            pass

    return service, "No banner"
