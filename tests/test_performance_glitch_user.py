import time
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.base_test import BaseTest
from utils.soft_assert import SoftAssert
from conftest import capture_screenshot


@pytest.mark.usefixtures("browser")
class TestPerformanceGlitchUser(BaseTest):


    @pytest.mark.performance_glitch_user_e2e
    def test_performance_glitch_user_login_time(self, browser, request):
        login_page = LoginPage(browser)
        product_page = ProductPage(browser)
        cart_page = CartPage(browser)
        checkout_page = CheckoutPage(browser)
        soft_assert = SoftAssert()

        try:
            print("\nAttempting to log in as 'performance_glitch_user'...")
            start_time = time.time()
            login_page.login('performance_glitch_user', 'secret_sauce')
            end_time = time.time()
            login_duration = end_time - start_time

            print("Verifying if the login time exceeds 5 seconds...")
            if login_duration <= 5:
                print("Login successful and took less than or equal to 5 seconds.")
                soft_assert.assert_true(True, "Test passed: Login took less than or equal to 5 seconds.")
            else:
                print(f"Test failed: Login took more than 5 seconds.")
                soft_assert.assert_true(False, f"Test failed: Login took more than 5 seconds. It took {login_duration:.2f} seconds.")
                capture_screenshot(browser, "performance_glitch_user_login_time_failure", request)
            print(f"Login took {login_duration:.2f} seconds.")

            print("Checking if the product list is displayed...")
            soft_assert.assert_true(product_page.is_product_list_displayed(),
                                    "Product list is not displayed after login.")
            print("Product list is displayed.")

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

            print("Entering checkout information...")
            checkout_page.enter_checkout_information("John", "Doe", "12345")
            print("Checkout information entered.")

            print("Completing the order...")
            checkout_page.finish_checkout()

            print("Verifying if the order is completed...")
            try:
                order_complete_element = WebDriverWait(browser, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".complete-header"))
                )
                if order_complete_element.is_displayed():
                    print("Order completed successfully.")
                    soft_assert.assert_true(True, "Order completed successfully.")
                else:
                    print("Order completion message not displayed.")
                    soft_assert.assert_true(False, "Order was not completed.")
            except TimeoutException:
                print("Order completion message did not appear.")
                soft_assert.assert_true(False, "Order was not completed.")
                capture_screenshot(browser, "performance_glitch_user_order_not_completed", request)

            print("Asserting all conditions.")
            soft_assert.assert_all()

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        else:
            print("Test completed successfully.")
