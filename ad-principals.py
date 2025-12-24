#!/usr/bin/env python3
import argparse
import csv
import os
import sys
from ad_principals.generator import PrincipalGenerator

def main():
    parser = argparse.ArgumentParser(
        description="ad-principals: AD Username Enumeration Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (generates UPN-compatible usernames, 64 char limit)
  %(prog)s -i employees.txt
  
  # Include numbered variations for collision detection
  %(prog)s -i employees.txt --with-numbers --max-num 5
  
  # Full red teaming mode with all variations
  %(prog)s -i employees.txt --with-numbers --with-years --with-admin
        """
    )
    
    # Required arguments
    parser.add_argument("-i", "--input", required=True, 
                       help="Input names (TXT or CSV)")
    parser.add_argument("-o", "--output", 
                       help="Custom output file path")
    
    # Optional variations
    parser.add_argument("--with-numbers", action='store_true',
                       help="Include numbered suffixes (e.g., jsmith1, jsmith2)")
    parser.add_argument("--with-years", action='store_true',
                       help="Include year-based suffixes (e.g., jsmith2024, jsmith24)")
    parser.add_argument("--with-admin", action='store_true', default=False,
                       help="Include admin account variations (e.g., jsmith-admin)")
    parser.add_argument("--max-num", type=int, default=3, metavar='N',
                       help="Maximum number suffix when --with-numbers is enabled (default: 3)")
    parser.add_argument("--locations", type=str, metavar='CODE1,CODE2',
                       help="Comma-separated location codes (e.g., nyc,lon,sfo)")
    
    args = parser.parse_args()

    # Initialize generator with UPN mode (64 char limit) for maximum coverage
    # Usernames ≤20 chars work for both SAM and UPN
    # Usernames 21-64 chars work for UPN only
    gen = PrincipalGenerator(mode='upn')
    usernames = set()
    
    # Parse locations if provided
    locations = args.locations.split(',') if args.locations else None

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
                        usernames.update(gen.generate(
                            parts[0], 
                            parts[-1],
                            include_numbers=args.with_numbers,
                            include_years=args.with_years,
                            include_admin=args.with_admin,
                            max_number=args.max_num,
                            locations=locations
                        ))
        else:
            with open(args.input, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        usernames.update(gen.generate(
                            parts[0], 
                            parts[-1],
                            include_numbers=args.with_numbers,
                            include_years=args.with_years,
                            include_admin=args.with_admin,
                            max_number=args.max_num,
                            locations=locations
                        ))

        # Save output
        out_file = args.output if args.output else f"{os.path.splitext(args.input)[0]}_principals.txt"
        with open(out_file, 'w') as f_out:
            f_out.write("\n".join(sorted(list(usernames))))
            
        print(f"[*] Generated {len(usernames)} unique principals.")
        print(f"[+] Character limit: 64 (UPN-compatible, ≤20 chars also work for sAMAccountName)")
        if args.with_numbers:
            print(f"[+] Numbered variations: Enabled (1-{args.max_num})")
        if args.with_years:
            print(f"[+] Year-based variations: Enabled")
        if args.with_admin:
            print(f"[+] Admin variations: Enabled")
        if locations:
            print(f"[+] Location codes: {', '.join(locations)}")
        print(f"[+] Results saved to: {out_file}")

    except Exception as e:
        print(f"[-] Fatal Error: {e}")

if __name__ == "__main__":
    main()
