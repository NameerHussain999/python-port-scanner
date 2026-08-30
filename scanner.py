import socket

from services import get_service, detect_service





def scan_port(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)


    try:
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            service = get_service(port)
            service, banner = detect_service(
                target_ip,
                port,
                service
            )


            
            return port, "OPEN", service, banner

    finally:
        sock.close()

    return None