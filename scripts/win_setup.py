import subprocess
import os

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell = True, capture_output = True, text = True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")

def main():
    # Creates the users
    users = ["Alice", "Bob", "Charlie"]
    for user in users:
        run_cmd(f"net user {user} [password] /add")

    # Creates the group and adds the users
    run_cmd("net localgroup Finance /add")
    for user in users:
        run_cmd(f"net localgroup Finance {user} /add")

    # Creates the directory
    target_dir = r"C:\FinancialInfo"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created {target_dir}")

    # NTFS Permissions
    run_cmd(f"icacls {target_dir} /inheritance:r")
    run_cmd(f"icacls {target_dir} /grant Administratators:(OI)(CI)F")
    run_cmd(f"icacls {target_dir} /grant Finance:(OI)(CI)M")

if __name__ == "__main__":
    main()