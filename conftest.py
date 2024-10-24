import pytest
import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pytest_html import extras


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")


@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption("--browser")

    print(f"\nLaunching browser: {browser_name}")

    if browser_name == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.headless = False
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_name == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.maximize_window()
    driver.get("https://www.saucedemo.com")

    # Add the URL as an extra in the report
    if request.config.pluginmanager.hasplugin('html'):
        extra_url = extras.url("https://www.saucedemo.com", "SauceDemo Home Page")
        request.node._report_extra.append(extra_url)

    yield driver

    print(f"\nClosing browser: {browser_name}")
    driver.quit()

    print(f"\nBrowser {browser_name} closed.")


def capture_screenshot(browser, name, request):
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot_name = f"{screenshot_dir}/{name}_{int(time.time())}.png"
    browser.save_screenshot(screenshot_name)
    print(f"Screenshot captured: {screenshot_name}")

    if request.config.pluginmanager.hasplugin('html'):
        with open(screenshot_name, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        html_img = f'<div style="clear: both; float: right; margin-bottom: 10px;">' \
                   f'<img src="data:image/png;base64,{encoded_image}" style="width:200px;height:100px;" ' \
                   f'onclick="this.style.width=\'600px\';this.style.height=\'400px\'" /></div>'
        extra = extras.html(html_img)
        request.node._report_extra.append(extra)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    item._report_extra = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        report.extra = getattr(item, '_report_extra', [])


@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    report.title = "SauceDemo Test Report with Screenshots"
