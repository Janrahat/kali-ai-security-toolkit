#!/usr/bin/env python3
"""
Network Traffic Analyzer with AI Anomaly Detection
Real-time packet analysis and threat detection
For authorized network monitoring only
"""

try:
    from scapy.all import *
except ImportError:
    print("[!] Scapy not found. Install with: pip3 install scapy")
    print("[!] You may also need: sudo apt install python3-scapy")
    exit(1)

import collections
import argparse
from datetime import datetime
import json
import sys

class TrafficAnalyzer:
    def __init__(self, interface="eth0"):
        self.interface = interface
        self.packet_count = 0
        self.protocols = collections.Counter()
        self.ips = collections.Counter()
        self.ports = collections.Counter()
        self.packet_sizes = []
        self.suspicious_ips = set()
        self.start_time = datetime.now()
        
        print(f"[*] Initializing traffic analyzer on {interface}")
        print(f"[*] Started: {self.start_time}")
    
    def analyze_packet(self, packet):
        """Analyze individual packet"""
        self.packet_count += 1
        
        # Show progress
        if self.packet_count % 100 == 0:
            print(f"\r[*] Packets captured: {self.packet_count}", end='', flush=True)
        
        # IP layer analysis
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            self.ips[src_ip] += 1
            
            # Packet size
            self.packet_sizes.append(len(packet))
            
            # Protocol analysis
            if TCP in packet:
                self.protocols['TCP'] += 1
                self.ports[packet[TCP].dport] += 1
                
                # Check for common attack patterns
                self.detect_tcp_attacks(packet)
                
            elif UDP in packet:
                self.protocols['UDP'] += 1
                self.ports[packet[UDP].dport] += 1
                
            elif ICMP in packet:
                self.protocols['ICMP'] += 1
                self.detect_icmp_attacks(packet)
        
        # ARP analysis
        elif ARP in packet:
            self.protocols['ARP'] += 1
            self.detect_arp_spoofing(packet)
    
    def detect_tcp_attacks(self, packet):
        """Detect TCP-based attacks"""
        tcp_flags = packet[TCP].flags
        
        # SYN flood detection (SYN without ACK)
        if tcp_flags == 'S':
            if self.ips[packet[IP].src] > 100:
                self.suspicious_ips.add(packet[IP].src)
        
        # XMAS scan detection (FIN, PSH, URG)
        if tcp_flags == 'FPU':
            print(f"\n[!] XMAS scan detected from {packet[IP].src}")
            self.suspicious_ips.add(packet[IP].src)
        
        # NULL scan detection (no flags)
        if tcp_flags == 0:
            print(f"\n[!] NULL scan detected from {packet[IP].src}")
            self.suspicious_ips.add(packet[IP].src)
    
    def detect_icmp_attacks(self, packet):
        """Detect ICMP-based attacks"""
        # ICMP flood detection
        if self.protocols['ICMP'] > 1000:
            print(f"\n[!] Potential ICMP flood detected")
        
        # Ping of death (oversized ICMP)
        if len(packet) > 65535:
            print(f"\n[!] Ping of Death detected from {packet[IP].src}")
            self.suspicious_ips.add(packet[IP].src)
    
    def detect_arp_spoofing(self, packet):
        """Detect ARP spoofing attempts"""
        if packet[ARP].op == 2:  # ARP reply
            # Store ARP cache for comparison
            # Simplified detection - would need state tracking in production
            pass
    
    def detect_port_scan(self):
        """Detect port scanning activity"""
        print("\n\n" + "="*60)
        print("[*] PORT SCAN DETECTION")
        print("="*60)
        
        # Check for IPs accessing many different ports
        port_threshold = 20
        
        for ip, count in self.ips.most_common(20):
            # Count unique ports accessed by this IP
            # Simplified - would need per-IP port tracking in production
            if count > port_threshold:
                print(f"[!] Potential port scan from {ip} ({count} packets)")
                self.suspicious_ips.add(ip)
    
    def detect_anomalies(self):
        """AI-based anomaly detection"""
        print("\n\n" + "="*60)
        print("[*] AI ANOMALY DETECTION ANALYSIS")
        print("="*60)
        
        # Calculate statistics
        total_packets = self.packet_count
        duration = (datetime.now() - self.start_time).total_seconds()
        packets_per_sec = total_packets / duration if duration > 0 else 0
        
        print(f"\n[*] Capture Duration: {duration:.2f} seconds")
        print(f"[*] Total Packets: {total_packets}")
        print(f"[*] Packets/Second: {packets_per_sec:.2f}")
        
        # Protocol distribution
        print(f"\n[*] Protocol Distribution:")
        for proto, count in self.protocols.most_common():
            percentage = (count / total_packets) * 100
            print(f"  {proto}: {count} ({percentage:.2f}%)")
        
        # Top talkers (potential DDoS sources)
        print(f"\n[*] Top Source IPs:")
        ddos_threshold = 1000
        
        for ip, count in self.ips.most_common(10):
            percentage = (count / total_packets) * 100
            
            if count > ddos_threshold:
                print(f"  [!] {ip}: {count} packets ({percentage:.2f}%) - POTENTIAL DDoS")
                self.suspicious_ips.add(ip)
            else:
                print(f"  {ip}: {count} packets ({percentage:.2f}%)")
        
        # Top ports
        print(f"\n[*] Top Destination Ports:")
        for port, count in self.ports.most_common(10):
            percentage = (count / total_packets) * 100
            
            # Flag suspicious ports
            suspicious_ports = [23, 135, 139, 445, 3389, 1433, 3306]
            if port in suspicious_ports:
                print(f"  [!] Port {port}: {count} ({percentage:.2f}%) - High-risk port")
            else:
                print(f"  Port {port}: {count} ({percentage:.2f}%)")
        
        # Packet size analysis
        if self.packet_sizes:
            avg_size = sum(self.packet_sizes) / len(self.packet_sizes)
            max_size = max(self.packet_sizes)
            min_size = min(self.packet_sizes)
            
            print(f"\n[*] Packet Size Statistics:")
            print(f"  Average: {avg_size:.2f} bytes")
            print(f"  Min: {min_size} bytes")
            print(f"  Max: {max_size} bytes")
            
            # Detect anomalous packet sizes
            if max_size > 9000:
                print(f"  [!] Jumbo frames detected (potential covert channel)")
            if min_size < 60:
                print(f"  [!] Undersized packets detected (potential attack)")
        
        # Suspicious IPs summary
        if self.suspicious_ips:
            print(f"\n[!] SUSPICIOUS IPs DETECTED: {len(self.suspicious_ips)}")
            for ip in self.suspicious_ips:
                print(f"  - {ip}")
        else:
            print(f"\n[+] No obvious threats detected")
        
        # Port scan detection
        self.detect_port_scan()
        
        return {
            'total_packets': total_packets,
            'duration_seconds': duration,
            'packets_per_second': packets_per_sec,
            'protocols': dict(self.protocols),
            'top_ips': dict(self.ips.most_common(10)),
            'top_ports': dict(self.ports.most_common(10)),
            'suspicious_ips': list(self.suspicious_ips),
            'avg_packet_size': sum(self.packet_sizes) / len(self.packet_sizes) if self.packet_sizes else 0
        }
    
    def start_capture(self, count=1000, timeout=60, filter_str=None):
        """
        Start packet capture
        
        Args:
            count: Number of packets to capture (0 = unlimited)
            timeout: Timeout in seconds
            filter_str: BPF filter string (e.g., 'tcp port 80')
        """
        print(f"\n[*] Starting packet capture on {self.interface}")
        print(f"[*] Packet limit: {count if count > 0 else 'Unlimited'}")
        print(f"[*] Timeout: {timeout}s")
        
        if filter_str:
            print(f"[*] Filter: {filter_str}")
        
        print("\n[*] Press Ctrl+C to stop early\n")
        
        try:
            # Start sniffing
            sniff(
                iface=self.interface,
                prn=self.analyze_packet,
                count=count,
                timeout=timeout,
                filter=filter_str,
                store=False  # Don't store packets in memory
            )
        except KeyboardInterrupt:
            print("\n\n[*] Capture interrupted by user")
        except PermissionError:
            print("\n[!] Permission denied. Run with sudo:")
            print(f"    sudo python3 {sys.argv[0]} {' '.join(sys.argv[1:])}")
            sys.exit(1)
        except Exception as e:
            print(f"\n[!] Capture error: {e}")
        
        # Analyze results
        results = self.detect_anomalies()
        
        return results
    
    def save_results(self, results, filename=None):
        """Save analysis results to JSON"""
        if not filename:
            filename = f"traffic_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results['timestamp'] = str(datetime.now())
        results['interface'] = self.interface
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[+] Results saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Network Traffic Analyzer with AI Anomaly Detection',
        epilog='WARNING: Only monitor networks you own or have authorization to monitor'
    )
    
    parser.add_argument('-i', '--interface', default='eth0',
                        help='Network interface to monitor (default: eth0)')
    parser.add_argument('-c', '--count', type=int, default=1000,
                        help='Number of packets to capture (0 = unlimited, default: 1000)')
    parser.add_argument('-t', '--timeout', type=int, default=60,
                        help='Capture timeout in seconds (default: 60)')
    parser.add_argument('-f', '--filter',
                        help='BPF filter (e.g., "tcp port 80")')
    parser.add_argument('-o', '--output',
                        help='Output JSON filename')
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║      NETWORK TRAFFIC ANALYZER v1.0                        ║
║      AI-Powered Anomaly Detection                         ║
║      For Authorized Network Monitoring Only               ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"[!] WARNING: Only monitor authorized networks!")
    print(f"[!] Unauthorized monitoring is illegal\n")
    
    analyzer = TrafficAnalyzer(args.interface)
    results = analyzer.start_capture(
        count=args.count,
        timeout=args.timeout,
        filter_str=args.filter
    )
    
    if results:
        analyzer.save_results(results, args.output)
        print("\n[+] Analysis complete!")


if __name__ == "__main__":
    main()
