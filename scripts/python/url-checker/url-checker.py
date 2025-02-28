name: Check Broken Links

on:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at midnight
  push:
    branches:
      - canary
      - main
  workflow_dispatch:

jobs:
  url-check:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests colorama

    - name: Enable Color Output
      run: echo "FORCE_COLOR=1" >> $GITHUB_ENV
      
    - name: Check for broken links
      id: check_links
      run: |
        python scripts/python/url-checker/url-checker.py
        echo "LINK_CHECK_EXIT_CODE=$?" >> $GITHUB_ENV

    - name: Upload log file
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: url-checker-log
        path: scripts/python/url-checker/logs/*.log

    - name: Clean up environment
      if: always()
      run: rm -rf scripts/python/url-checker/__pycache__
      
    - name: Report final status
      if: env.LINK_CHECK_EXIT_CODE != '0'
      run: |
        echo "::error::Broken links were found in the documentation. See uploaded logs for details."
        exit 1
