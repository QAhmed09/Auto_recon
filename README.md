# Auto recon

at first you should have python,nmap,gobuster and whatweb

second you can download the Auto_recon.py tool

in Linux/MacOS go to CLI (Termenal) and write 

`git clone git@github.com:QAhmed09/Auto_recon.git`

`cd Auto_recon`

`chmod +x Auto_recon.py`

Now you should know all the commands:

- `-h, --help`
Displays the help menu and shows how to use all available commands.
- `-a, --all`
Runs a full reconnaissance scan (Port scanning, service versions, directory scanning, and web technology analysis all together).
- `-p, --port`
Runs a quick and basic nmap port scan to find open ports on the target host.
- `-pv, --port-version`
Scans open ports and detects the exact service versions running on them.
- `-s, --service`
Uses whatweb to analyze web technologies, application headers, and CMS of the target website.
- `-e, --exploit` 
Searches the local searchsploit database for vulnerabilities matching the specific service or version you type.

IMPORTANT: Manual Code Modification Required

Inside the `Auto_recon.py` script, the paths for specific tools and wordlists (such as the Gobuster wordlist) are hardcoded and automatically chosen by the tool itself.

like :

in the 13th line

        `self.common_wordlist = "/usr/share/wordlists/dirb/common.txt”`

It is **absolutely necessary** to open the Python file and manually modify these paths to match your own operating system environment (Kali Linux, Parrot OS, etc.) before running the tool. Failing to change these hardcoded paths will result in command or file not found errors.
