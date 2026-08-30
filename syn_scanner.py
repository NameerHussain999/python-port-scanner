
from scapy.all import IP, TCP, sr1, send

from services import get_service, detect_service


def syn_scan(target_ip, port):
    packet = (
        IP(dst=target_ip)
        / TCP(
            dport=port,
            flags="S"
        )
    )

    response = sr1(
        packet,
        timeout=1,
        verbose=0
    )

    if response is None:
        return "FILTERED"

    if response.haslayer(TCP):
        flags = response[TCP].flags

        # SYN + ACK means the port is open.
        if flags & 0x12 == 0x12:
            rst_packet = (
                IP(dst=target_ip)
                / TCP(
                    dport=port,
                    flags="R"
                )
            )

            send(
                rst_packet,
                verbose=0
            )

            return "OPEN"

        # RST means the port is closed.
        if flags & 0x04:
            return "CLOSED"

    return "FILTERED"


def scan_port_syn(target_ip, port):
    state = syn_scan(
        target_ip,
        port
    )

    if state == "OPEN":
        service = get_service(port)

        service, banner = detect_service(
            target_ip,
            port,
            service
        )

        return (
            port,
            state,
            service,
            banner
        )

    return (
        port,
        state,
        "-",
        "-"
    )

    