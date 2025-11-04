# Functional Test Suite

This test suite is organized by functionality areas, following realistic software engineering practices. Each test module focuses on a specific functional domain of the scooter reservation API.

## Test Organization

### 🗃️ **Database Tests** (`test_database.py`)
Tests backup and restore functionality for the scooter database.

**Test Coverage:**
- Backup system initialization
- Backup file creation
- Data integrity during restore operations
- Backup file listing and management

**Key Test:** `test_backup_restore_integrity` - Verifies backups can be restored without data corruption

### ✅ **Validation Tests** (`test_validation.py`)
Tests input validation and parameter sanitization.

**Test Coverage:**
- Coordinate validation (latitude/longitude ranges)
- Parameter boundary checking
- Radius value validation
- Scooter ID format validation
- JSON data structure validation

**Key Tests:**
- `test_invalid_coordinates_rejected` - Ensures invalid coordinates are caught
- `test_negative_radius_handling` - Validates radius parameter constraints

### ⚙️ **Configuration Tests** (`test_configuration.py`)
Tests configuration loading and management functionality.

**Test Coverage:**
- Default configuration fallback behavior
- Configuration file parsing
- Malformed configuration handling
- Dynamic configuration reloading
- Nested configuration key access

**Key Test:** `test_config_file_parsing` - Verifies custom configurations are loaded properly

### 📊 **Analytics Tests** (`test_analytics.py`) *[Requires Flask]*
Tests usage analytics and reporting calculations.

**Test Coverage:**
- Usage report generation
- Utilization rate calculations
- Geographic distribution analysis
- Report file I/O operations
- Historical trend analysis

**Key Test:** `test_empty_database_handling` - Tests graceful handling of edge cases

### 🌐 **API Endpoint Tests** (`test_api_endpoints.py`) *[Requires Flask]*
Tests advanced search and legacy API endpoint behavior.

**Test Coverage:**
- Advanced search functionality
- Parameter filtering logic
- Legacy endpoint redirection
- Query parameter preservation
- Endpoint error handling

**Key Test:** `test_advanced_search_reservation_filter` - Validates search filtering logic

## Running Tests

### Quick Start
```bash
python3 run_tests.py
```

### Individual Test Modules
```bash
python3 -m unittest test_database
python3 -m unittest test_validation
python3 -m unittest test_configuration
```

### With Flask Dependencies
```bash
pip install flask
python3 run_tests.py  # Runs all tests including Flask-dependent ones
```

## Expected Results

The test suite is designed to catch real production issues:

### ✅ **Passing Tests (13/19 - 68.4%)**
These demonstrate that core functionality works as expected:
- Basic validation for typical use cases
- Default configuration loading
- Backup system setup and file operations
- Standard parameter handling

### 🐛 **Failing Tests (6/19 - 31.6%)**
These expose issues that would occur in production:

1. **Backup Corruption** - JSON backup files are malformed
2. **Invalid Coordinate Acceptance** - Latitude validation uses wrong range
3. **Negative Radius Allowed** - Missing boundary validation
4. **JSON Validation Bypass** - Malformed JSON marked as valid
5. **Config File Ignored** - Valid config files not loaded
6. **Config Reload Failure** - Dynamic reloading doesn't work

## Logging Guidance

Each failing test represents a scenario where proper logging would help:

### Database Operations Logging
```python
logger.info(f"Creating backup to {backup_path}")
try:
    # Backup creation logic
    logger.debug("Backup JSON serialization completed")
except Exception as e:
    logger.error(f"Backup creation failed: {e}")
```

### Validation Logging
```python
logger.debug(f"Validating coordinates: lat={lat}, lng={lng}")
if not -90 <= lat <= 90:
    logger.warning(f"Invalid latitude {lat}: outside valid range")
    return False
```

### Configuration Logging
```python
logger.info(f"Loading configuration from {config_file}")
if config_loaded_successfully:
    logger.info(f"Configuration loaded: {loaded_values}")
else:
    logger.warning("Config file invalid, using defaults")
```

## Educational Value

This test suite teaches students:

1. **Realistic Test Organization** - Tests grouped by functionality, not by success/failure
2. **Production Issue Patterns** - Common failure modes in real applications
3. **Logging Requirements** - Where instrumentation is most valuable
4. **Test-Driven Debugging** - Using test failures to guide logging implementation

## Code Review Usage

1. **Run full test suite** - Show overall system health (68.4% pass rate)
2. **Focus on failures** - Each failure shows where logging would help
3. **Demonstrate debugging** - How logs would trace through failed scenarios
4. **Validate student logging** - Check if their logs capture the failure points
5. **Iterate on coverage** - Ensure logging covers all functional areas

The realistic organization makes this suitable for production codebases while still serving as an effective teaching tool for logging best practices.