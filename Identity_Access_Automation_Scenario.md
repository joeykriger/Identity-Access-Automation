# Portfolio Project: Systems Automation & Access Management Lab

**Role Target:** Systems Administrator / Junior DevOps / IT Support Specialist

**Objective:** To demonstrate competency in local identity management, file system permissions (NTFS & POSIX/ACLs), internal network configuration, and task automation using Python, all within isolated virtualized environments. 

## Skills Demonstrated
*   **Networking:** Virtual network isolation (VirtualBox Internal Networks), static IP configuration, OSI Model troubleshooting.
*   **Operating Systems:** Windows 11 Home & Ubuntu Linux Desktop management.
*   **Security & Permissions:** NTFS inheritance manipulation, Linux standard permissions (chmod/chown) and Advanced Access Control Lists (ACLs).
*   **Automation:** Python scripting (Standard Library) to programmatically manage OS-level users, groups, and permissions.
*   **Troubleshooting:** CompTIA A+/Network+ 6-step methodology applied to network and script execution failures.

---

## Lab Architecture & Prerequisites

### Architecture Diagram
```text
[ Physical Host (Isolated, no host-to-guest traffic) ]
      |
      |-- VirtualBox Hypervisor
            |
            |=== [ Internal Network: "LabNet" ] ===|
            |                                      |
     [ Windows 11 Home VM ]                [ Ubuntu Desktop VM ]
     IP: 192.168.10.20/24                  IP: 192.168.10.10/24
     Gateway: None (Isolated)              Gateway: None (Isolated)
```

### Prerequisites
1.  **VirtualBox** installed on the host machine.
2.  **Windows 11 Home** ISO (Installation media).
3.  **Ubuntu Desktop** ISO.
4.  Basic understanding of the Python `subprocess` module and shell execution.

---

## Part 1: Windows 11 Home Scenario

**Scenario Context:** Windows 11 Home lacks the GUI "Local Users and Groups" snap-in (lusrmgr.msc) and advanced GUI security tabs for some folder settings. You must manage 3 new departmental users, group them into a `Finance` group, and establish a secured directory using Python.

### Step 1: Virtual Machine & Network Setup
1.  Create a Windows 11 VM in VirtualBox.
2.  Under VM Settings -> Network:
    *   Change Adapter 1 to **Internal Network**.
    *   Set the Name to `LabNet`.
3.  Boot the VM and complete the initial Windows setup.
4.  **Networking Sabotage (Intentional):**
    *   Set the IP manually, but use the wrong subnet mask (e.g., `255.255.255.128`) instead of `/24` (`255.255.255.0`).
    *   *Do not fix this immediately. This is part of the troubleshooting lab.*

### Step 2: The Python Automation Script
Create a file named `win_setup.py` on the Desktop. This script uses the Python standard library to bypass Windows 11 Home GUI limitations.

```python
import subprocess
import os

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")

def main():
    # 1. Create Users
    users = ["Alice", "Bob", "Charlie"]
    for user in users:
        run_cmd(f"net user {user} Password123! /add")
    
    # 2. Create Group and Add Users
    run_cmd("net localgroup Finance /add")
    for user in users:
        run_cmd(f"net localgroup Finance {user} /add")
    
    # 3. Create Directory
    target_dir = r"C:\FinanceData"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created {target_dir}")
    
    # 4. NTFS Permissions: Break inheritance, grant Finance group read/write, deny others
    # /inheritance:r removes inherited permissions. 
    # /grant grants specific permissions (OI=Object Inherit, CI=Container Inherit, M=Modify)
    run_cmd(f"icacls {target_dir} /inheritance:r")
    run_cmd(f"icacls {target_dir} /grant Administrators:(OI)(CI)F")
    run_cmd(f"icacls {target_dir} /grant Finance:(OI)(CI)M")

if __name__ == "__main__":
    main()
```

### Step 3: Beginner Sabotage & Troubleshooting
Before running the script, intentionally cause these issues:
1.  **Sabotage 1 (Scripting - OSI Layer 7):** Do not run the command prompt or IDE as Administrator before executing the Python script.
2.  **Sabotage 2 (Networking - OSI Layer 3):** Ping the Ubuntu VM (`192.168.10.10`). It will fail due to the subnet mask sabotage from Step 1.

**Troubleshooting Exercise (Apply CompTIA Methodology):**
1.  *Identify:* Script throws "Access is denied" errors; Ping to `192.168.10.10` returns "Destination host unreachable."
2.  *Theory:* Lacking elevated privileges for `net user`; Subnet mask configuration isolates the host on Layer 3.
3.  *Test:* Check `ipconfig /all`; right-click IDE and "Run as Administrator".
4.  *Plan/Implement:* Correct Subnet mask to `255.255.255.0`; Re-run script from an elevated prompt.
5.  *Verify:* Check `C:\FinanceData` properties via command line (`icacls C:\FinanceData`) and verify ping succeeds.
6.  *Document:* (Use the template at the bottom).

---

## Part 2: Ubuntu Desktop Scenario

**Scenario Context:** You need to rapidly provision access for a development team on a Linux workstation. You will automate user creation, standard POSIX permissions, and advanced Access Control Lists (ACLs) using a Python standard library script.

