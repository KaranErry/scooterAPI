# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based REST API for a scooter reservation system. The API allows users to view available scooters, search for scooters within a radius, reserve scooters, and end reservations with payment processing.

## Development Commands

### Local Development
- **Run the application**: `python3 app.py`
  - Runs on http://localhost:8080
  - Uses Flask's built-in development server with debug mode enabled

### Production Deployment
- **Production server**: Uses gunicorn as specified in `Procfile: web: gunicorn app:app`
- **Live deployment**: https://scooter-reservation.herokuapp.com
- **Platform**: Configured for Heroku with Python buildpack (see `app.json`)

### Dependencies
- **Install dependencies**: `pip install -r requirements.txt`
- **Key dependencies**: Flask 1.0.2, geopy 1.18.1, gunicorn 19.9.0

## Architecture & Data Flow

### Core Components
- **Single-file application**: All logic contained in `app.py`
- **JSON file database**: `scooter_db.json` serves as the data persistence layer
- **Scooter class**: Internal model for representing scooter objects with id, lat, lng, and is_reserved properties

### API Endpoints
1. **GET /**: Redirects to view all available scooters
2. **GET /view_all_available**: Returns all unreserved scooters
3. **GET /search**: Find scooters within a radius of given coordinates
4. **GET /reservation/start**: Reserve a scooter by ID
5. **GET /reservation/end**: End reservation, update location, and process payment

### Data Management Pattern
- `init_db()`: Reads JSON file and converts to Scooter objects
- `write_db()`: Converts Scooter objects back to JSON and persists to file
- All database operations follow read → modify → write pattern

### Payment System
- Currently uses mock payment processing (`payment_gateway()` and `calculate_cost()`)
- Payment is triggered when ending a reservation
- Cost calculation is based on distance traveled (currently 1:1 ratio)
- Returns transaction ID for successful payments

## Important Implementation Details

### Coordinate Validation
- Latitude: Must be in range [-90, 90]
- Longitude: Must be in range [-180, 180]
- Uses geopy library for accurate distance calculations between coordinates

### Error Handling
- Consistent error responses with 422 status code and descriptive messages
- Validates required parameters and data types for all endpoints
- Handles cases like scooter not found, already reserved, or invalid coordinates

### Database State Management
- JSON file acts as persistent storage
- Each request reads entire database into memory
- Modifications write entire database back to file
- No concurrent access protection (suitable for demo/development only)

## Development Notes

### Current Limitations
- No user authentication or session management
- Single-threaded file-based database (not production-ready)
- Mock payment processing system
- Debug mode enabled in production (see TODO in app.py:244)

### Code Structure
- Flask routes handle HTTP requests and parameter validation
- Helper functions manage database operations and business logic
- Scooter class provides object representation and serialization methods
- All business logic is contained within route handlers