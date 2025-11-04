# Test Suite for Bug Demonstration

This test suite contains 10 unit tests designed to demonstrate both working functionality and the bugs introduced in the enhanced modules.

## Quick Start

Run the complete test suite:
```bash
python3 run_tests.py
```

Or run tests directly:
```bash
python3 test_bug_scenarios.py
```

## Test Breakdown

### ✅ Passing Tests (5)
These tests demonstrate that basic functionality works correctly:

1. **Valid Coordinate Validation** - Normal coordinates pass validation
2. **Config Defaults** - Config loader falls back to defaults properly
3. **Analytics with Valid Data** - Analytics work with good scooter data
4. **Backup System Setup** - Directory creation and initialization work
5. **JSON Validation** - Valid JSON data passes validation

### ❌ Failing Tests (5)
These tests expose the bugs and show where logging would help:

1. **Coordinate Validation Bug** - Latitude validation uses wrong range (-180/180 instead of -90/90)
2. **Config Loader Silent Failure** - Always returns defaults even when config file exists
3. **Analytics Division by Zero** - Crashes when database is empty (no scooters)
4. **Backup JSON Corruption** - Creates invalid JSON backups that can't be restored
5. **Advanced Search Filter Bug** - Ignores filter parameters and returns all results

## Expected Results

When you run the tests, you should see:
- **5 tests PASS** (basic functionality works)
- **5 tests FAIL** (bugs are exposed)
- **Success rate: 50%**

## Logging Guidance

The failing tests highlight areas where comprehensive logging would help students debug issues:

### 1. Parameter Validation Logging
```python
# Example logging for coordinate validation
logger.info(f"Validating coordinates: lat={lat}, lng={lng}")
if not -90 <= lat <= 90:
    logger.error(f"Invalid latitude {lat}: must be between -90 and 90")
    return False
logger.debug("Coordinate validation passed")
```

### 2. Configuration Loading Logging
```python
# Example logging for config operations
logger.info(f"Loading configuration from {config_file}")
if os.path.exists(config_file):
    logger.debug("Config file found, parsing JSON")
    # ... load config ...
    logger.info("Configuration loaded successfully from file")
else:
    logger.warning("Config file not found, using defaults")
```

### 3. Mathematical Operation Logging
```python
# Example logging for analytics calculations
logger.info(f"Calculating utilization rate: {reserved}/{total}")
if total == 0:
    logger.error("Cannot calculate utilization: no scooters in database")
    raise ZeroDivisionError("Division by zero in utilization calculation")
```

### 4. File I/O Operation Logging
```python
# Example logging for backup operations
logger.info(f"Creating backup to {backup_path}")
try:
    # ... create backup ...
    logger.info(f"Backup created successfully: {backup_path}")
except Exception as e:
    logger.error(f"Backup creation failed: {e}")
```

### 5. Business Logic Logging
```python
# Example logging for search filtering
logger.info(f"Applying filters: include_reserved={include_reserved}")
logger.debug(f"Found {len(results)} results before filtering")
# ... apply filters ...
logger.debug(f"Found {len(filtered_results)} results after filtering")
```

## Using Tests for Development

1. **Run tests before adding logging** - See the 5 failures
2. **Add logging to your enhanced modules** - Focus on the failing areas
3. **Run tests again** - Failures should now provide better error messages
4. **Use log output to debug** - Trace through the execution paths

This approach helps students understand where logging is most valuable and how it aids in debugging production issues.