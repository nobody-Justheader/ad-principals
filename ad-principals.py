#!/usr/bin/env python3
import argparse
import csv
import os
import sys
from ad_principals.generator import PrincipalGenerator

def main():
    parser = argparse.ArgumentParser(description="ad-principals: AD Username Enumeration Generator")
    parser.add_argument("-i", "--input", required=True, help="Input names (TXT or CSV)")
    parser.add_argument("-o", "--output", help="Custom output file path")
    args = parser.parse_args()

    gen = PrincipalGenerator()
    usernames = set()

    try:
        # Support for CSV and TXT
        if args.input.lower().endswith('.csv'):
            with open(args.input, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                name_col = next((c for c in reader.fieldnames if 'name' in c.lower()), None)
                if not name_col:
                    print(f"[-] Error: 'Name' column not found in {args.input}")
                    sys.exit(1)
                for row in reader:
                    parts = row[name_col].split()
                    if len(parts) >= 2:
                        usernames.update(gen.generate(parts[0], parts[-1]))
        else:
            with open(args.input, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        usernames.update(gen.generate(parts[0], parts[-1]))

        # Save output
        out_file = args.output if args.output else f"{os.path.splitext(args.input)[0]}_principals.txt"
        with open(out_file, 'w') as f_out:
            f_out.write("\n".join(sorted(list(usernames))))
            
        print(f"[*] Generated {len(usernames)} unique principals.")
        print(f"[+] Results saved to: {out_file}")

    except Exception as e:
        print(f"[-] Fatal Error: {e}")

if __name__ == "__main__":
    main()
