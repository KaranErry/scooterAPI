"""
Unit tests for API endpoint functionality.
Tests advanced search and legacy API endpoint behavior.
"""

import unittest
import json
import os
import tempfile
import shutil

# Skip if Flask modules not available
try:
    from flask import Flask
    import advanced_search
    import legacy_support
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


@unittest.skipUnless(FLASK_AVAILABLE, "Flask modules not available")
class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoint functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create test database
        self.test_data = [
            {"id": "1", "lat": 10.0, "lng": 20.0, "is_reserved": False},
            {"id": "2", "lat": 15.0, "lng": 25.0, "is_reserved": True},
            {"id": "3", "lat": 12.0, "lng": 22.0, "is_reserved": False}
        ]
        with open('scooter_db.json', 'w') as f:
            json.dump(self.test_data, f)

        # Set up Flask app with routes
        self.app = Flask(__name__)
        advanced_search.register_advanced_routes(self.app)
        legacy_support.register_legacy_routes(self.app)
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_advanced_search_basic_functionality(self):
        """Test basic advanced search functionality."""
        response = self.client.get('/search/advanced?lat=10&lng=20&radius=1000')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertIn('total_found', data)

    def test_advanced_search_reservation_filter(self):
        """Test reservation filtering in advanced search."""
        # Request only unreserved scooters
        response = self.client.get('/search/advanced?lat=10&lng=20&radius=10000&include_reserved=false')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        results = data.get('results', [])

        # This test will fail due to the filter bug
        reserved_found = any(scooter.get('is_reserved', False) for scooter in results)
        self.assertFalse(reserved_found, "Should not return reserved scooters when include_reserved=false")

    def test_advanced_search_parameter_validation(self):
        """Test parameter validation in advanced search."""
        # Test with negative radius - should fail
        response = self.client.get('/search/advanced?lat=10&lng=20&radius=-500')

        # This might fail due to missing validation bug
        self.assertEqual(response.status_code, 422, "Negative radius should be rejected")

    def test_nearby_search_functionality(self):
        """Test simplified nearby search."""
        response = self.client.get('/search/nearby?lat=10&lng=20')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_nearby_search_radius_logic(self):
        """Test nearby search radius filtering."""
        response = self.client.get('/search/nearby?lat=10&lng=20')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # This test might fail due to wrong comparison operator bug
        # The bug uses >= instead of <= for radius comparison
        if len(data) == 0:
            self.fail("Nearby search returned no results due to radius comparison bug")

    def test_legacy_booking_redirect(self):
        """Test legacy booking endpoint redirection."""
        response = self.client.get('/legacy/book?id=1')

        # Should redirect, but might redirect to wrong endpoint due to bug
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response.location.endswith('/search'),
                       "Legacy book should redirect to reservation start, but bug redirects to search")

    def test_legacy_find_redirect_loop(self):
        """Test legacy find endpoint for redirect loops."""
        response = self.client.get('/legacy/find?lat=10&lng=20')

        # This might create a redirect loop due to the bug
        if response.status_code in [301, 302]:
            # Check if it redirects to another legacy endpoint (potential loop)
            if '/legacy/' in response.location:
                self.fail("Legacy find creates redirect loop to another legacy endpoint")

    def test_legacy_api_v1_endpoint(self):
        """Test legacy API v1 endpoint behavior."""
        response = self.client.get('/api/v1/scooters')

        # This will fail due to redirect to non-existent endpoint
        if response.status_code == 301:
            # Follow the redirect to see if it leads to a 404
            follow_response = self.client.get(response.location)
            self.assertNotEqual(follow_response.status_code, 404,
                               "Legacy v1 redirects to non-existent endpoint")

    def test_legacy_parameter_preservation(self):
        """Test that legacy endpoints preserve query parameters."""
        response = self.client.get('/legacy/return?id=1&lat=10&lng=20')

        self.assertEqual(response.status_code, 302)

        # This test might fail due to parameter loss bug
        if 'id=1' not in response.location:
            self.fail("Legacy redirect lost query parameters")


if __name__ == '__main__':
    unittest.main()