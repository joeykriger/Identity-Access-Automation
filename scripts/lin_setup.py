import subprocess
import os

def run_cmd(cmd:)
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output = True, text = True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout.strip()}")

def main():
    # Creates the group
    run_cmd(["sudo", "groupadd", "devteam"])

    # Creates users and adds them to the group
    users = ["dave", "eve", "frank"]
    for user in users:
        run_cmd(["sudo", "useradd", "-m", "-G", "devteam", "-s", "/bin/bash", user])

    # Creates the directory and sets standard permissions
    target_dir = "/opt/devproject"
    run_cmd(["sudo", "mkdir", "-p", target_dir])
    run_cmd(["sudo", "chown", "root:devteam", target_dir])
    run_cmd(["sudo", "chmod", "770", target_dir]) # rwx for Owner and Group, and nothing for Others

    # Creates and gives a specific non-group user (named backup_svc) read-only access
    run_cmd(["sudo", "useradd", "-M", "-s", "/usr/sbin/nologin", "backup_svc"])
    run_cmd(["sudo", "setfacl", "-m", "u:backup_svc:r-x", target_dir])

    # Verifies ACLs
    print("--- Current ACLs ---")
    run_cmd(["getfacl", target_dir])

if __name__ == "__main__":
    main()