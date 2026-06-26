# Internet Speed Test

A simple command-line tool to measure internet speed by downloading files from a specified URL. The tool performs multiple HTTP requests, measures download speed, and provides detailed statistics.

## Features

- 📊 Measures download speed in MB/s
- 🔄 Performs multiple requests for accurate results
- 🌐 Customizable URL for testing
- ⏱️ Automatic timeout handling (30 seconds)
- 📝 Detailed logging with timestamps
- ❌ Comprehensive error handling
- 🎯 Validates URL format before testing
- 📈 Individual request progress tracking

## Requirements

- Python 3.7+
- requests library

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/Arkadi-AK/speed_test_robot.git
cd speed-test

python -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
