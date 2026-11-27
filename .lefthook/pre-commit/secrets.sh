#!/bin/sh

# Fail with a clear message if gitleaks is not installed
if ! command -v gitleaks >/dev/null 2>&1; then
    echo "gitleaks is not installed. See the CONTRIBUTING.md for installation steps."
    exit 1
fi

# Scan only the staged changes and block the commit if a secret is found
gitleaks git --pre-commit --staged --redact --verbose