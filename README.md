# ad-principals

**ad-principals** is a lightweight, standalone Python utility designed for Red Teamers and Security Auditors to generate Active Directory `sAMAccountName` and `UserPrincipalName` (UPN) permutations from raw name lists.

It is specifically optimized for identifying valid domain principals during the enumeration phase of an internal assessment or an Active Directory lab (e.g., Hack The Box, TryHackMe).

---

## Features
- **AD Compliance**: Automatically enforces the **20-character** `sAMAccountName` limit for legacy compatibility.
- **Sanitized Output**: Removes non-alphanumeric characters (apostrophes, hyphens) to prevent Kerberos protocol errors.
- **Flexible Input**: Native support for `.txt` (raw names) and `.csv` (auto-detects 'Name' or 'Full Name' columns).
- **Format Coverage**: Generates 10+ standard corporate naming variations (e.g., `jmarston`, `john.m`, `marston.j`).

---

## Installation
Clone the repository and install the minimal requirements:

```bash
git clone [https://github.com/bishwabikash/ad-principals.git](https://github.com/bishwabikash/ad-principals.git)
cd ad-principals
pip3 install -r requirements.txt

```

---

## Execution

### Option 1: Standalone Binary (Recommended)

Download the latest pre-compiled binary from the [suspicious link removed] tab. This is a single executable that doesn't require Python.

```bash
chmod +x ad-principals
sudo mv ad-principals /usr/local/bin/
ad-principals -i names.txt

```

### Option 2: Manual Setup (Local Development)

**Note:** It is recommended not to run this directly from the Downloads folder.

```bash
chmod +x ad-principals.py
sudo ln -s $(pwd)/ad-principals.py /usr/local/bin/ad-principals

```

---

## 🛡️ Security & Integrity

To ensure the binary has not been tampered with, verify the SHA256 checksum after downloading:

**Latest Binary Checksum (SHA256):** `060a55e970da9d7cda8ca9fe2aa13407597939f03af974478f0ca0cf3e8a12f1`

### Verification Command:

```bash
echo "060a55e970da9d7cda8ca9fe2aa13407597939f03af974478f0ca0cf3e8a12f1  ad-principals" | sha256sum -c -

```

---

## 🔄 Integration Workflow

This tool is designed to be the first step in your AD attack chain:

1. **Permutation**: Use `ad-principals` to generate a candidate list.
2. **Enumeration**: Pipe the output to **Kerbrute** to identify valid users:
```bash
./kerbrute userenum -d ILF.local --dc 10.129.202.85 output_principals.txt

```


3. **Exploitation**: Attempt **AS-REP Roasting** on discovered valid users using `GetNPUsers.py`.

---

## 📜 Disclaimer

This tool is for educational and ethical security testing purposes only. Use it only on systems you have explicit permission to test. The author is not responsible for any misuse of this tool.

---

Made with <3 and VibeCoding

```
