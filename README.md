# ad-principals

**ad-principals** is a lightweight Python utility designed for Red Teamers and Penetration Testers to generate Active Directory `sAMAccountName` and `UserPrincipalName` permutations from raw name lists.

It is specifically optimized for identifying valid domain principals during the enumeration phase of an internal assessment or an Active Directory lab (e.g., Hack The Box, TryHackMe).

## Features
- **AD Compliance**: Automatically enforces the 20-character `sAMAccountName` limit.
- **Flexible Input**: Supports both `.txt` (raw names) and `.csv` (auto-detects 'Name' columns).
- **Format Coverage**: Generates 10+ standard corporate naming variations (e.g., `jmarston`, `john.m`, `marston.j`).
- **Sanitized Output**: Removes non-alphanumeric characters to prevent Kerberos protocol errors.

## Installation
Clone the repository and install the minimal requirements:
```bash
git clone [https://github.com/bishwabikash/ad-principals.git](https://github.com/bishwabikash/ad-principals.git)
cd ad-principals
pip3 install -r requirements.txt


## Execution
### Make Sure you don't keep in the Downloads Folder
chmod +x ad-principals.py
sudo ln -s $(pwd)/ad-principals.py /usr/local/bin/ad-principals


Made with <3 and VibeCoding
