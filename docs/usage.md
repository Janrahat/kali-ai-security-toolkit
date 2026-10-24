# Usage Guide

Complete usage examples for all tools in the Kali AI Security Toolkit.

---

## 🔍 AI Port Scanner

### Basic Usage

```bash
# Scan single host (all 65535 ports)
python3 tools/ai_port_scanner.py 192.168.1.1

# Scan with specific port range
python3 tools/ai_port_scanner.py 192.168.1.1 -p 1-1000

# Quick scan (common ports only)
python3 tools/ai_port_scanner.py 192.168.1.1 --type quick

# Stealth scan
python3 tools/ai_port_scanner.py 192.168.1.1 --type stealth

# Save results to custom file
python3 tools/ai_port_scanner.py 192.168.1.1 -o results.json
```

### Examples

```bash
# Full scan of web server
python3 tools/ai_port_scanner.py example.com

# Scan specific ports
python3 tools/ai_port_scanner.py 10.0.0.5 -p 80,443,22,21

# Scan with output
python3 tools/ai_port_scanner.py 192.168.1.100 -o server_scan.json
```

### Output
- Terminal: Real-time scan results with AI vulnerability analysis
- JSON file: Complete results with severity ratings and recommendations

---

## 🌐 Reconnaissance Framework

### Basic Usage

```bash
# Full reconnaissance of domain
python3 tools/recon_framework.py example.com

# Quick scan only
python3 tools/recon_framework.py example.com --type quick

# Specific modules only
python3 tools/recon_framework.py example.com -m nmap subdomain

# Custom output directory
python3 tools/recon_framework.py example.com -o my_recon_results
```

### Module Options

```bash
# Run only nmap
python3 tools/recon_framework.py target.com -m nmap

# Run subdomain + DNS enumeration
python3 tools/recon_framework.py target.com -m subdomain dns

# All available modules
python3 tools/recon_framework.py target.com -m nmap subdomain dns whois web
```

### Examples

```bash
# Full recon on corporate domain
python3 tools/recon_framework.py company.com

# Quick web app assessment
python3 tools/recon_framework.py webapp.net -m nmap web

# Network infrastructure mapping
python3 tools/recon_framework.py 192.168.1.0/24 -m nmap dns
```

### Output Structure
```
recon_example_com_20261024_120000/
├── nmap.xml
├── nmap.nmap
├── nmap.gnmap
├── subdomains.txt
├── dns_records.txt
├── whois.txt
├── spider/
└── recon_summary.json
```

---

## 💥 Exploit Suggester

### Basic Usage

```bash
# Search for exploits
python3 tools/exploit_suggester.py -s Apache -v 2.4.49

# Platform-specific search
python3 tools/exploit_suggester.py -s OpenSSH -v 7.2 -p linux

# Filter by exploit type
python3 tools/exploit_suggester.py -s vsftpd -v 2.3.4 -t remote

# CVE lookup
python3 tools/exploit_suggester.py -s Apache -v 2.4.49 -c CVE-2021-41773
```

### Examples

```bash
# Web server vulnerabilities
python3 tools/exploit_suggester.py -s Apache -v 2.4.49
python3 tools/exploit_suggester.py -s nginx -v 1.18.0

# SSH vulnerabilities
python3 tools/exploit_suggester.py -s OpenSSH -v 7.2p2 -p linux

# Database vulnerabilities
python3 tools/exploit_suggester.py -s MySQL -v 5.7.29

# Windows-specific
python3 tools/exploit_suggester.py -s SMB -v 1.0 -p windows
```

### Exploit Types
- `remote`: Remote code execution
- `local`: Local privilege escalation
- `webapps`: Web application vulnerabilities
- `dos`: Denial of service

### Output
- Exploit-DB links with EDB-IDs
- AI severity analysis (CRITICAL/HIGH/MEDIUM/LOW)
- Risk score (0-100)
- Specific recommendations
- JSON results file

---

## 📡 Network Traffic Analyzer

### Basic Usage

⚠️ **Requires root/sudo**

```bash
# Capture 1000 packets on eth0
sudo python3 tools/traffic_analyzer.py

# Specific interface
sudo python3 tools/traffic_analyzer.py -i wlan0

# Unlimited capture with 60s timeout
sudo python3 tools/traffic_analyzer.py -c 0 -t 60

# Capture with BPF filter
sudo python3 tools/traffic_analyzer.py -f "tcp port 80"

# Save results
sudo python3 tools/traffic_analyzer.py -o traffic_report.json
```

