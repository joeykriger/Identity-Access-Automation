Troubleshooting Journal

| CompTIA Steps | Lab 2: Linux Script Execution Issue |
| :--- | :--- |
| **1. Identify the Problem** Permission denied when attempting to run `python3 scripts/lin_setup.py`. |
| **2. Establish Theory** | Permissions for `lin_setup.py` are misconfigured. |
| **3. Test Theory** | Run `ls -l scripts/lin_setup.py`; returns `---------- 1 joebrosmith joebrosmith 1235 Jul 20 11:44 scripts/lin_setup.py`. |
| **4. Plan & Implement** | Run `chmod 744 scripts/lin_setup.py`. |
| **5. Verify Functionality** | Script executes and users are created. |
| **6. Document Findings** | Issue resolved. Preventive action: Enforce default umask. |