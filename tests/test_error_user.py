from time import sleep

import pytest
from selenium.common import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from conftest import capture_screenshot
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.base_test import BaseTest
from utils.soft_assert import SoftAssert


@pytest.mark.usefixtures("browser")
class TestErrorUser(BaseTest):

    @pytest.mark.error_user
    def test_error_user_checkout_flow(self, browser, request):
        login_page = LoginPage(browser)
        product_page = ProductPage(browser)
        cart_page = CartPage(browser)
        checkout_page = CheckoutPage(browser)
        soft_assert = SoftAssert()

        try:
            print("\nAttempting to log in as 'error_user'...")
            login_page.login('error_user', 'secret_sauce')
            assert login_page.is_login_successful(), "Login failed for 'error_user'."
            print("Login successful.")

            print("Checking if the product list is displayed...")
            soft_assert.assert_true(product_page.is_product_list_displayed(),
                                    "Product list is not displayed for error_user.")
            print("Product list is displayed.")
            print("Sorting products by price: low to high...")
            product_page.sort_by_price_low_high()

            print("Verifying if alert pops up after sorting by price...")
            try:
                WebDriverWait(browser, 3).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert_text = alert.text
                sleep(2)
                print(f"Alert detected with message: {alert_text}")

                soft_assert.assert_true("Sorting is broken!" in alert_text, f"Unexpected alert message: {alert_text}")
                alert.accept()
                print("Alert accepted.")

                capture_screenshot(browser, "error_user_sorting_by_price_alert_handled", request)
            except TimeoutException:
                print("No alert was displayed after sorting by price.")
                soft_assert.assert_true(False, "Sorting alert was not displayed after sorting by price.")
            print("Sorting products by name: A to Z...")
            product_page.sort_by_name_z_a()

            print("Verifying if alert pops up after sorting by name...")
            try:
                WebDriverWait(browser, 3).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert_text = alert.text
                sleep(2)
                print(f"Alert detected with message: {alert_text}")

                soft_assert.assert_true("Sorting is broken!" in alert_text, f"Unexpected alert message: {alert_text}")
                alert.accept()
                print("Alert accepted.")

                capture_screenshot(browser, "error_user_sorting_by_name_alert_handled", request)
            except TimeoutException:
                print("No alert was displayed after sorting by name.")
                soft_assert.assert_true(False, "Sorting alert was not displayed after sorting by name.")

            print("Adding first item to the cart...")
            product_page.add_first_item_to_cart()
            print("First item added to the cart.")

            print("Navigating to the cart page...")
            product_page.go_to_cart()

            print("Verifying that the item is in the cart...")
            soft_assert.assert_true(cart_page.is_item_in_cart(), "Cart is empty after adding item.")
            print("Item is present in the cart.")

            print("Proceeding to checkout...")
            cart_page.click_checkout()

            print("Entering checkout information with missing last name...")
            checkout_page.enter_checkout_information("Jane", "", "54321")
            print("Checkout information entered. Last name left blank.")

            try:
                WebDriverWait(browser, 3).until(EC.url_contains("/checkout-step-two.html"))
                soft_assert.assert_true(False,
                                        "User proceeded to the next step of checkout without entering a last name.")
                capture_screenshot(browser, "error_user_checkout_step_failure", request)
            except TimeoutException:
                print("User was blocked from proceeding to the next checkout step, as expected.")

            print("Verifying if the order is completed...")
            try:
                order_complete_element = WebDriverWait(browser, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".complete-header"))
                )
                if order_complete_element.is_displayed():
                    print("Order completed successfully.")
                else:
                    soft_assert.assert_true(False, "Order was not completed.")
                    capture_screenshot(browser, "error_user_order_not_completed", request)
            except TimeoutException:
                print("Order completion message did not appear.")
                soft_assert.assert_true(False, "Order was not completed.")
                capture_screenshot(browser, "error_user_order_not_completed", request)

            soft_assert.assert_all()

        except UnexpectedAlertPresentException as e:
            print(f"Unexpected alert detected: {e.alert_text}")
            alert = browser.switch_to.alert
            alert.accept()
            capture_screenshot(browser, "unexpected_alert", request)
            print("Unexpected alert handled.")
            soft_assert.assert_true(False, f"Unexpected alert detected: {e.alert_text}")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        else:
            capture_screenshot(browser, "error_user_checkout_flow_success", request)
