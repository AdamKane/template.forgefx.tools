import pytest
import sys
from io import StringIO
from datetime import datetime


def run_tests_and_save_results():
    # Redirect stdout to capture test output
    stdout_backup = sys.stdout
    sys.stdout = StringIO()

    # Run pytest with compact output
    pytest.main(['-v', '-s', '--tb=short'])

    # Get the test output
    output = sys.stdout.getvalue()

    # Restore stdout
    sys.stdout = stdout_backup

    # Shorten separator lines
    output = output.replace('===', '=')

    # Get current time in 12-hour format
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    # Write test results to file with current time at the top
    with open('pytest.log', 'w') as f:
        f.write(f"Test run at: {current_time}\n\n")
        f.write(output)

    # Print test results to console
    print(f"Test run at: {current_time}\n")
    print(output)

    print(f"Test results have been written to 'pytest.log' in the project root")

if __name__ == '__main__':
    run_tests_and_save_results()
