import argparse
import subprocess
import sys
import shutil
from colorama import Fore, Style, init

# Initialize Colorama for cross-platform color support
init(autoreset=True)

class AutoRecon:
    def __init__(self, target):
        self.target = target
        self.common_wordlist = "/usr/share/wordlists/dirb/common.txt"

    def _print_header(self, message):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}[*] {message}")
        print(f"{Fore.CYAN}{'='*60}\n")

    def _check_tool(self, tool_name):
        """Check if a required system tool is installed."""
        if shutil.which(tool_name) is None:
            print(f"{Fore.RED}[!] Error: {tool_name} is not installed or not in PATH.")
            return False
        return True

    def run_command(self, command):
        """Executes a system command and streams output."""
        try:
            process = subprocess.Popen(
                command, 
                shell=False, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True
            )
            for line in process.stdout:
                print(f"{Fore.WHITE}{line.strip()}")
            process.wait()
        except Exception as e:
            print(f"{Fore.RED}[!] An error occurred: {e}")

    def scan_ports(self, version_detect=False):
        if not self._check_tool("nmap"): return
        self._print_header(f"Starting Nmap Port Scan on {self.target}")
        
        flags = "-sV" if version_detect else "-F"
        cmd = ["nmap", flags, self.target]
        self.run_command(cmd)

    def scan_directories(self):
        if not self._check_tool("gobuster"): return
        self._print_header("Starting Directory Discovery (Gobuster)")
        
        # Checking if default wordlist exists
        import os
        if not os.path.exists(self.common_wordlist):
            print(f"{Fore.YELLOW}[!] Wordlist not found at {self.common_wordlist}. Skipping Gobuster.")
            return

        cmd = ["gobuster", "dir", "-u", self.target, "-w", self.common_wordlist, "-q", "-z"]
        self.run_command(cmd)

    def identify_services(self):
        if not self._check_tool("whatweb"): return
        self._print_header("Identifying Web Technologies (WhatWeb)")
        
        cmd = ["whatweb", self.target]
        self.run_command(cmd)

    def find_exploits(self, service):
        if not self._check_tool("searchsploit"): return
        self._print_header(f"Searching Exploits for: {service}")
        
        cmd = ["searchsploit", service]
        self.run_command(cmd)

def main():
    parser = argparse.ArgumentParser(
        description=f"{Fore.GREEN}Auto Recon: Automated Penetration Testing Recon Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("target", help="Target IP address or URL")
    parser.add_argument("-a", "--all", action="store_true", help="Execute all reconnaissance tasks")
    parser.add_argument("-p", "--port", action="store_true", help="Perform a basic port scan")
    parser.add_argument("-pv", "--port-version", action="store_true", help="Perform port scan with version detection")
    parser.add_argument("-s", "--service", action="store_true", help="Run WhatWeb service identification")
    parser.add_argument("-d", "--dir", action="store_true", help="Run Gobuster directory scanning")
    parser.add_argument("-e", "--exploit", metavar="SERVICE", help="Search for exploits for a specific service")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    recon = AutoRecon(args.target)

    # Logic for flag execution
    if args.all:
        recon.scan_ports(version_detect=True)
        recon.identify_services()
        recon.scan_directories()
        print(f"\n{Fore.YELLOW}[!] Manual Search: Use -e to search for specific service versions found.")
    else:
        if args.port:
            recon.scan_ports(version_detect=False)
        if args.port_version:
            recon.scan_ports(version_detect=True)
        if args.service:
            recon.identify_services()
        if args.dir:
            recon.scan_directories()
        if args.exploit:
            recon.find_exploits(args.exploit)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] User interrupted. Exiting...")
        sys.exit(0)