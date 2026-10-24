#!/usr/bin/env python3
"""
AI-Enhanced Port Scanner & Service Detector
For authorized penetration testing only
"""

import nmap
import socket
import json
from datetime import datetime
import argparse
import sys

class AIPortScanner:
    def __init__(self):
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError:
            print("[!] Nmap not found. Install with: sudo apt install nmap")
            sys.exit(1)
        
    def scan_target(self, target, ports='1-65535', scan_type='full'):
        """
        Scan all ports - comprehensive scan
        
        Args:
            target: IP address or hostname
            ports: Port range (default: all 65535 ports)
            scan_type: 'full', 'quick', or 'stealth'
        """
        print(f"[*] Scanning {target} on ports {ports}")
        print(f"[*] Scan started: {datetime.now()}")
        print(f"[*] Scan type: {scan_type}")
        
        # Choose scan arguments based on type
        if scan_type == 'full':
            arguments = '-p- -sV -sC -T4 -A'
        elif scan_type == 'quick':
            arguments = '-sV -T4'
        elif scan_type == 'stealth':
            arguments = '-sS -sV -T2'
        else:
            arguments = '-sV -T4'
        
        try:
            # Full TCP scan
            self.nm.scan(target, ports, arguments=arguments)
        except Exception as e:
            print(f"[!] Scan error: {e}")
            return None
        
        results = []
        for host in self.nm.all_hosts():
            print(f"\n[+] Host: {host} ({self.nm[host].hostname()})")
            print(f"[+] State: {self.nm[host].state()}")
            
            for proto in self.nm[host].all_protocols():
                print(f"\n[*] Protocol: {proto}")
                port_list = self.nm[host][proto].keys()
                
                for port in port_list:
                    service = self.nm[host][proto][port]
                    
                    result = {
                        'host': host,
                        'port': port,
                        'state': service['state'],
                        'service': service.get('name', 'unknown'),
                        'version': service.get('version', 'unknown'),
                        'product': service.get('product', 'unknown'),
                        'extrainfo': service.get('extrainfo', '')
                    }
                    
                    results.append(result)
                    
                    print(f"  Port {port}/{proto}: {service['state']} - "
                          f"{service.get('name', 'unknown')} "
                          f"{service.get('product', '')} "
                          f"{service.get('version', '')}")
        
        return self.ai_analyze(results)
    
    def ai_analyze(self, scan_results):
        """AI-powered vulnerability assessment"""
        print("\n" + "="*60)
        print("[*] AI VULNERABILITY ANALYSIS")
        print("="*60)
        
        vulnerabilities = []
        critical_count = 0
        high_count = 0
        medium_count = 0
        
        for service in scan_results:
            severity = None
            recommendation = None
            
            # Critical vulnerabilities
            if service['port'] in [23, 512, 513, 514, 2049] and service['state'] == 'open':
                severity = 'CRITICAL'
                recommendation = f"Insecure legacy service {service['service']} on port {service['port']} - DISABLE IMMEDIATELY"
                critical_count += 1
                
            # High severity
            elif 'ftp' in service['service'].lower() and service['state'] == 'open':
                severity = 'HIGH'
                recommendation = f"FTP on port {service['port']} - Check for anonymous access, use SFTP instead"
                high_count += 1
                
            elif service['port'] == 3389 and service['state'] == 'open':
                severity = 'HIGH'
                recommendation = f"RDP exposed on port {service['port']} - Enable NLA, use VPN, strong passwords"
                high_count += 1
                
            elif service['port'] in [1433, 3306, 5432, 27017] and service['state'] == 'open':
                severity = 'HIGH'
                recommendation = f"Database port {service['port']} ({service['service']}) exposed - Restrict to localhost"
                high_count += 1
            
            # Medium severity
            elif 'ssh' in service['service'].lower() and service['state'] == 'open':
                severity = 'MEDIUM'
                recommendation = f"SSH on port {service['port']} - Disable root login, use key-based auth"
                medium_count += 1
                
            elif service['port'] in [80, 8080, 8000] and 'http' in service['service'].lower():
                severity = 'MEDIUM'
                recommendation = f"HTTP on port {service['port']} - Consider HTTPS, check for web vulnerabilities"
                medium_count += 1
            
            if recommendation:
                vulnerabilities.append({
                    'severity': severity,
                    'port': service['port'],
                    'service': service['service'],
                    'recommendation': recommendation
                })
                
                # Color coding
                if severity == 'CRITICAL':
                    print(f"\n[!] {severity}: {recommendation}")
                elif severity == 'HIGH':
                    print(f"\n[!] {severity}: {recommendation}")
                else:
                    print(f"\n[*] {severity}: {recommendation}")
        
        # Summary
        print("\n" + "="*60)
        print("[*] VULNERABILITY SUMMARY")
        print("="*60)
        print(f"Critical: {critical_count}")
        print(f"High: {high_count}")
        print(f"Medium: {medium_count}")
        print(f"Total services found: {len(scan_results)}")
        
        return {
            'timestamp': str(datetime.now()),
            'services': scan_results,
            'vulnerabilities': vulnerabilities,
            'summary': {
                'critical': critical_count,
                'high': high_count,
                'medium': medium_count,
                'total_services': len(scan_results)
            }
        }
    
    def save_results(self, results, filename=None):
        """Save results to JSON file"""
        if not filename:
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[+] Results saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='AI-Enhanced Port Scanner for authorized pentesting',
        epilog='WARNING: Only use on systems you own or have written authorization to test'
    )
    
    parser.add_argument('target', help='Target IP address or hostname')
    parser.add_argument('-p', '--ports', default='1-65535', 
                        help='Port range (default: 1-65535 for full scan)')
    parser.add_argument('-t', '--type', choices=['full', 'quick', 'stealth'],
                        default='full', help='Scan type (default: full)')
    parser.add_argument('-o', '--output', help='Output JSON filename')
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║         AI-ENHANCED PORT SCANNER v1.0                     ║
║         For Authorized Penetration Testing Only           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"[!] WARNING: Only scan authorized targets!")
    print(f"[!] Unauthorized scanning is illegal\n")
    
    scanner = AIPortScanner()
    results = scanner.scan_target(args.target, args.ports, args.type)
    
    if results:
        scanner.save_results(results, args.output)
        print("\n[+] Scan complete!")
    else:
        print("\n[!] Scan failed")


if __name__ == "__main__":
    main()
