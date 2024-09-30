# Unit Tests

import unittest
from app import validate_user_input, check_user_db, return_signin_result

class TestUserSignin(unittest.TestCase):

    def test_valid_input(self):
        # Test with valid input
        self.assertEqual(return_signin_result(validate_user_input('john@test.com'), check_user_db('john@test.com')), "Sign-in successful")
    
    def test_invalid_input(self):  
        # Test with invalid input
        self.assertEqual(return_signin_result(validate_user_input('invalid'), check_user_db('invalid')), "Sign-in failed")

# Integration Tests 

# Test sign-in flow from view to database and back

...

# Implementation