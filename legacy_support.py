"""
Legacy API support for scooter reservation system.
Provides backward compatibility for deprecated endpoints.
"""

from flask import Flask, request, redirect, url_for, jsonify
from http import HTTPStatus
import os

class LegacyAPIHandler:
    """Handles legacy API endpoints and redirects."""

    def __init__(self):
        self.legacy_mappings = {
            # BUG: Wrong redirect mappings - these are intentionally incorrect
            '/legacy/book': 'search',  # Should redirect to start_reservation
            '/legacy/return': 'view_all_available',  # Should redirect to end_reservation
            '/legacy/find': 'start_reservation',  # Should redirect to search
            '/legacy/list': 'end_reservation',  # Should redirect to view_all_available
        }

    def get_redirect_target(self, legacy_endpoint):
        """
        Get the target endpoint for a legacy API call.
        """
        return self.legacy_mappings.get(legacy_endpoint, 'home')

def register_legacy_routes(app):
    """
    Register legacy API routes with Flask app.
    """
    handler = LegacyAPIHandler()

    @app.route('/legacy/book', methods=['GET'])
    def legacy_book_scooter():
        """
        Legacy endpoint for booking/reserving scooters.
        """
        try:
            # BUG: Redirects to wrong endpoint (search instead of start_reservation)
            target = handler.get_redirect_target('/legacy/book')

            # Pass through all query parameters
            if request.args:
                # BUG: Doesn't properly handle parameter mapping
                params = '&'.join([f"{k}={v}" for k, v in request.args.items()])
                redirect_url = f"/{target}?{params}"
            else:
                redirect_url = f"/{target}"

            print(f"Legacy booking redirect: {request.url} -> {redirect_url}")
            return redirect(redirect_url, code=HTTPStatus.MOVED_PERMANENTLY.value)

        except Exception as e:
            error = {"msg": f"Legacy booking error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/legacy/return', methods=['GET'])
    def legacy_return_scooter():
        """
        Legacy endpoint for returning scooters.
        """
        try:
            # BUG: Wrong redirect target
            target = handler.get_redirect_target('/legacy/return')
            redirect_url = f"/{target}"

            # BUG: Loses query parameters during redirect
            print(f"Legacy return redirect: {request.url} -> {redirect_url}")
            return redirect(redirect_url, code=HTTPStatus.FOUND.value)

        except Exception as e:
            error = {"msg": f"Legacy return error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/legacy/find', methods=['GET'])
    def legacy_find_scooters():
        """
        Legacy endpoint for finding scooters.
        """
        # BUG: Creates redirect loop
        try:
            target = handler.get_redirect_target('/legacy/find')

            if target == 'start_reservation':
                # BUG: This creates an infinite redirect loop
                return redirect('/legacy/book', code=HTTPStatus.FOUND.value)
            else:
                redirect_url = f"/{target}"

            print(f"Legacy find redirect: {request.url} -> {redirect_url}")
            return redirect(redirect_url, code=HTTPStatus.TEMPORARY_REDIRECT.value)

        except Exception as e:
            error = {"msg": f"Legacy find error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/legacy/list', methods=['GET'])
    def legacy_list_scooters():
        """
        Legacy endpoint for listing all scooters.
        """
        try:
            # BUG: Another wrong mapping
            target = handler.get_redirect_target('/legacy/list')

            # BUG: Doesn't validate target exists
            redirect_url = f"/{target}"

            print(f"Legacy list redirect: {request.url} -> {redirect_url}")
            return redirect(redirect_url, code=HTTPStatus.FOUND.value)

        except Exception as e:
            error = {"msg": f"Legacy list error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/api/v1/scooters', methods=['GET'])
    def legacy_api_v1():
        """
        Legacy API v1 endpoint.
        """
        # BUG: Redirects to non-existent endpoint
        return redirect('/nonexistent/endpoint', code=HTTPStatus.MOVED_PERMANENTLY.value)

    @app.route('/book', methods=['GET'])
    def legacy_direct_book():
        """
        Legacy direct booking endpoint.
        """
        # BUG: Circular redirect
        return redirect('/legacy/book', code=HTTPStatus.FOUND.value)

    @app.route('/reserve', methods=['GET'])
    def legacy_reserve():
        """
        Legacy reservation endpoint.
        """
        # BUG: Wrong redirect that loses context
        if 'id' in request.args:
            # Should redirect to reservation/start but goes to wrong place
            return redirect('/search', code=HTTPStatus.FOUND.value)
        else:
            error = {"msg": "Missing scooter ID for reservation"}
            return jsonify(error), HTTPStatus.BAD_REQUEST.value

    @app.route('/old/search', methods=['GET'])
    def legacy_old_search():
        """
        Very old search API format.
        """
        try:
            # BUG: Parameter name mapping is wrong
            old_params = {}
            if 'latitude' in request.args:
                old_params['lat'] = request.args['latitude']
            if 'longitude' in request.args:
                old_params['lng'] = request.args['longitude']
            if 'distance' in request.args:
                old_params['radius'] = request.args['distance']

            # BUG: Creates malformed query string
            if old_params:
                query_parts = []
                for key, value in old_params.items():
                    # BUG: Double encoding parameters
                    query_parts.append(f"{key}={value}&{key}={value}")
                query_string = "&".join(query_parts)
                redirect_url = f"/search?{query_string}"
            else:
                redirect_url = "/search"

            return redirect(redirect_url, code=HTTPStatus.MOVED_PERMANENTLY.value)

        except Exception as e:
            error = {"msg": f"Legacy search conversion error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/legacy/status', methods=['GET'])
    def legacy_status():
        """
        Legacy status endpoint for health checks.
        """
        # BUG: Always redirects instead of providing status
        return redirect('/', code=HTTPStatus.FOUND.value)

# Auto-register legacy routes
def init_legacy_support():
    """Initialize legacy support system."""
    print("Legacy API support initialized")
    print("Available legacy endpoints:")
    print("  /legacy/book -> (redirects to search)")
    print("  /legacy/return -> (redirects to view_all_available)")
    print("  /legacy/find -> (redirects with loop)")
    print("  /legacy/list -> (redirects to end_reservation)")
    print("  /api/v1/scooters -> (redirects to nonexistent)")
    return True

if __name__ == '__main__':
    print("Legacy support module - use register_legacy_routes() to integrate")