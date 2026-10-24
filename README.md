# 🛡️ Kali AI Security Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94.svg)](https://www.kali.org/)

**AI-enhanced penetration testing toolkit for Kali Linux with automated reconnaissance, port scanning, exploit analysis & traffic monitoring**

⚠️ **FOR AUTHORIZED USE ONLY** - Only use on systems you own or have explicit written permission to test.

---

## 🚀 Features

### 🔍 AI-Enhanced Port Scanner
- **Full 65535 port scanning** with service detection
- **AI-powered vulnerability analysis** with severity ratings
- **Automated recommendations** for discovered services
- Support for stealth, quick, and comprehensive scans
- JSON output for integration with other tools

### 🌐 Automated Reconnaissance Framework
- **Multi-tool integration**: nmap, sublist3r, amass, subfinder
- **DNS enumeration** with all record types
- **WHOIS lookups** and domain intelligence
- **Web crawling** with gospider/hakrawler
- **Comprehensive reporting** in JSON format

### 💥 AI Exploit Suggester
- **Exploit-DB integration** for vulnerability research
- **AI severity analysis** (CRITICAL/HIGH/MEDIUM/LOW)
- **CVE lookup** and cross-referencing
- **Risk scoring** (0-100) with actionable recommendations
- Platform-specific filtering (Linux/Windows/macOS)

### 📡 Network Traffic Analyzer
- **Real-time packet capture** with scapy
- **AI anomaly detection** for DDoS, port scans, and attacks
- **Protocol analysis** and distribution statistics
- **Attack pattern detection**: SYN flood, XMAS scan, NULL scan
- **BPF filtering** for targeted monitoring

---

## 📦 Installation

### Quick Start (Kali Linux)

```bash
# Clone the repository
git clone https://github.com/Janrahat/kali-ai-security-toolkit.git
cd kali-ai-security-toolkit

# Install system dependencies
sudo apt update
sudo apt install nmap python3-pip python3-scapy -y

# Install Python dependencies
pip3 install -r requirements.txt

# Make tools executable
chmod +x tools/*.py
```

### Full Installation

See [Installation Guide](docs/installation.md) for complete setup instructions.

---

## 🔧 Usage

### AI Port Scanner

```bash
# Full scan (all 65535 ports)
python3 tools/ai_port_scanner.py 192.168.1.1

# Quick scan
python3 tools/ai_port_scanner.py example.com --type quick

# Save results
python3 tools/ai_port_scanner.py 10.0.0.5 -o scan_results.json
```

### Reconnaissance Framework

```bash
# Full reconnaissance
python3 tools/recon_framework.py example.com

# Specific modules only
python3 tools/recon_framework.py target.com -m nmap subdomain dns
```

### Exploit Suggester

```bash
# Search for exploits
python3 tools/exploit_suggester.py -s Apache -v 2.4.49

# Platform-specific
python3 tools/exploit_suggester.py -s OpenSSH -v 7.2 -p linux

# CVE lookup
python3 tools/exploit_suggester.py -s nginx -v 1.18.0 -c CVE-2021-XXXXX
```

### Traffic Analyzer

```bash
# Monitor network (requires sudo)
sudo python3 tools/traffic_analyzer.py -i eth0

# Filter specific traffic
sudo python3 tools/traffic_analyzer.py -f "tcp port 80"

# Capture and analyze
sudo python3 tools/traffic_analyzer.py -c 5000 -o traffic_report.json
```

See [Usage Guide](docs/usage.md) for detailed examples and workflows.

---

## 📁 Repository Structure

```
kali-ai-security-toolkit/
├── tools/
│   ├── ai_port_scanner.py       # AI-enhanced port scanner
│   ├── recon_framework.py       # Automated reconnaissance
│   ├── exploit_suggester.py     # Exploit research tool
│   └── traffic_analyzer.py      # Network traffic analyzer
├── docs/
│   ├── installation.md          # Installation guide
│   ├── usage.md                 # Usage examples
│   └── legal_disclaimer.md      # Legal information
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # This file
```

---

## 🎯 Use Cases

### Authorized Penetration Testing
- Network infrastructure assessments
- Web application security testing
- Vulnerability assessments
- Red team operations

