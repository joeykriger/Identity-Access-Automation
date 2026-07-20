# Portfolio Project: Systems Automation & Access Management Lab

**Role Target:** Systems Administrator / Junior DevOps / IT Support Specialist

**Objective:** To demonstrate competency in local identity management, file system permissions (NTFS & POSIX/ACLs), and task automation using Python. 

## Skills Demonstrated
*   **Operating Systems:** Windows 11 Home & Ubuntu Linux Desktop management.
*   **Security & Permissions:** NTFS inheritance manipulation, Linux standard permissions (chmod/chown) and Advanced Access Control Lists (ACLs).
*   **Automation:** Python scripting (Standard Library) to programmatically manage OS-level users, groups, and permissions.
*   **Troubleshooting:** CompTIA A+ 6-step methodology and OSI Model applied to script execution failures.

---

### Prerequisites
1.  **VirtualBox** installed on the host machine.
2.  **Windows 11 Home** ISO (Installation media).
3.  **Ubuntu Desktop** ISO.
4.  Basic understanding of the Python `subprocess` module and shell execution.

---

## Part 1: Windows 11 Home Scenario

**Scenario Context:** Windows 11 Home lacks the GUI "Local Users and Groups" snap-in (lusrmgr.msc) and advanced GUI security tabs for some folder settings. You must manage 3 new departmental users, group them into a `Finance` group, and establish a secured directory using Python.

### Step 1: Virtual Machine Setup
1.  Create a Windows 11 VM in VirtualBox.
2.  Boot the VM and complete the initial Windows setup.

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
        run_cmd(f"net user {user} [boilerplate_password] /add")
    
    # 2. Create Group and Add Users
    run_cmd("net localgroup Finance /add")
    for user in users:
        run_cmd(f"net localgroup Finance {user} /add")
    
    # 3. Create Directory
    target_dir = r"C:\FinancialInfo"
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
Before running the script, intentionally cause this issue:
**Sabotage (Scripting - OSI Layer 7):** Do not run the command prompt or IDE as Administrator before executing the Python script.

**Troubleshooting Exercise (Apply CompTIA Methodology):**
1.  *Identify:* Script throws "Access is denied" errors.
2.  *Theory:* Lacking elevated privileges for `net user`.
3.  *Test:* Right-click IDE and "Run as Administrator".
4.  *Plan/Implement:* Re-run script from an elevated prompt.
5.  *Verify:* Check `C:\FinancialInfo` properties via command line (`icacls C:\FinancialInfo`).
6.  *Document:* (Use the template at the bottom).

---

## Part 2: Ubuntu Desktop Scenario

**Scenario Context:** You need to rapidly provision access for a development team on a Linux workstation. You will automate user creation, standard POSIX permissions, and advanced Access Control Lists (ACLs) using a Python standard library script.

### Step 1: Virtual Machine Setup
1.  Create an Ubuntu Desktop VM in VirtualBox.
2.  Boot the VM.

### Step 2: Sabotage Setup
Before running the script:

**Sabotage (Permissions - OSI Layer 7):** Create the python file, but remove read/execute permissions intentionally: `chmod 000 lin_setup.py`.

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
1.  *Identify:* Cannot run `python3 lin_setup.py` (Permission denied).
2.  *Theory:* `lin_setup.py` lacks read/execute bits.
3.  *Test:* Run `ls -l lin_setup.py`.
4.  *Plan/Implement:* `chmod 755 lin_setup.py`. 
5.  *Verify:* Run the script with `sudo python3 lin_setup.py` and verify `getfacl` output.
6.  *Document:* Complete the journal.

---

## Documentation & Evidence Requirements

### 1. Evidence Checklist (Screenshots for Portfolio)
*   [ ] Windows: Output of `icacls C:\FinanceData` showing inheritance broken and explicit permissions.
*   [ ] Linux: Output of `getfacl /opt/devproject` showing base permissions and the `backup_svc` ACL.
*   [ ] IDE/Terminal showing successful execution of both Python scripts.

### 2. Troubleshooting Journal Template
*Include this in your GitHub repository or Portfolio presentation to demonstrate your diagnostic methodology.*

| CompTIA Step | "Lab 2: Linux Script Execution Issue" |
| :--- | :--- |
| **1. Identify the Problem** | `python3 lin_setup.py` returns Permission Denied. |
| **2. Establish Theory** | Incorrect file permissions (OSI Layer 7). |
| **3. Test Theory** | `ls -l` shows `----------`. |
| **4. Plan & Implement** | Execute `chmod 744 lin_setup.py`. |
| **5. Verify Functionality**| Script executes and users are created. |
| **6. Document Findings** | Issue resolved. Preventive action: Enforce default umask. |

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
│   ├── win_permissions.png    # icacls output
│   └── lin_acls.png           # getfacl output
└── TROUBLESHOOTING.md         # Completed CompTIA methodology journal
```
