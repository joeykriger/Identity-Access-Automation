Troubleshooting Journal

| CompTIA Steps | Lab 1: Windows Script Execution Issue |
| :--- | :--- |
| **1. Identify the Problem** | Access denied when attempting to run `python3 .\scripts\win_setup.py`. |
| **2. Establish Theory** | Lacking elevated privileges for `net LabAdmin`. |
| **3. Test Theory** | Right-clicked VS Code and selected "Run as Administrator". |
| **4. Plan & Implement** | Re-ran script as an Admin. |
| **5. Verify Functionality** | Running net user and net localgroup confirms the users and group were created. Running `icacls C:\FinancialInfo` returns correct permissions assigned.  |
| **6. Document Findings** | Issue resolved. Preventive action: ensure terminal is running as Admin before running script. |