### Bug Bounty Hunting
- Subdomain discovery
- Service enumeration
- CVE research
- Attack surface mapping

### Security Operations
- Network monitoring
- Threat detection
- Incident response
- Security auditing

### Education & Research
- Cybersecurity training
- CTF competitions
- Lab environments (HackTheBox, TryHackMe)
- Security research

---

## 📊 Output Examples

### Port Scanner Output
```
[*] VULNERABILITY SUMMARY
Critical: 2
High: 5
Medium: 3
Total services found: 15

[!] CRITICAL: Insecure legacy service telnet on port 23 - DISABLE IMMEDIATELY
[!] HIGH: RDP exposed on port 3389 - Enable NLA, use VPN, strong passwords
```

### Reconnaissance Output
```
recon_example_com_20261024_120000/
├── nmap.xml              # Full nmap results
├── subdomains.txt        # 47 subdomains found
├── dns_records.txt       # A, MX, NS, TXT records
├── whois.txt            # Domain registration info
└── recon_summary.json   # Complete summary
```

---

## ⚖️ Legal & Ethical Use

### ⚠️ IMPORTANT WARNING

**You MUST have explicit written authorization before using these tools on any system you do not own.**

Unauthorized use may result in:
- Criminal prosecution
- Civil lawsuits  
- Imprisonment
- Significant fines

### Legal Framework
- Computer Fraud and Abuse Act (CFAA) - USA
- General Data Protection Regulation (GDPR) - EU
- Computer Misuse Act - UK
- Budapest Convention on Cybercrime
- Local cybercrime laws

### ✅ Authorized Use
- Your own systems/networks
- Written penetration testing contracts
- Bug bounty programs (within scope)
- Educational labs (CTF, HackTheBox, etc.)
- Employer-authorized testing

### ❌ Unauthorized Use
- Scanning networks without permission
- "Helping" websites find vulnerabilities
- Testing school/work systems without approval
- Any illegal activity

**Read the full [Legal Disclaimer](docs/legal_disclaimer.md) before use.**

---

## 🛠️ Requirements

- **OS**: Kali Linux 2020.1+ (or Debian-based Linux)
- **Python**: 3.7+
- **Root**: Required for traffic analyzer
- **Dependencies**: nmap, scapy, requests, colorama

See [Installation Guide](docs/installation.md) for details.

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- All tools remain ethical and legal
- Code follows PEP 8 style guidelines
- Documentation is updated
- Legal warnings are preserved

```bash
# Fork the repository
# Create feature branch
git checkout -b feature/new-tool

# Make changes and test
# Commit and push
git push origin feature/new-tool

# Create Pull Request
```

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Disclaimer
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY. Authors are NOT liable for any misuse, damage, or legal consequences. **You are solely responsible for your actions.**

---

## 👤 Author

**Created by:** [@Janrahat](https://github.com/Janrahat)

**Purpose:** Legitimate penetration testing and security research

---

## 🙏 Acknowledgments

- [Exploit-DB](https://www.exploit-db.com/) for vulnerability database
- [Nmap](https://nmap.org/) for port scanning
- [Scapy](https://scapy.net/) for packet manipulation
- Kali Linux community for security tools

---

## 📚 Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Penetration Testing Execution Standard](http://www.pentest-standard.org/)
- [Bug Bounty Platforms](https://www.bugcrowd.com/)
- [Cybersecurity Training](https://www.hackthebox.com/)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Janrahat/kali-ai-security-toolkit/issues)
- **Documentation**: [Wiki](https://github.com/Janrahat/kali-ai-security-toolkit/wiki) *(coming soon)*
- **Discussions**: [GitHub Discussions](https://github.com/Janrahat/kali-ai-security-toolkit/discussions) *(coming soon)*

---

## ⭐ Star History

If you find this toolkit useful, please consider giving it a star! ⭐

---

## 🔒 Security

If you discover a security vulnerability in this toolkit, please report it privately via GitHub Security Advisories.

---

**Remember: With great power comes great responsibility. Always get authorization. Use ethically.**

---

*Last Updated: October 24, 2026*
