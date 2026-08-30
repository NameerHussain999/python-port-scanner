import socket
from concurrent.futures import ThreadPoolExecutor
from syn_scanner import syn_scan
import time
import csv
from datetime import datetime
from scanner import scan_port
from syn_scanner import scan_port_syn
from exporter import export_csv, export_txt




    

def main():
    print("=" * 50)
    print("         Python Port Scanner")
    print("=" * 50)


    target = input("Enter target IP or hostname:  ").strip()


    try:
        target_ip = socket.gethostbyname(target)

    except socket.gaierror:
        print("[ERROR] Could not resolve the target")
        return
    
    print(f"\nResolved IP: {target_ip}")

    try:
        start_port = int(input("Enter starting point: "))
        end_port = int(input("Enter ending port: "))
    except ValueError:
        print("[ERROR] Please enter valid port numbers.")
        return
    
        

        
    if start_port < 1 or start_port > 65535:
        print("[ERROR] Starting port must be between 1 and 65535")
        return
    
    if end_port < 1 or end_port > 65535:
        print("[ERROR] Starting port must be between 1 and 65535")
        return

    if start_port > end_port:
        print("[ERROR] Starting port can not be greater than ending port")
        return


    print("\nSelect scan type:")
    print("1. TCP Connect Scan")
    print("2. SYN Scan")
    
    scan_choice = input("Choice: ").strip()
    
    
    if scan_choice not in ["1", "2"]:
        print("[ERROR] Invalid scan type.")
        return
    
    total_ports = end_port - start_port + 1
    
    print("\n" + "=" * 60)
    print("SCAN INFORMATION")
    print("=" * 60)
    
    print(f"Target       :{target_ip}")
    print(f"Port range   :{start_port}-{end_port}")
    print(f"Ports        :{total_ports}")


    print(f"\nScanning ports {start_port}-{end_port}...\n")

    if scan_choice == "1":

        print("\nRunning TCP Connect Scan...\n"

        )
    else:
        print("Scan type    : SYN Scan")


    results_list = []

    start_time = time.time()
        


    if scan_choice == "1":
        print("\nRunning TCP Connect Scan...\n")

    with ThreadPoolExecutor(max_workers = 100) as executer:
                results = executer.map(
                lambda port: scan_port(target_ip, port),
                range(start_port, end_port + 1)
            )

    for result in results:
            if result is not None:
                results_list.append(result)


    else:
            print("\nRunning SYN Scan...\n")

            with ThreadPoolExecutor(max_workers = 50) as executer:
                results = executer.map(
                lambda port: scan_port_syn(target_ip, port),
                range(start_port, end_port + 1)
            )

            for result in results:
                results_list.append(result)


    end_time = time.time()
    scan_duration = end_time - start_time

    print("\n" + "=" * 75)
    print("SCAN RESULTS")
    print("=" * 75)


    print(
        f"{'PORT':<10}"
        f"{'STATE':<12}"
        f"{'SERVICE':<16}"
        f"Banner"
    )

    print("-" * 75)

    if not results_list:
        print("No open ports found.")

    for port, state, service, banner in results_list:
        print(
            f"{port:<10}"
            f"{state:<12}"
            f"{service:<16}"
            f"{banner}"
        )

    open_count = 0
    closed_count = 0
    filtered_count = 0


    for port, state, service, banner in results_list:

        if state == "OPEN":
            open_count += 1

        elif state == "CLOSED":
            closed_count += 1

        elif state == "FILTERED":
            filtered_count += 1


    print("\n" + "=" * 75)
    print("SCAN SUMMARY")
    print("=" * 75)


    print(f"Target        :{target_ip}")
    print(f"Port range    :{start_port}-{end_port}")
    print(f"Ports scanned :{total_ports}")
    print(f"Open ports    :{open_count}")


    if scan_choice == "2":
        print(f"Closed ports     :{closed_count}")
        print(f"Filtered ports   :{filtered_count}")


    print(f"Scan duration   :{scan_duration:.2f} seconds")


    print("=" * 75)


    print("\nSave scan results?")
    print("1. CSV")
    print("2. TXT")
    print("3. Both")
    print("4. Do not save")

    export_choice = input("Choice: ").strip()

    if export_choice == "1":
        export_csv(
            results_list,
            target_ip,
            start_port,
            end_port,
            scan_choice,
            scan_duration
        )

    elif export_choice == "2":
        export_txt(
            results_list,
            target_ip,
            start_port,
            end_port,
            scan_choice,
            scan_duration
        )

    elif export_choice == "3":
        export_csv(
            results_list,
            target_ip,
            start_port,
            end_port,
            scan_choice,
            scan_duration
        )

        export_txt(
            results_list,
            target_ip,
            start_port,
            end_port,
            scan_choice,
            scan_duration
        )

    elif export_choice == "4":
        print("\nResults were not saved.")

    else:
        print("\n[WARNING] Invalid option. Results were not saved.")


        
if __name__ == "__main__":
    main()