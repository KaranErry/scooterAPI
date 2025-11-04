"""
Unit tests for input validation functionality.
Tests coordinate validation, parameter sanitization, and data validation.
"""

import unittest
import validators


class TestInputValidation(unittest.TestCase):
    """Test input validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = validators.EnhancedValidators()

    def test_valid_coordinates_accepted(self):
        """Test that valid coordinates are accepted."""
        # Test typical coordinates (San Francisco)
        is_valid, result = self.validator.validate_coordinates(37.7749, -122.4194)

        self.assertTrue(is_valid)
        self.assertEqual(result, (37.7749, -122.4194))

    def test_coordinate_boundary_validation(self):
        """Test coordinate boundary validation."""
        # Test edge cases for coordinate validation
        valid_cases = [
            (90.0, 180.0),    # Maximum valid values
            (-90.0, -180.0),  # Minimum valid values
            (0.0, 0.0),       # Origin point
        ]

        for lat, lng in valid_cases:
            is_valid, _ = self.validator.validate_coordinates(lat, lng)
            self.assertTrue(is_valid, f"Coordinates ({lat}, {lng}) should be valid")

    def test_invalid_coordinates_rejected(self):
        """Test that invalid coordinates are properly rejected."""
        # Test coordinates that should be rejected
        invalid_cases = [
            (91.0, 0.0),      # Latitude too high
            (-91.0, 0.0),     # Latitude too low
            (0.0, 181.0),     # Longitude too high
            (0.0, -181.0),    # Longitude too low
            (100.0, 200.0),   # Both out of range
        ]

        for lat, lng in invalid_cases:
            is_valid, _ = self.validator.validate_coordinates(lat, lng)
            # This test will fail due to the latitude validation bug
            self.assertFalse(is_valid, f"Coordinates ({lat}, {lng}) should be rejected")

    def test_radius_validation(self):
        """Test radius parameter validation."""
        # Test valid radius values
        valid_radii = [100, 1000, 5000.5, 0.1]

        for radius in valid_radii:
            is_valid, result = self.validator.validate_radius(radius)
            self.assertTrue(is_valid, f"Radius {radius} should be valid")

    def test_negative_radius_handling(self):
        """Test handling of negative radius values."""
        # Negative radius should be rejected
        is_valid, _ = self.validator.validate_radius(-100)

        # This test will fail due to the negative radius bug
        self.assertFalse(is_valid, "Negative radius should be rejected")

    def test_scooter_id_validation(self):
        """Test scooter ID validation."""
        # Test valid scooter IDs
        valid_ids = ["scooter_001", "12345", "ABC-123"]

        for scooter_id in valid_ids:
            is_valid, result = self.validator.validate_scooter_id(scooter_id)
            self.assertTrue(is_valid, f"Scooter ID '{scooter_id}' should be valid")

    def test_empty_scooter_id_handling(self):
        """Test handling of empty or invalid scooter IDs."""
        invalid_ids = ["", None, " ", "x" * 200]  # Empty, None, whitespace, too long

        for scooter_id in invalid_ids:
            is_valid, _ = self.validator.validate_scooter_id(scooter_id)
            if scooter_id == "":
                self.assertFalse(is_valid, "Empty scooter ID should be rejected")

    def test_json_validation(self):
        """Test JSON data validation."""
        # Test valid JSON
        valid_json = '{"id": "test", "lat": 10.0, "lng": 20.0}'
        is_valid, result = self.validator.validate_json_data(valid_json)

        self.assertTrue(is_valid)
        self.assertIsInstance(result, dict)

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON data."""
        # Test invalid JSON
        invalid_json = '{"id": "test", "lat": 10.0, "lng":}'  # Missing value
        is_valid, _ = self.validator.validate_json_data(invalid_json)

        # This test will fail due to the JSON validation bug
        self.assertFalse(is_valid, "Malformed JSON should be rejected")


if __name__ == '__main__':
    unittest.main()