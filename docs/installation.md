# Installation Guide

## Prerequisites

### System Requirements
- **Operating System**: Kali Linux 2020.1+ (or Debian-based Linux)
- **Python**: 3.7 or higher
- **Root Access**: Required for packet capture and some scans
- **Internet Connection**: Required for exploit database searches

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Janrahat/kali-ai-security-toolkit.git
cd kali-ai-security-toolkit
```

### 2. Install System Dependencies

```bash
# Update package list
sudo apt update

# Install nmap
sudo apt install nmap -y

# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Install scapy system dependencies
sudo apt install python3-scapy -y

# Optional: Additional recon tools
sudo apt install sublist3r whois dnsutils -y

# Optional: Web crawling tools (Go required)
# Install Go first
sudo apt install golang -y

# Install gospider
go install github.com/jaeles-project/gospider@latest

# Add Go bin to PATH
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### 3. Install Python Dependencies

```bash
# Install required Python packages
pip3 install -r requirements.txt

# Or install individually
pip3 install python-nmap scapy requests colorama
```

### 4. Verify Installation

```bash
# Check Python version
python3 --version

# Check nmap
nmap --version

# Check scapy
python3 -c "from scapy.all import *; print('Scapy OK')"

# Make tools executable
chmod +x tools/*.py
```

---

## Tool-Specific Setup

### AI Port Scanner
```bash
# Test installation
python3 tools/ai_port_scanner.py --help

# No additional setup required
```

### Reconnaissance Framework
```bash
# Install optional tools for full functionality
sudo apt install sublist3r amass subfinder -y

# Test
python3 tools/recon_framework.py --help
```

### Exploit Suggester
```bash
# Requires internet connection only
python3 tools/exploit_suggester.py --help
```

### Traffic Analyzer
```bash
# Requires root for packet capture
sudo python3 tools/traffic_analyzer.py --help

# Grant capabilities to Python (optional, allows non-root capture)
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

---

## Troubleshooting

### "Nmap not found" Error
```bash
sudo apt install nmap
```

### "Scapy not found" Error
```bash
sudo apt install python3-scapy
pip3 install scapy
```

### "Permission denied" on Traffic Analyzer
```bash
# Run with sudo
sudo python3 tools/traffic_analyzer.py -i eth0

# Or grant capabilities
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

### "Module not found" Errors
```bash
# Reinstall all dependencies
pip3 install --upgrade -r requirements.txt
```

---

## Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# When finished
deactivate
```

---

## Docker Installation (Alternative)

```bash
# Build Docker image
docker build -t kali-ai-toolkit .

# Run container
docker run -it --net=host --privileged kali-ai-toolkit

# Note: Requires Dockerfile (not included yet)
```

---

## Upgrade

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip3 install --upgrade -r requirements.txt
```

---

## Verification Tests

```bash
# Test all tools
python3 tools/ai_port_scanner.py --help
python3 tools/recon_framework.py --help
python3 tools/exploit_suggester.py --help
sudo python3 tools/traffic_analyzer.py --help
```

---

## Next Steps

- Read [Usage Guide](usage.md)
- Review [Legal Disclaimer](legal_disclaimer.md)
- Start with authorized testing only!
