import re

class PrincipalGenerator:
    def __init__(self, sam_limit=20):
        self.sam_limit = sam_limit

    def generate(self, first, last):
        """Generates AD-compatible permutations for a given name."""
        # Clean non-alphanumeric characters (Kali tools often sanitize input)
        f = re.sub(r'[^a-zA-Z0-9]', '', first.lower().strip())
        l = re.sub(r'[^a-zA-Z0-9]', '', last.lower().strip())
        
        if not f or not l:
            return []

        # Standard AD & Corporate patterns
        patterns = {
            f"{f}{l}",           # johnmarston
            f"{f}.{l}",          # john.marston
            f"{f[0]}{l}",        # jmarston
            f"{f}.{l[0]}",       # john.m
            f"{f[0]}.{l}",       # j.marston
            f"{l}{f[0]}",        # marstonj
            f"{l}.{f[0]}",       # marston.j
            f"{f}{l[0]}",        # johnm
            f"{f[0]}{l[0]}",     # jm
            f"{f[:3]}{l[:3]}",   # johmar (legacy)
        }
        
        return sorted({p[:self.sam_limit] for p in patterns})
