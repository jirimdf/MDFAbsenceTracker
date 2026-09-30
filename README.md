# MDF Absence Calculator

[![Tests](https://github.com/jirimdf/MDFAbsenceTracker/actions/workflows/tests.yml/badge.svg)](https://github.com/jirimdf/MDFAbsenceTracker/actions/workflows/tests.yml)

A desktop application built with PyQt5 that helps students keep track of school absence. Based on the total number of hours and the hours already missed, it calculates how many more hours you can miss without exceeding the allowed limit.

## Features

- Calculates the maximum number of hours you can still miss (rounded down, so you never go over the limit)
- Shows your current absence percentage
- Shows your future absence percentage including planned absence
- Configurable maximum absence percentage (saved to `settings.txt`)
- Custom graphical interface

## Tech stack

- Python 3
- PyQt5

## Installation

```bash
git clone https://github.com/jirimdf/MDFAbsenceTracker.git
cd MDFAbsenceTracker
pip install -r requirements.txt
```

## Usage

The application files are in the `MDFAbsenceTracker` subfolder:

```bash
python MDFAbsenceTracker/main.py
```

1. Enter **Total hours**, **Hours of absence** and **Planning to miss**.
2. Click **Calculate** to see the results.
3. Click the gear icon to change the maximum allowed absence percentage.

## Screenshot

![example](https://github.com/jirimdf/LupusAbsenceTracker/assets/163419314/573a9e90-86f2-41e7-b8cc-d7f64284652d)

## Tests

```bash
pip install pytest
python -m pytest
```

Tests run automatically on every push via GitHub Actions.

## Notes

- Tested on Windows and Linux.

## License

This project is licensed under the [MIT License](LICENSE).
