import unittest
from ad_principals.generator import PrincipalGenerator

class TestPrincipalGenerator(unittest.TestCase):
    def setUp(self):
        """Initialize the generator before each test."""
        self.gen_sam = PrincipalGenerator(mode='sam')
        self.gen_upn = PrincipalGenerator(mode='upn')

    def test_basic_permutation(self):
        """Test if standard permutations are generated correctly."""
        results = self.gen_sam.generate("Jane", "Smith")
        # Check for common patterns
        self.assertIn("jsmith", results)
        self.assertIn("jane.smith", results)
        self.assertIn("smithj", results)
        self.assertIn("janes", results)
        self.assertIn("jane_smith", results)
        self.assertIn("smith.j", results)

    def test_sam_account_limit(self):
        """Test if the 20-character sAMAccountName limit is enforced."""
        # 'christopher.longnamevantage' would be 29 characters
        results = self.gen_sam.generate("Christopher", "Longnamevantage")
        for username in results:
            self.assertLessEqual(len(username), 20, f"Username {username} exceeds 20 chars")

    def test_upn_limit(self):
        """Test if the 64-character UPN limit is enforced."""
        # Generate very long name
        results = self.gen_upn.generate("Christopheralexander", "Vanderbiltlongnamevantage")
        for username in results:
            self.assertLessEqual(len(username), 64, f"Username {username} exceeds 64 chars")

    def test_special_characters_sam(self):
        """Test if non-alphanumeric characters are stripped for SAM format."""
        # Names with hyphens or apostrophes should be sanitized
        results = self.gen_sam.generate("O'Brian", "Smith-Jones")
        for username in results:
            # SAM allows only alphanumeric, period, hyphen, underscore
            self.assertTrue(all(c.isalnum() or c in '._-' for c in username),
                          f"Username {username} contains invalid SAM characters")

    def test_special_characters_upn(self):
        """Test UPN allows additional characters."""
        # UPN allows more characters including ! # ^ ~ '
        results = self.gen_upn.generate("O'Brian", "Smith-Jones")
        # Should successfully generate usernames
        self.assertTrue(len(results) > 0)
        for username in results:
            # Check characters are UPN-valid
            self.assertTrue(all(c.isalnum() or c in "._-!#^~'" for c in username),
                          f"Username {username} contains invalid UPN characters")

    def test_case_insensitivity(self):
        """Test if the generator converts everything to lowercase."""
        results = self.gen_sam.generate("CAROL", "JOHNSON")
        self.assertIn("cjohnson", results)
        self.assertTrue(all(u.islower() or not u.isalpha() for u in results))

    def test_empty_input(self):
        """Test behavior with empty strings."""
        results = self.gen_sam.generate("", "Smith")
        self.assertEqual(results, [])

    def test_separator_variations(self):
        """Test underscores and hyphens in usernames."""
        results = self.gen_sam.generate("John", "Doe")
        self.assertIn("john_doe", results)
        self.assertIn("john-doe", results)
        self.assertIn("j_doe", results)
        self.assertIn("j-doe", results)

    def test_reverse_formats(self):
        """Test reverse name patterns (lastname.firstname)."""
        results = self.gen_sam.generate("John", "Smith")
        self.assertIn("smithjohn", results)
        self.assertIn("smith.john", results)
        self.assertIn("smith.j", results)
        self.assertIn("smithj", results)

    def test_numbered_variations_disabled_by_default(self):
        """Test that numbered variations are NOT included by default."""
        results = self.gen_sam.generate("Jane", "Smith")
        # Should not contain numbered versions
        self.assertNotIn("jsmith1", results)
        self.assertNotIn("jsmith2", results)
        self.assertNotIn("jane.smith1", results)

    def test_numbered_variations_enabled(self):
        """Test numbered variations when explicitly enabled."""
        results = self.gen_sam.generate("Jane", "Smith", include_numbers=True, max_number=3)
        # Should contain numbered versions
        self.assertIn("jsmith1", results)
        self.assertIn("jsmith2", results)
        self.assertIn("jsmith3", results)
        self.assertIn("jsmith01", results)  # zero-padded

    def test_year_variations(self):
        """Test year-based suffixes."""
        results = self.gen_sam.generate("Jane", "Smith", include_years=True, current_year=2024)
        self.assertIn("jsmith2024", results)
        self.assertIn("jsmith24", results)

    def test_admin_variations_disabled_by_default(self):
        """Test that admin variations are NOT included by default."""
        results = self.gen_sam.generate("Jane", "Smith", include_admin=False)
        self.assertNotIn("jsmith-admin", results)
        self.assertNotIn("jsmith_adm", results)

    def test_admin_variations_enabled(self):
        """Test admin account variations."""
        results = self.gen_sam.generate("Jane", "Smith", include_admin=True)
        # Should contain admin versions (truncated to 20 chars)
        self.assertTrue(any('admin' in u or 'adm' in u for u in results))

    def test_location_variations(self):
        """Test location-based suffixes."""
        results = self.gen_sam.generate("Jane", "Smith", locations=['nyc', 'lon'])
        self.assertIn("jsmith.nyc", results)
        self.assertIn("jsmith-lon", results)

    def test_middle_name_patterns(self):
        """Test middle name/initial handling."""
        results = self.gen_sam.generate("Jane", "Smith", middle="Robert")
        self.assertIn("jane.r.smith", results)
        self.assertIn("j.r.smith", results)
        self.assertIn("jrs", results)

    def test_initial_patterns(self):
        """Test various initial-based formats."""
        results = self.gen_sam.generate("Jane", "Doe")
        self.assertIn("jd", results)
        self.assertIn("dj", results)
        self.assertIn("j.d", results)
        self.assertIn("d.j", results)

    def test_no_trailing_period(self):
        """Test that usernames don't end with a period (AD requirement)."""
        results = self.gen_sam.generate("Jane", "Smith")
        for username in results:
            self.assertFalse(username.endswith('.'), 
                           f"Username {username} ends with period")

    def test_legacy_truncated_format(self):
        """Test 3+3 legacy format."""
        results = self.gen_sam.generate("Christopher", "Washington")
        self.assertIn("chrwas", results)

    def test_output_count_increased(self):
        """Test that we generate more variations than the old 10."""
        results = self.gen_sam.generate("Jane", "Smith", include_admin=False)
        # Should have 20+ variations with new patterns
        self.assertGreater(len(results), 15, 
                          f"Expected 15+ variations, got {len(results)}")

if __name__ == "__main__":
    unittest.main()
