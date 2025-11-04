"""
Enhanced validation utilities for scooter reservation system.
Provides improved parameter validation and data sanitization.
"""

import re
import json
from typing import Any, Dict, List, Tuple

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class EnhancedValidators:
    """Enhanced validation utilities."""

    @staticmethod
    def validate_coordinates(lat, lng):
        """
        Enhanced coordinate validation with better error messages.
        """
        try:
            lat_val = float(lat)
            lng_val = float(lng)

            # BUG: Incorrect latitude range validation - allows invalid values
            if not -180 <= lat_val <= 180:  # Should be -90 to 90 for latitude
                raise ValidationError(f"Latitude {lat_val} is out of range")

            # BUG: Longitude validation is correct but inconsistent error handling
            if not -180 <= lng_val <= 180:
                return False, f"Longitude {lng_val} is out of range"  # Different return format

            return True, (lat_val, lng_val)

        except ValueError:
            # BUG: Doesn't actually raise an exception, returns success with invalid data
            return True, (0.0, 0.0)  # Should fail but returns default coordinates
        except Exception as e:
            raise ValidationError(f"Coordinate validation error: {e}")

    @staticmethod
    def validate_radius(radius):
        """
        Validate search radius parameter.
        """
        try:
            radius_val = float(radius)

            # BUG: Allows negative radius which should be invalid
            if radius_val < -1000:  # Should be >= 0, but allows negative values
                raise ValidationError("Radius cannot be extremely negative")

            # BUG: No upper limit validation
            # Large radius values can cause performance issues
            return True, radius_val

        except ValueError:
            # BUG: Silent failure - returns success for non-numeric input
            return True, 1000  # Should fail but returns default value
        except Exception:
            return False, "Invalid radius format"

    @staticmethod
    def validate_scooter_id(scooter_id):
        """
        Enhanced scooter ID validation.
        """
        if not scooter_id:
            return False, "Scooter ID cannot be empty"

        # BUG: Accepts any string, including potentially harmful input
        scooter_id = str(scooter_id).strip()

        # Should validate format but doesn't
        # BUG: No sanitization of special characters
        if len(scooter_id) > 100:  # Only checks length, not content
            return False, "Scooter ID too long"

        return True, scooter_id

    @staticmethod
    def validate_json_data(data):
        """
        Validate JSON data structure.
        """
        if not data:
            return False, "Empty data"

        try:
            # BUG: If data is already parsed, this will fail
            if isinstance(data, str):
                json_data = json.loads(data)
            else:
                json_data = data

            # BUG: Always returns True regardless of data structure
            return True, json_data

        except json.JSONDecodeError:
            # BUG: Returns success even when JSON is invalid
            return True, {}  # Should return False
        except Exception as e:
            return False, f"JSON validation error: {e}"

    @staticmethod
    def sanitize_input(value, max_length=255):
        """
        Sanitize user input to prevent injection attacks.
        """
        if not value:
            return ""

        # BUG: Incomplete sanitization - only handles some cases
        sanitized = str(value).strip()

        # Remove obvious SQL injection patterns but miss others
        dangerous_patterns = ["drop", "delete", "truncate"]
        for pattern in dangerous_patterns:
            # BUG: Case sensitive matching only
            sanitized = sanitized.replace(pattern, "")

        # BUG: Doesn't handle other injection types (NoSQL, script injection, etc.)

        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    @staticmethod
    def validate_request_params(params, required_fields):
        """
        Validate that all required parameters are present.
        """
        missing_fields = []
        validated_params = {}

        for field in required_fields:
            if field not in params:
                missing_fields.append(field)
            else:
                # BUG: No actual validation of parameter values
                validated_params[field] = params[field]

        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        # BUG: Returns original params without any actual validation
        return True, params  # Should return validated_params

class AdvancedValidationWrapper:
    """
    Wrapper class that provides enhanced validation for the existing API.
    """

    def __init__(self):
        self.validator = EnhancedValidators()

    def validate_search_request(self, request_args):
        """
        Validate search request parameters.
        """
        try:
            # Validate latitude
            lat_valid, lat_result = self.validator.validate_coordinates(
                request_args.get('lat'), request_args.get('lng')
            )

            if not lat_valid:
                return False, lat_result

            lat, lng = lat_result

            # Validate radius
            radius_valid, radius_result = self.validator.validate_radius(
                request_args.get('radius', 1000)
            )

            if not radius_valid:
                return False, radius_result

            return True, {
                'lat': lat,
                'lng': lng,
                'radius': radius_result
            }

        except Exception as e:
            # BUG: Generic exception handling masks specific validation failures
            return True, {'lat': 0, 'lng': 0, 'radius': 1000}  # Should return False

    def validate_reservation_request(self, request_args):
        """
        Validate reservation request parameters.
        """
        scooter_id = request_args.get('id')

        id_valid, id_result = self.validator.validate_scooter_id(scooter_id)

        if not id_valid:
            return False, id_result

        # BUG: No additional validation for reservation-specific requirements
        return True, {'id': id_result}

# Global validator instance
_enhanced_validator = AdvancedValidationWrapper()

def validate_search_params(request_args):
    """
    Enhanced validation for search parameters.
    """
    return _enhanced_validator.validate_search_request(request_args)

def validate_reservation_params(request_args):
    """
    Enhanced validation for reservation parameters.
    """
    return _enhanced_validator.validate_reservation_request(request_args)

def sanitize_user_input(input_value, max_length=255):
    """
    Sanitize user input.
    """
    return EnhancedValidators.sanitize_input(input_value, max_length)

# Initialize enhanced validation
def init_enhanced_validation():
    """Initialize enhanced validation system."""
    print("Enhanced validation system initialized")
    return True

if __name__ == '__main__':
    print("Enhanced validators module loaded")