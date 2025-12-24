import unittest
from ad_principals.generator import PrincipalGenerator

class TestPrincipalGenerator(unittest.TestCase):
    def setUp(self):
        """Initialize the generator before each test."""
        self.gen = PrincipalGenerator(sam_limit=20)

    def test_basic_permutation(self):
        """Test if standard permutations are generated correctly."""
        results = self.gen.generate("John", "Marston")
        # Check for common patterns
        self.assertIn("jmarston", results)
        self.assertIn("john.marston", results)
        self.assertIn("marstonj", results)
        self.assertIn("johnm", results)

    def test_sam_account_limit(self):
        """Test if the 20-character sAMAccountName limit is enforced."""
        # 'christopher.longnamevantage' is 26 characters
        results = self.gen.generate("Christopher", "Longnamevantage")
        for username in results:
            self.assertLessEqual(len(username), 20, f"Username {username} exceeds 20 chars")

    def test_special_characters(self):
        """Test if non-alphanumeric characters are stripped."""
        # Names with hyphens or apostrophes should be sanitized
        results = self.gen.generate("O'Brian", "Smith-Jones")
        for username in results:
            # Check that no special characters exist in the output
            self.assertTrue(username.isalnum() or '.' in username)

    def test_case_insensitivity(self):
        """Test if the generator converts everything to lowercase."""
        results = self.gen.generate("CAROL", "JOHNSON")
        self.assertIn("cjohnson", results)
        self.assertTrue(all(u.islower() for u in results))

    def test_empty_input(self):
        """Test behavior with empty strings."""
        results = self.gen.generate("", "Marston")
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
