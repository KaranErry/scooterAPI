#!/usr/bin/env python3
"""
Comprehensive test runner for the scooter reservation API.
Runs unit tests for all functional modules.
"""

import sys
import os
import unittest
import importlib

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables to enable features
os.environ['ENABLE_BACKUP'] = 'true'
os.environ['USE_CONFIG_FILE'] = 'true'
os.environ['ENHANCED_VALIDATION'] = 'true'
os.environ['ENABLE_ANALYTICS'] = 'true'
os.environ['ENABLE_ADVANCED_SEARCH'] = 'true'
os.environ['ENABLE_LEGACY_SUPPORT'] = 'true'

def check_dependencies():
    """Check which dependencies are available."""
    dependencies = {
        'flask': False,
        'analytics': False,
        'advanced_search': False,
        'legacy_support': False
    }

    try:
        import flask
        dependencies['flask'] = True
    except ImportError:
        pass

    if dependencies['flask']:
        try:
            import analytics
            dependencies['analytics'] = True
        except ImportError:
            pass

        try:
            import advanced_search
            dependencies['advanced_search'] = True
        except ImportError:
            pass

        try:
            import legacy_support
            dependencies['legacy_support'] = True
        except ImportError:
            pass

    return dependencies

def discover_and_run_tests():
    """Discover and run all test modules."""
    print("=" * 60)
    print("SCOOTER API FUNCTIONAL TEST SUITE")
    print("=" * 60)

    # Check dependencies
    deps = check_dependencies()
    print("Dependency Status:")
    for dep, available in deps.items():
        status = "✓ Available" if available else "✗ Missing"
        print(f"  {dep:15} {status}")
    print()

    # Test modules to run
    test_modules = [
        ('test_database', 'Database Backup Tests'),
        ('test_validation', 'Input Validation Tests'),
        ('test_configuration', 'Configuration Management Tests'),
    ]

    # Add Flask-dependent tests if available
    if deps['flask'] and deps['analytics']:
        test_modules.append(('test_analytics', 'Analytics & Reporting Tests'))

    if deps['flask'] and deps['advanced_search'] and deps['legacy_support']:
        test_modules.append(('test_api_endpoints', 'API Endpoint Tests'))

    print(f"Running {len(test_modules)} test suites:")
    print("-" * 60)

    total_tests = 0
    total_failures = 0
    total_errors = 0
    suite_results = []

    for module_name, description in test_modules:
        try:
            print(f"\n📋 {description}")
            print("-" * 40)

            # Import and run the test module
            module = importlib.import_module(module_name)
            suite = unittest.TestLoader().loadTestsFromModule(module)
            runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
            result = runner.run(suite)

            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)

            total_tests += tests_run
            total_failures += failures
            total_errors += errors

            suite_results.append({
                'name': description,
                'tests': tests_run,
                'failures': failures,
                'errors': errors,
                'success': tests_run - failures - errors
            })

            print(f"   Tests: {tests_run}, Passed: {tests_run - failures - errors}, Failed: {failures + errors}")

        except Exception as e:
            print(f"   ❌ Error running {module_name}: {e}")
            suite_results.append({
                'name': description,
                'tests': 0,
                'failures': 0,
                'errors': 1,
                'success': 0
            })

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for result in suite_results:
        status = "✓" if result['failures'] + result['errors'] == 0 else "✗"
        print(f"{status} {result['name']}")
        print(f"    {result['success']}/{result['tests']} passed")

    print(f"\nOverall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_tests - total_failures - total_errors}")
    print(f"  Failed: {total_failures + total_errors}")

    success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
    print(f"  Success Rate: {success_rate:.1f}%")

    if total_failures + total_errors > 0:
        print(f"\n🐛 Found {total_failures + total_errors} issues across functional areas.")
        print("💡 These failures indicate where logging would help debug problems:")
        print("   • Database operations (backup/restore)")
        print("   • Input validation (coordinates, parameters)")
        print("   • Configuration management (file parsing)")
        if deps['analytics']:
            print("   • Analytics calculations (division by zero)")
        if deps['advanced_search']:
            print("   • API endpoint behavior (filtering, redirects)")
        print("\nEach failure represents a realistic production scenario where")
        print("proper logging would help developers identify and fix issues.")
    else:
        print("\n✅ All tests passed! No issues found in functional areas.")

    print("=" * 60)

if __name__ == '__main__':
    discover_and_run_tests()