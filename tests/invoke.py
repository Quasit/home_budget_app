import pytest
import sys

# Invoke tests with coverage report in terminal

if __name__ == "__main__":
    sys.exit(pytest.main(["--cov-report", "term", "--cov=script/"]))