### Step 1: Virtual Machine & Network Setup
1.  Create an Ubuntu Desktop VM in VirtualBox.
2.  Under VM Settings -> Network:
    *   Change Adapter 1 to **Internal Network**.
    *   Set the Name to `LabNet`.
3.  Boot the VM and configure the IP address dynamically, then move to static.
4.  **Setup the static IP (`192.168.10.10/24`)**:
    *   Edit Network connections via GUI or Netplan. 

### Step 2: Sabotage Setup
Before running the script:
1.  **Sabotage 1 (Networking - OSI Layer 1/2):** In VirtualBox settings for the Ubuntu VM, go to Network -> Advanced -> **Uncheck "Cable Connected"**.
2.  **Sabotage 2 (Permissions - OSI Layer 7):** Create the python file, but remove read/execute permissions intentionally: `chmod 000 lin_setup.py`.

### Step 3: The Python Automation Script
Create `lin_setup.py`.

```python
import subprocess
import os

def run_cmd(cmd):
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout.strip()}")

def main():
    # 1. Create Group
    run_cmd(["sudo", "groupadd", "devteam"])
    
    # 2. Create Users and add to group
    users = ["dave", "eve", "frank"]
    for user in users:
        run_cmd(["sudo", "useradd", "-m", "-G", "devteam", "-s", "/bin/bash", user])
    
    # 3. Create Directory & Standard Permissions (chown/chmod)
    target_dir = "/opt/devproject"
    run_cmd(["sudo", "mkdir", "-p", target_dir])
    run_cmd(["sudo", "chown", "root:devteam", target_dir])
    run_cmd(["sudo", "chmod", "770", target_dir]) # rwx for owner and group, nothing for others
    
    # 4. Advanced ACLs (setfacl)
    # Give a specific non-group user (e.g., a service account named 'backup_svc') read-only access.
    run_cmd(["sudo", "useradd", "-M", "-s", "/usr/sbin/nologin", "backup_svc"])
    run_cmd(["sudo", "setfacl", "-m", "u:backup_svc:r-x", target_dir])
    
    # Verify ACLs
    print("--- Current ACLs ---")
    run_cmd(["getfacl", target_dir])

if __name__ == "__main__":
    main()
```

### Step 4: Troubleshooting Exercise
1.  *Identify:* Cannot run `python3 lin_setup.py` (Permission denied); Cannot ping Windows VM at `192.168.10.20`.
2.  *Theory:* `lin_setup.py` lacks read/execute bits. Virtual interface is down (Layer 1 physical link issue).
3.  *Test:* Run `ls -l lin_setup.py`. Check interface status with `ip link show`.
4.  *Plan/Implement:* `chmod 755 lin_setup.py`. Re-check "Cable Connected" in VirtualBox settings.
5.  *Verify:* Ping Windows VM successfully. Run the script with `sudo python3 lin_setup.py` and verify `getfacl` output.
6.  *Document:* Complete the journal.

---

## Documentation & Evidence Requirements

### 1. Evidence Checklist (Screenshots for Portfolio)
*   [ ] VirtualBox Network settings showing `LabNet` Internal Network for both VMs.
*   [ ] Windows: Command Prompt showing successful `ping 192.168.10.10`.
*   [ ] Windows: Output of `icacls C:\FinanceData` showing inheritance broken and explicit permissions.
*   [ ] Linux: Terminal showing successful `ping 192.168.10.20`.
*   [ ] Linux: Output of `getfacl /opt/devproject` showing base permissions and the `backup_svc` ACL.
*   [ ] IDE/Terminal showing successful execution of both Python scripts.

### 2. Troubleshooting Journal Template
*Include this in your GitHub repository or Portfolio presentation to demonstrate your diagnostic methodology.*

| CompTIA Step | Lab 1: Windows Connectivity Issue | Lab 2: Linux Script Execution Issue |
| :--- | :--- | :--- |
| **1. Identify the Problem** | Ping to 192.168.10.10 fails. | `python3 lin_setup.py` returns Permission Denied. |
| **2. Establish Theory** | Incorrect IP configuration (OSI Layer 3). | Incorrect file permissions (OSI Layer 7). |
| **3. Test Theory** | `ipconfig` shows mask as 255.255.255.128. | `ls -l` shows `----------`. |
| **4. Plan & Implement** | Change subnet mask to 255.255.255.0. | Execute `chmod 744 lin_setup.py`. |
| **5. Verify Functionality**| Ping succeeds. | Script executes and users are created. |
| **6. Document Findings** | Issue resolved. Preventive action: Review IP deployment policies. | Issue resolved. Preventive action: Enforce default umask. |

---

### Suggested GitHub Repository Structure
If publishing to GitHub, organize your repository as follows:
```text
/HomeLab-Identity-Automation
│
├── README.md                  # Use the Introduction and Skills Demonstrated from this document
├── /scripts
│   ├── win_setup.py           # Windows automation script
│   └── lin_setup.py           # Linux automation script
├── /evidence
│   ├── network_config.png     # Ping tests and LabNet settings
│   ├── win_permissions.png    # icacls output
│   └── lin_acls.png           # getfacl output
└── TROUBLESHOOTING.md         # Completed CompTIA methodology journal
```
