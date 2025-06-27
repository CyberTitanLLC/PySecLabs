import nmap
import sys

def scan_target(network_range):
    scanner = nmap.PortScanner()
    print(f"\n[*] Starting full scan on {network_range} ...\n")

    try:
        scanner.scan(
            hosts=network_range,
            arguments="-T4 -p- -sV -sC -O --host-timeout 60m"
        )
    except Exception as e:
        print(f"[!] Scan failed: {e}")
        sys.exit(1)

    for host in scanner.all_hosts():
        print("="*60)
        print(f"Host: {host} ({scanner[host].hostname()})")
        print(f"State: {scanner[host].state()}")

        if 'osmatch' in scanner[host]:
            if scanner[host]['osmatch']:
                print(f"OS Guess: {scanner[host]['osmatch'][0]['name']}")
            else:
                print("OS Guess: Not available")

        for proto in scanner[host].all_protocols():
            print(f"\nProtocol: {proto}")
            ports = scanner[host][proto].keys()
            for port in sorted(ports):
                info = scanner[host][proto][port]
                print(f"  Port {port}/{proto} | State: {info['state']} | Service: {info.get('name', 'n/a')} | Version: {info.get('version', '')} {info.get('product', '')}")

        print("="*60 + "\n")

if __name__ == "__main__":
    net_range = input("Enter target network/range (e.g., 192.168.1.0/24): ")
    scan_target(net_range)
