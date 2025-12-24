import re
from datetime import datetime

class PrincipalGenerator:
    def __init__(self, sam_limit=20, upn_limit=64, mode='sam'):
        """
        Initialize the AD Principal Generator.
        
        Args:
            sam_limit: sAMAccountName character limit (default: 20)
            upn_limit: UserPrincipalName character limit (default: 64)
            mode: Output mode - 'sam', 'upn', or 'both'
        """
        self.sam_limit = sam_limit
        self.upn_limit = upn_limit
        self.mode = mode

    def _sanitize_sam(self, text):
        """Sanitize for sAMAccountName (allows: letters, numbers, . - _)"""
        # Remove invalid characters for sAMAccountName
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', text.lower().strip())
        # Ensure it doesn't end with a period
        return sanitized.rstrip('.')

    def _sanitize_upn(self, text):
        """Sanitize for UserPrincipalName (allows: letters, numbers, . - _ ! # ^ ~ ')"""
        # Remove invalid characters for UPN username part
        sanitized = re.sub(r"[^a-zA-Z0-9._\-!#^~']", '', text.lower().strip())
        # Ensure it doesn't end with a period
        return sanitized.rstrip('.')

    def _apply_limit(self, username):
        """Apply character limits based on mode"""
        if self.mode == 'sam':
            return username[:self.sam_limit]
        elif self.mode == 'upn':
            return username[:self.upn_limit]
        else:  # both
            # Return SAM version, UPN will be handled separately if needed
            return username[:self.sam_limit]

    def generate(self, first, last, middle=None, include_numbers=False, 
                 include_years=False, include_admin=True, max_number=3, 
                 current_year=None, locations=None):
        """
        Generates AD-compatible permutations for a given name.
        
        Args:
            first: First name
            last: Last name
            middle: Middle name/initial (optional)
            include_numbers: Add numbered suffixes (1-max_number)
            include_years: Add year-based suffixes
            include_admin: Add admin/service account variations
            max_number: Maximum number for suffixes (default: 3)
            current_year: Year to use for year-based suffixes (default: current year)
            locations: List of location codes to append (e.g., ['nyc', 'lon'])
            
        Returns:
            Sorted list of unique username permutations
        """
        # Determine sanitization method based on mode
        if self.mode == 'upn':
            sanitize = self._sanitize_upn
        else:
            sanitize = self._sanitize_sam
        
        # Clean names
        f = sanitize(first)
        l = sanitize(last)
        m = sanitize(middle) if middle else None
        
        if not f or not l:
            return []

        # Base patterns without numbers/suffixes
        patterns = set()
        
        # === STANDARD FORMATS ===
        # Full name combinations
        patterns.add(f"{f}{l}")              # janesmith
        patterns.add(f"{f}.{l}")             # jane.smith
        patterns.add(f"{f}_{l}")             # jane_smith
        patterns.add(f"{f}-{l}")             # jane-smith
        
        # First initial + last name
        patterns.add(f"{f[0]}{l}")           # jsmith
        patterns.add(f"{f[0]}.{l}")          # j.smith
        patterns.add(f"{f[0]}_{l}")          # j_smith
        patterns.add(f"{f[0]}-{l}")          # j-smith
        
        # First name + last initial
        patterns.add(f"{f}{l[0]}")           # janes
        patterns.add(f"{f}.{l[0]}")          # john.m
        patterns.add(f"{f}_{l[0]}")          # john_m
        patterns.add(f"{f}-{l[0]}")          # john-m
        
        # === REVERSE FORMATS ===
        patterns.add(f"{l}{f}")              # smithjane
        patterns.add(f"{l}.{f}")             # smith.jane
        patterns.add(f"{l}_{f}")             # smith_jane
        patterns.add(f"{l}-{f}")             # smith-jane
        
        # Last name + first initial
        patterns.add(f"{l}{f[0]}")           # smithj
        patterns.add(f"{l}.{f[0]}")          # smith.j
        patterns.add(f"{l}_{f[0]}")          # smith_j
        patterns.add(f"{l}-{f[0]}")          # smith-j
        
        # Last initial + first name
        patterns.add(f"{l[0]}{f}")           # sjane
        patterns.add(f"{l[0]}.{f}")          # s.jane
        
        # === INITIAL-BASED FORMATS ===
        patterns.add(f"{f[0]}{l[0]}")        # jm
        patterns.add(f"{l[0]}{f[0]}")        # mj
        patterns.add(f"{f[0]}.{l[0]}")       # j.m
        patterns.add(f"{l[0]}.{f[0]}")       # m.j
        
        # === LEGACY/TRUNCATED FORMATS ===
        if len(f) >= 3 and len(l) >= 3:
            patterns.add(f"{f[:3]}{l[:3]}")  # johmar (3+3 legacy)
        
        # === MIDDLE NAME PATTERNS (if provided) ===
        if m:
            patterns.add(f"{f}.{m[0]}.{l}")      # john.m.marston
            patterns.add(f"{f[0]}.{m[0]}.{l}")   # j.m.marston
            patterns.add(f"{f}{m[0]}{l}")         # janesmarston
            patterns.add(f"{f[0]}{m[0]}{l[0]}")  # jmm
        
        # Apply character limits to base patterns
        base_usernames = {self._apply_limit(p) for p in patterns}
        
        # === OPTIONAL VARIATIONS ===
        all_usernames = set(base_usernames)
        
        # Add numbered variations (1-max_number)
        if include_numbers:
            for base in base_usernames:
                for num in range(1, max_number + 1):
                    all_usernames.add(self._apply_limit(f"{base}{num}"))
                    # Also add zero-padded versions for some patterns
                    if num <= 9:
                        all_usernames.add(self._apply_limit(f"{base}0{num}"))
        
        # Add year-based variations
        if include_years:
            year = current_year if current_year else datetime.now().year
            year_short = str(year)[-2:]  # Last 2 digits
            
            for base in base_usernames:
                all_usernames.add(self._apply_limit(f"{base}{year}"))      # jsmith2024
                all_usernames.add(self._apply_limit(f"{base}{year_short}"))  # jsmith24
        
        # Add admin/service account variations
        if include_admin:
            admin_suffixes = ['-admin', '_admin', '-adm', '_adm', 'admin']
            for base in base_usernames:
                for suffix in admin_suffixes:
                    all_usernames.add(self._apply_limit(f"{base}{suffix}"))
        
        # Add location-based variations
        if locations:
            for base in base_usernames:
                for loc in locations:
                    loc_clean = sanitize(loc)
                    all_usernames.add(self._apply_limit(f"{base}.{loc_clean}"))
                    all_usernames.add(self._apply_limit(f"{base}-{loc_clean}"))
        
        return sorted(list(all_usernames))

