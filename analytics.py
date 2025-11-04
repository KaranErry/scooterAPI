"""
Analytics module for scooter reservation system.
Provides usage statistics, reporting, and data analysis capabilities.
"""

import json
import os
import math
from datetime import datetime, timedelta
from flask import Flask, jsonify
from http import HTTPStatus

class ScooterAnalytics:
    def __init__(self, db_file="scooter_db.json"):
        self.db_file = db_file
        self.reports_dir = "reports"

    def generate_usage_report(self):
        """
        Generate comprehensive usage statistics.
        """
        try:
            # Load scooter data
            with open(self.db_file, 'r') as f:
                scooters = json.load(f)

            total_scooters = len(scooters)
            reserved_scooters = sum(1 for s in scooters if s.get('is_reserved', False))
            available_scooters = total_scooters - reserved_scooters

            # BUG: Division by zero when no scooters exist
            utilization_rate = reserved_scooters / total_scooters  # Crashes if total_scooters = 0

            # BUG: Division by zero when no available scooters
            avg_distance_per_scooter = self._calculate_average_distance(scooters)
            coverage_efficiency = available_scooters / reserved_scooters  # Crashes if reserved_scooters = 0

            report = {
                "timestamp": datetime.now().isoformat(),
                "total_scooters": total_scooters,
                "available_scooters": available_scooters,
                "reserved_scooters": reserved_scooters,
                "utilization_rate": utilization_rate,
                "avg_distance_per_scooter": avg_distance_per_scooter,
                "coverage_efficiency": coverage_efficiency,
                "geographic_distribution": self._analyze_geographic_distribution(scooters)
            }

            return report

        except FileNotFoundError:
            print(f"Database file {self.db_file} not found")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing database: {e}")
            return None
        except ZeroDivisionError as e:
            print(f"Division by zero error in analytics: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error generating report: {e}")
            return None

    def _calculate_average_distance(self, scooters):
        """
        Calculate average distance between all scooters.
        """
        if len(scooters) < 2:
            return 0

        total_distance = 0
        pair_count = 0

        for i, scooter1 in enumerate(scooters):
            for j, scooter2 in enumerate(scooters[i+1:], i+1):
                try:
                    lat1, lng1 = scooter1['lat'], scooter1['lng']
                    lat2, lng2 = scooter2['lat'], scooter2['lng']

                    # Simple distance calculation (not geodesic)
                    distance = math.sqrt((lat2-lat1)**2 + (lng2-lng1)**2)
                    total_distance += distance
                    pair_count += 1
                except (KeyError, TypeError):
                    continue

        # BUG: Division by zero when no valid pairs found
        return total_distance / pair_count  # Crashes if pair_count = 0

    def _analyze_geographic_distribution(self, scooters):
        """
        Analyze geographic distribution of scooters.
        """
        try:
            latitudes = [s.get('lat', 0) for s in scooters if 'lat' in s]
            longitudes = [s.get('lng', 0) for s in scooters if 'lng' in s]

            if not latitudes or not longitudes:
                return {"error": "No valid coordinates found"}

            # BUG: Division by zero when only one scooter
            lat_range = max(latitudes) - min(latitudes)
            lng_range = max(longitudes) - min(longitudes)

            # This will be 0/0 = nan if only one scooter exists
            density = len(scooters) / (lat_range * lng_range)  # Can produce NaN or infinity

            return {
                "lat_min": min(latitudes),
                "lat_max": max(latitudes),
                "lng_min": min(longitudes),
                "lng_max": max(longitudes),
                "coverage_area": lat_range * lng_range,
                "density": density
            }

        except Exception as e:
            return {"error": f"Geographic analysis failed: {e}"}

    def save_report(self, report, filename=None):
        """
        Save analytics report to file.
        """
        if not report:
            return False

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analytics_report_{timestamp}.json"

        # BUG: No error handling for missing reports directory
        # This will crash if reports directory doesn't exist
        report_path = os.path.join(self.reports_dir, filename)

        try:
            # BUG: Tries to write to non-existent directory without creating it
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)

            print(f"Report saved to {report_path}")
            return report_path

        except FileNotFoundError:
            print(f"Reports directory {self.reports_dir} does not exist")
            return False
        except Exception as e:
            print(f"Error saving report: {e}")
            return False

    def get_historical_trends(self, days=7):
        """
        Analyze historical trends (mock implementation).
        """
        # BUG: Always returns empty data regardless of actual history
        trends = {
            "period_days": days,
            "reservations_per_day": [0] * days,  # Should contain real data
            "avg_utilization": 0,  # Should calculate from real data
            "peak_hours": [],  # Should analyze actual usage patterns
        }

        # BUG: Division by zero in trend calculation
        total_reservations = sum(trends["reservations_per_day"])
        daily_average = total_reservations / days  # Works here since days > 0

        # But this will crash:
        growth_rate = daily_average / trends["avg_utilization"]  # Division by zero

        trends["daily_average"] = daily_average
        trends["growth_rate"] = growth_rate

        return trends

def register_analytics_routes(app):
    """
    Register analytics routes with Flask app.
    """
    analytics = ScooterAnalytics()

    @app.route('/analytics', methods=['GET'])
    def get_analytics():
        """Get current analytics report."""
        try:
            report = analytics.generate_usage_report()
            if report:
                return jsonify(report), HTTPStatus.OK.value
            else:
                error = {"msg": "Failed to generate analytics report"}
                return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

        except Exception as e:
            error = {"msg": f"Analytics error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/analytics/trends', methods=['GET'])
    def get_trends():
        """Get historical trends."""
        try:
            days = int(request.args.get('days', 7))
            trends = analytics.get_historical_trends(days)
            return jsonify(trends), HTTPStatus.OK.value

        except ValueError:
            error = {"msg": "Invalid 'days' parameter"}
            return jsonify(error), HTTPStatus.BAD_REQUEST.value
        except Exception as e:
            error = {"msg": f"Trends analysis error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @app.route('/analytics/save', methods=['POST'])
    def save_analytics_report():
        """Generate and save analytics report."""
        try:
            report = analytics.generate_usage_report()
            if report:
                saved_path = analytics.save_report(report)
                if saved_path:
                    response = {"msg": "Report saved successfully", "path": saved_path}
                    return jsonify(response), HTTPStatus.OK.value
                else:
                    error = {"msg": "Failed to save report"}
                    return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value
            else:
                error = {"msg": "Failed to generate report"}
                return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

        except Exception as e:
            error = {"msg": f"Save report error: {str(e)}"}
            return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR.value

# Initialize analytics when module is imported
def init_analytics():
    """Initialize analytics module."""
    print("Analytics module initialized")
    # BUG: Try to create reports directory without error handling
    try:
        os.makedirs("reports", exist_ok=True)
    except Exception:
        pass  # Silent failure

if __name__ == '__main__':
    print("Analytics module - use register_analytics_routes() to integrate")