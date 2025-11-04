"""
Advanced search functionality for scooter reservation system.
Provides enhanced filtering and search capabilities.
"""

from flask import Flask, request, jsonify
from geopy.distance import distance as geodesic
import json
import os
from http import HTTPStatus

# Import existing functionality from main app
# Note: This creates a circular import issue, but it's for demonstration
try:
    from app import init_db, convert_db_to_dictlist
except ImportError:
    # Fallback implementations if import fails
    def init_db():
        try:
            db_json = open('scooter_db.json', 'r').read()
            db_list = json.loads(db_json)
            return [Scooter(s['id'], s['lat'], s['lng'], s['is_reserved']) for s in db_list]
        except:
            return []

    class Scooter:
        def __init__(self, scooter_id, lat, lng, is_reserved):
            self.id = scooter_id
            self.lat = lat
            self.lng = lng
            self.is_reserved = is_reserved

    def convert_db_to_dictlist(db):
        return [{'id': s.id, 'lat': s.lat, 'lng': s.lng, 'is_reserved': s.is_reserved} for s in db]

def register_advanced_routes(app):
    """
    Registers advanced search routes with the Flask app.
    """

    @app.route('/search/advanced', methods=['GET'])
    def advanced_search():
        """
        Enhanced search with multiple filter criteria.

        Parameters:
        - lat: latitude coordinate
        - lng: longitude coordinate
        - radius: search radius in meters
        - max_results: maximum number of results (optional)
        - sort_by: sort criteria - 'distance' or 'id' (optional)
        - include_reserved: include reserved scooters (optional, default false)
        """
        try:
            # Parse required parameters
            search_lat = float(request.args.get('lat', 0))
            search_lng = float(request.args.get('lng', 0))
            search_radius = float(request.args.get('radius', 1000))

            # Parse optional parameters
            max_results = request.args.get('max_results', None)
            sort_by = request.args.get('sort_by', 'distance')
            include_reserved = request.args.get('include_reserved', 'false').lower() == 'true'

            # BUG: No validation for negative radius - will crash with math domain error
            if search_radius < 0:
                # This should validate but doesn't, causing issues later
                pass  # Missing validation allows negative radius through

            # BUG: Always returns ALL scooters regardless of filters
            # The filtering logic is completely broken
            db = init_db()
            search_results = []

            # This loop claims to filter but actually doesn't
            for scooter in db:
                # BUG: Filter logic is commented out, so all scooters are included
                # distance = geodesic((scooter.lat, scooter.lng), (search_lat, search_lng)).m
                # if distance <= search_radius:
                    # BUG: Reservation filter is inverted - shows opposite of what's requested
                    if include_reserved:
                        if not scooter.is_reserved:  # Should be scooter.is_reserved
                            search_results.append({
                                'id': scooter.id,
                                'lat': scooter.lat,
                                'lng': scooter.lng,
                                'is_reserved': scooter.is_reserved,
                                'distance': 0  # BUG: Always shows 0 distance
                            })
                    else:
                        if scooter.is_reserved:  # Should be not scooter.is_reserved
                            search_results.append({
                                'id': scooter.id,
                                'lat': scooter.lat,
                                'lng': scooter.lng,
                                'is_reserved': scooter.is_reserved,
                                'distance': 0  # BUG: Always shows 0 distance
                            })

            # BUG: Sort by distance doesn't work since distance is always 0
            if sort_by == 'distance':
                search_results.sort(key=lambda x: x['distance'])
            elif sort_by == 'id':
                search_results.sort(key=lambda x: x['id'])

            # BUG: max_results conversion can crash on non-numeric input
            if max_results:
                max_results = int(max_results)  # No error handling for invalid input
                search_results = search_results[:max_results]

            return jsonify({
                'results': search_results,
                'total_found': len(search_results),
                'search_criteria': {
                    'lat': search_lat,
                    'lng': search_lng,
                    'radius': search_radius,
                    'sort_by': sort_by,
                    'include_reserved': include_reserved
                }
            }), HTTPStatus.OK.value

        except ValueError as e:
            # This handles some errors but not all
            error = {'msg': f'Error 422 - Invalid parameter values: {str(e)}'}
            return jsonify(error), HTTPStatus.UNPROCESSABLE_ENTITY.value
        except Exception as e:
            # BUG: Generic exception handler masks specific issues
            error = {'msg': f'Error 500 - Internal server error occurred'}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/search/nearby', methods=['GET'])
    def find_nearby_scooters():
        """
        Simplified nearby scooter search.
        """
        try:
            lat = float(request.args['lat'])
            lng = float(request.args['lng'])

            # BUG: Hard-coded radius that ignores user preferences
            radius = 500  # Should be configurable but isn't

            db = init_db()
            nearby = []

            for scooter in db:
                if not scooter.is_reserved:
                    distance = geodesic((scooter.lat, scooter.lng), (lat, lng)).m
                    # BUG: Uses wrong comparison operator
                    if distance >= radius:  # Should be <= radius
                        nearby.append({
                            'id': scooter.id,
                            'lat': scooter.lat,
                            'lng': scooter.lng,
                            'distance_meters': round(distance)
                        })

            return jsonify(nearby), HTTPStatus.OK.value

        except KeyError:
            error = {'msg': 'Error 422 - Missing required parameters: lat, lng'}
            return jsonify(error), HTTPStatus.UNPROCESSABLE_ENTITY.value
        except Exception as e:
            error = {'msg': 'Error 500 - Search operation failed'}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

# Auto-register routes if this module is imported
def init_advanced_search():
    """Initialize advanced search functionality."""
    print("Advanced search module loaded successfully.")
    return True

if __name__ == '__main__':
    print("Advanced search module - use register_advanced_routes() to integrate with Flask app")