### Filter Examples

```bash
# HTTP traffic only
sudo python3 tools/traffic_analyzer.py -f "tcp port 80"

# HTTPS traffic
sudo python3 tools/traffic_analyzer.py -f "tcp port 443"

# Specific host
sudo python3 tools/traffic_analyzer.py -f "host 192.168.1.100"

# SSH traffic
sudo python3 tools/traffic_analyzer.py -f "tcp port 22"

# DNS queries
sudo python3 tools/traffic_analyzer.py -f "udp port 53"

# Exclude SSH (monitor everything except SSH)
sudo python3 tools/traffic_analyzer.py -f "not tcp port 22"
```

### Advanced Examples

```bash
# Monitor web server traffic for 5 minutes
sudo python3 tools/traffic_analyzer.py -i eth0 -c 0 -t 300 -f "tcp port 80 or tcp port 443"

# Detect port scans (capture many packets, short timeout)
sudo python3 tools/traffic_analyzer.py -c 5000 -t 30

# Monitor specific subnet
sudo python3 tools/traffic_analyzer.py -f "net 192.168.1.0/24"
```

### AI Detection Features
- DDoS detection (high packet rates from single IP)
- Port scan detection (many ports accessed)
- Protocol anomalies (unusual distributions)
- Attack patterns (SYN flood, XMAS scan, NULL scan)
- ICMP flood detection
- Suspicious packet sizes

---

## 🔗 Combining Tools (Workflow Examples)

### Web Application Assessment

```bash
# 1. Reconnaissance
python3 tools/recon_framework.py target.com -m subdomain dns web

# 2. Port scan discovered hosts
python3 tools/ai_port_scanner.py target.com

# 3. Check for exploits on discovered services
python3 tools/exploit_suggester.py -s Apache -v 2.4.50

# 4. Monitor traffic during testing
sudo python3 tools/traffic_analyzer.py -f "host target.com"
```

### Network Penetration Test

```bash
# 1. Full network scan
python3 tools/ai_port_scanner.py 10.0.0.0/24

# 2. Deep recon on discovered hosts
python3 tools/recon_framework.py 10.0.0.5

# 3. Traffic analysis
sudo python3 tools/traffic_analyzer.py -i eth0 -c 2000

# 4. Exploit research for found services
python3 tools/exploit_suggester.py -s vsftpd -v 2.3.4
```

### Bug Bounty Workflow

```bash
# 1. Subdomain discovery
python3 tools/recon_framework.py target.com -m subdomain

# 2. Port scan all subdomains
cat recon_*/subdomains.txt | while read sub; do
    python3 tools/ai_port_scanner.py "$sub" -o "scan_$sub.json"
done

# 3. Web crawling
python3 tools/recon_framework.py target.com -m web

# 4. CVE research
python3 tools/exploit_suggester.py -s nginx -v 1.19.0
```

---

## 📊 Output Files

### Port Scanner JSON
```json
{
  "timestamp": "2026-10-24 10:30:00",
  "services": [...],
  "vulnerabilities": [...],
  "summary": {
    "critical": 2,
    "high": 5,
    "medium": 3
  }
}
```

### Recon Summary JSON
```json
{
  "target": "example.com",
  "timestamp": "2026-10-24 10:30:00",
  "scans_completed": [...]
}
```

---

## ⚠️ Important Notes

1. **Authorization Required**: Only test systems you own or have written permission to test
2. **Root Access**: Traffic analyzer requires sudo/root
3. **Network Impact**: Full port scans can be detected by IDS/IPS
4. **Rate Limiting**: Exploit-DB searches are rate-limited
5. **Legal Compliance**: Follow all local laws and regulations

---

## 🆘 Common Issues

### "Permission denied" on traffic analyzer
```bash
sudo python3 tools/traffic_analyzer.py -i eth0
```

### "Nmap not found"
```bash
sudo apt install nmap
```

### No subdomains found
- Tool may not be installed: `sudo apt install sublist3r`
- Domain may have no public subdomains
- Rate limiting by search engines

### Slow scans
- Use `--type quick` for faster scans
- Reduce port range with `-p 1-1000`
- Check network bandwidth

---

## 📚 Additional Resources

- [Installation Guide](installation.md)
- [Legal Disclaimer](legal_disclaimer.md)
- [Exploit-DB](https://www.exploit-db.com/)
- [CVE Details](https://www.cvedetails.com/)
