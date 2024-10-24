# SauceDemo Cross-Browser Testing with PyTest and Selenium

This project contains a comprehensive suite of cross-browser tests for [SauceDemo](https://www.saucedemo.com) using Python, PyTest, and Selenium WebDriver. It covers various user scenarios and validates functionality across Chrome, Firefox, and Edge browsers.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Setup](#setup)
- [Running the Tests](#running-the-tests)
- [Test Scenarios](#test-scenarios)
- [Soft Assertions](#soft-assertions)
- [Reports](#reports)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The purpose of this project is to automate the end-to-end testing of the SauceDemo website using Selenium WebDriver. The tests ensure functionality like login, product sorting, cart management, and checkout flow works correctly for various user types, including edge cases like performance glitches and locked-out users.

## Features

- **Cross-Browser Support**: Tests run on Chrome, Firefox, and Edge using WebDriver Manager.
- **User Scenarios**: Tests for various users:
  - `standard_user`
  - `locked_out_user`
  - `problem_user`
  - `performance_glitch_user`
  - `visual_user`
  - `error_user`
  - `invalid_user`
- **Soft Assertions**: Allows for multiple verification points before failing the test.
- **Screenshots**: Captures screenshots on test failures and key steps.
- **HTML Test Reports**: Generates detailed HTML reports with embedded screenshots.

## Setup

### Prerequisites

- Python 3.12.6
- [PyTest](https://docs.pytest.org/en/latest/) (v8.3.3)
- [Selenium](https://www.selenium.dev/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- Supported browsers: Chrome, Firefox, Edge
- ChromeDriver, GeckoDriver (Firefox), EdgeDriver

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/GeorgeMPetre/sauce-demo.git
    cd sauce_demo_project
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Tests

To run the tests for all supported browsers, use:
```bash
pytest --browser chrome
pytest --browser firefox
pytest --browser edge

