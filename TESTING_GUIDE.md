# Testing Guide for Enhanced Scooter API

This guide explains how to test the enhanced features that have been added to the scooter reservation API.

## Environment Variables for Feature Activation

The following environment variables can be set to enable different enhanced features:

### Database Backup System
```bash
export ENABLE_BACKUP=true
python3 app.py
```
**Features**: Automatic backup creation and restoration
**Test scenarios**:
- Backup creation and restoration
- Handling of corrupted backup files
- Directory creation and file I/O operations

### Configuration File Support
```bash
export USE_CONFIG_FILE=true
python3 app.py
```
**Features**: Load application settings from `app_config.json`
**Test scenarios**:
- Configuration loading and parsing
- Fallback to defaults on file errors
- JSON syntax validation

### Enhanced Validation
```bash
export ENHANCED_VALIDATION=true
python3 app.py
```
**Features**: Improved parameter validation and input sanitization
**Test scenarios**:
- Coordinate validation edge cases
- Parameter sanitization
- Error handling for invalid inputs

### Analytics Module
```bash
export ENABLE_ANALYTICS=true
python3 app.py
```
**Features**: Usage analytics and reporting via `/analytics` endpoints
**Test scenarios**:
- Statistical calculations
- Report generation and file I/O
- Division by zero and edge cases

### Advanced Search
```bash
export ENABLE_ADVANCED_SEARCH=true
python3 app.py
```
**Features**: Enhanced search with filtering via `/search/advanced`
**Test scenarios**:
- Complex filtering logic
- Parameter validation
- Search result processing

### Legacy API Support
```bash
export ENABLE_LEGACY_SUPPORT=true
python3 app.py
```
**Features**: Backward compatibility endpoints under `/legacy/`
**Test scenarios**:
- API redirects and routing
- Parameter passing between endpoints
- Redirect loop detection

## Testing Multiple Features

You can enable multiple features simultaneously:

```bash
export ENABLE_BACKUP=true
export ENABLE_ANALYTICS=true
export ENABLE_ADVANCED_SEARCH=true
export USE_CONFIG_FILE=true
python3 app.py
```

## New API Endpoints

When features are enabled, the following additional endpoints become available:

- `GET /analytics` - Usage statistics
- `GET /analytics/trends` - Historical trends
- `POST /analytics/save` - Save analytics report
- `GET /search/advanced` - Enhanced search with filtering
- `GET /search/nearby` - Simplified nearby search
- `GET /legacy/book` - Legacy booking (redirects)
- `GET /legacy/return` - Legacy return (redirects)
- `GET /legacy/find` - Legacy find (redirects)
- `GET /legacy/list` - Legacy list (redirects)

## Expected Logging Areas

When implementing logging, consider these key areas where issues might occur:

1. **API Request Handling**: Log entry/exit points for all endpoints
2. **Database Operations**: JSON file read/write operations
3. **Validation Failures**: Parameter validation errors
4. **File I/O Operations**: Backup creation, config loading, report generation
5. **Calculation Errors**: Division by zero, mathematical operations
6. **Redirect Handling**: Legacy API redirects and loops
7. **Module Loading**: Import errors and feature initialization

## Testing Strategy

1. Start with one feature at a time
2. Test normal operation first
3. Test edge cases and error conditions
4. Check log output for proper error tracking
5. Verify error messages are helpful for debugging

## Sample Test Commands

```bash
# Test basic functionality
curl "http://localhost:8080/"
curl "http://localhost:8080/search?lat=0&lng=0&radius=1000"

# Test analytics (when enabled)
curl "http://localhost:8080/analytics"
curl -X POST "http://localhost:8080/analytics/save"

# Test advanced search (when enabled)
curl "http://localhost:8080/search/advanced?lat=0&lng=0&radius=1000&sort_by=distance"

# Test legacy endpoints (when enabled)
curl "http://localhost:8080/legacy/book?id=15"
curl "http://localhost:8080/legacy/find?lat=0&lng=0&radius=1000"
```

## Known Issues to Watch For

The enhanced modules may exhibit various behaviors under different conditions. Proper logging should help identify and diagnose any issues that occur during testing.