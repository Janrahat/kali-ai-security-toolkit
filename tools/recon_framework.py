#!/usr/bin/env python3
"""
Automated Reconnaissance Framework
Multi-tool automation for comprehensive target reconnaissance
For authorized security assessments only
"""

import subprocess
import os
import sys
import argparse
from datetime import datetime
import json

class ReconFramework:
    def __init__(self, target, output_dir=None):
        self.target = target
        
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = f"recon_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"[+] Output directory: {self.output_dir}")
        
        self.results = {
            'target': target,
            'timestamp': str(datetime.now()),
            'scans_completed': []
        }
    
    def check_tool(self, tool_name):
        """Check if a tool is installed"""
        try:
            subprocess.run(['which', tool_name], 
                          capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def nmap_scan(self, scan_type='full'):
        """Comprehensive nmap scan"""
        print("\n" + "="*60)
        print("[*] Running NMAP scan...")
        print("="*60)
        
        if not self.check_tool('nmap'):
            print("[!] nmap not found. Install with: sudo apt install nmap")
            return False
        
        output_file = f"{self.output_dir}/nmap"
        
        if scan_type == 'full':
            cmd = f"nmap -p- -sV -sC -A -oA {output_file} {self.target}"
        elif scan_type == 'quick':
            cmd = f"nmap -sV -T4 -oA {output_file} {self.target}"
        else:
            cmd = f"nmap -p- -sV -oA {output_file} {self.target}"
        
        print(f"[*] Command: {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(result.stdout)
            
            self.results['scans_completed'].append({
                'scan': 'nmap',
                'status': 'completed',
                'output_file': output_file
            })
            
            print(f"[+] NMAP scan completed. Results saved to {output_file}.*")
            return True
        except Exception as e:
            print(f"[!] NMAP scan error: {e}")
            return False
    
    def subdomain_enum(self):
        """Subdomain enumeration"""
        print("\n" + "="*60)
        print("[*] Running subdomain enumeration...")
        print("="*60)
        
        output_file = f"{self.output_dir}/subdomains.txt"
        
        # Try multiple tools
        tools = [
            ('sublist3r', f"sublist3r -d {self.target} -o {output_file}"),
            ('amass', f"amass enum -passive -d {self.target} -o {output_file}"),
            ('subfinder', f"subfinder -d {self.target} -o {output_file}")
        ]
        
        for tool_name, cmd in tools:
            if self.check_tool(tool_name):
                print(f"[*] Using {tool_name}")
                print(f"[*] Command: {cmd}")
                
                try:
                    subprocess.run(cmd, shell=True)
                    
                    self.results['scans_completed'].append({
                        'scan': 'subdomain_enum',
                        'tool': tool_name,
                        'status': 'completed',
                        'output_file': output_file
                    })
                    
                    # Count subdomains found
                    if os.path.exists(output_file):
                        with open(output_file, 'r') as f:
                            count = len(f.readlines())
                        print(f"[+] Found {count} subdomains. Saved to {output_file}")
                    
                    return True
                except Exception as e:
                    print(f"[!] Error with {tool_name}: {e}")
                    continue
        
        print("[!] No subdomain enumeration tools found.")
        print("[*] Install with: sudo apt install sublist3r")
        return False
    
    def dns_enum(self):
        """DNS enumeration"""
        print("\n" + "="*60)
        print("[*] Running DNS enumeration...")
        print("="*60)
        
        output_file = f"{self.output_dir}/dns_records.txt"
        
        # Common DNS record types
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        with open(output_file, 'w') as f:
            for record in record_types:
                print(f"[*] Querying {record} records...")
                cmd = f"dig {self.target} {record} +short"
                
                try:
                    result = subprocess.run(cmd, shell=True, 
                                          capture_output=True, text=True)
                    
                    if result.stdout.strip():
                        f.write(f"\n=== {record} Records ===\n")
                        f.write(result.stdout)
                        print(f"[+] {record}: {result.stdout.strip()}")
                except Exception as e:
                    print(f"[!] Error querying {record}: {e}")
        
        self.results['scans_completed'].append({
            'scan': 'dns_enum',
            'status': 'completed',
            'output_file': output_file
        })
        
        print(f"[+] DNS enumeration complete. Saved to {output_file}")
        return True
    
    def whois_lookup(self):
        """WHOIS lookup"""
        print("\n" + "="*60)
        print("[*] Running WHOIS lookup...")
        print("="*60)
        
        output_file = f"{self.output_dir}/whois.txt"
        cmd = f"whois {self.target}"
        
        try:
            result = subprocess.run(cmd, shell=True, 
                                  capture_output=True, text=True)
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            self.results['scans_completed'].append({
                'scan': 'whois',
                'status': 'completed',
                'output_file': output_file
            })
            
            print(f"[+] WHOIS lookup complete. Saved to {output_file}")
            return True
        except Exception as e:
            print(f"[!] WHOIS lookup error: {e}")
            return False
    
    def web_crawl(self):
        """Web application crawling"""
        print("\n" + "="*60)
        print("[*] Running web crawler...")
        print("="*60)
        
        output_dir = f"{self.output_dir}/spider"
        
        tools = [
            ('gospider', f"gospider -s http://{self.target} -o {output_dir}"),
            ('hakrawler', f"echo http://{self.target} | hakrawler -d 3 > {output_dir}/hakrawler.txt")
        ]
        
        for tool_name, cmd in tools:
            if self.check_tool(tool_name):
                print(f"[*] Using {tool_name}")
                print(f"[*] Command: {cmd}")
                
                try:
                    subprocess.run(cmd, shell=True)
                    
                    self.results['scans_completed'].append({
                        'scan': 'web_crawl',
                        'tool': tool_name,
                        'status': 'completed',
                        'output_dir': output_dir
                    })
                    
                    print(f"[+] Web crawl complete. Saved to {output_dir}")
                    return True
                except Exception as e:
                    print(f"[!] Error with {tool_name}: {e}")
                    continue
        
        print("[!] No web crawling tools found.")
        print("[*] Install with: go install github.com/jaeles-project/gospider@latest")
        return False
    
    def save_summary(self):
        """Save summary of all recon activities"""
        summary_file = f"{self.output_dir}/recon_summary.json"
        
        with open(summary_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[+] Summary saved to {summary_file}")
    
    def run_all(self, nmap_type='full'):
        """Run all reconnaissance modules"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║      AUTOMATED RECONNAISSANCE FRAMEWORK v1.0              ║
║      For Authorized Security Assessments Only             ║
╚═══════════════════════════════════════════════════════════╝
        """)
        
        print(f"[!] WARNING: Only scan authorized targets!")
        print(f"[!] Target: {self.target}")
        print(f"[!] Started: {datetime.now()}\n")
        
        # Run all modules
        self.nmap_scan(nmap_type)
        self.subdomain_enum()
        self.dns_enum()
        self.whois_lookup()
        self.web_crawl()
        
        # Save summary
        self.save_summary()
        
        print("\n" + "="*60)
        print(f"[+] Reconnaissance complete!")
        print(f"[+] All results saved to: {self.output_dir}/")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Automated Reconnaissance Framework for authorized testing',
        epilog='WARNING: Only use on systems you own or have written authorization to test'
    )
    
    parser.add_argument('target', help='Target domain or IP address')
    parser.add_argument('-o', '--output', help='Output directory name')
    parser.add_argument('-t', '--type', choices=['full', 'quick'],
                        default='full', help='Nmap scan type (default: full)')
    parser.add_argument('-m', '--modules', nargs='+',
                        choices=['nmap', 'subdomain', 'dns', 'whois', 'web'],
                        help='Run specific modules only (default: all)')
    
    args = parser.parse_args()
    
    recon = ReconFramework(args.target, args.output)
    
    if args.modules:
        # Run specific modules
        if 'nmap' in args.modules:
            recon.nmap_scan(args.type)
        if 'subdomain' in args.modules:
            recon.subdomain_enum()
        if 'dns' in args.modules:
            recon.dns_enum()
        if 'whois' in args.modules:
            recon.whois_lookup()
        if 'web' in args.modules:
            recon.web_crawl()
        
        recon.save_summary()
    else:
        # Run all modules
        recon.run_all(args.type)


if __name__ == "__main__":
    main()
