

import csv
import os
from datetime import datetime

def create_reports_folder():
    os.makedirs(
        "reports",
        exist_ok = True
    )





def export_csv(results_list, target_ip, start_port, end_port, scan_choice, scan_duration):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_results_{timestamp}.csv"


    scan_type = "TCP Connect Scan" if scan_choice == "1" else "SYN Scan"


    with open(filename, "w", newline = "", encoding = "utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Target", target_ip])
        writer.writerow(["Port Range", f"{start_port}-{end_port}"])
        writer.writerow(["Scan Type", scan_type])
        writer.writerow(["Scan Duration", f"{scan_duration:.2f} seconds"])
        writer.writerow([])


        writer.writerow([
            "Port",
            "State",
            "Service",
            "Banner"
        ])

        for port, state, service, banner in results_list:
            writer.writerow([
                port,
                state,
                service,
                banner
            ])

    print(f"\n[+] CSV report saved as: {filename}")


def export_txt(results_list, target_ip, start_port, end_port, scan_choice, scan_duration):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_results_{timestamp}.txt"


    scan_type = "TCP Connect Scan" if scan_choice == "1" else "SYN Scan"

    with open(filename, "w", encoding = "utf-8") as file:
        file.write("=" * 70 + "\n")
        file.write("PYTHON PORT SCANNER REPORT\n")
        file.write("=" * 70 + "\n\n")


        file.write(f"Target       :{target_ip}\n")
        file.write(f"Port Range   :{start_port}-{end_port}\n")
        file.write(f"Scan Type    :{scan_type}\n")
        file.write(f"Scan Duration:{scan_duration:.2f} seconds\n\n")


        file.write(
            f"{'PORT':<10}"
            f"{'STATE':<12}"
            f"{'SERVICE':<16}"
            f"banner\n"
        )

        file.write("-" * 70 + "\n")

        for port, state, service, banner in results_list:
            file.write(
                f"{port:<10}"
                f"{state:<12}"
                f"{service:<16}"
                f"{banner}\n"
            )

    print(f"\n[+] TXT Report saved as: {filename}")