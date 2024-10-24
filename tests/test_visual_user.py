import time
import pytest
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
class TestVisualUser(BaseTest):

    @pytest.mark.test_visual_user
    def test_visual_user(self, browser, request):
        login_page = LoginPage(browser)
        product_page = ProductPage(browser)
        cart_page = CartPage(browser)
        checkout_page = CheckoutPage(browser)
        soft_assert = SoftAssert()

        try:
            print("\nAttempting to log in as 'visual_user'...")
            login_page.login("visual_user", "secret_sauce")
            print("Login attempt completed.")

            time.sleep(2)

            print("Checking if we are on the inventory page...")
            soft_assert.assert_true(browser.current_url.endswith("/inventory.html"),
                                    "Login failed: Not on inventory page.")

            print("Checking if inventory items are present...")
            time.sleep(2)
            items_present = browser.find_elements(By.CLASS_NAME, "inventory_item")
            soft_assert.assert_true(len(items_present) > 0, "No inventory items found.")
            print(f"Number of inventory items found: {len(items_present)}")

            print("Waiting for the Sauce Labs Backpack image element to be loaded...")
            wait = WebDriverWait(browser, 10)
            image_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//img[@alt='Sauce Labs Backpack']")
                )
            )

            actual_image_src = image_element.get_attribute("src")
            expected_image_src = "/static/media/sauce-backpack-1200x1500.0a0b85a3.jpg"
            incorrect_image_src = "/static/media/sl-404.168b1cce.jpg"

            print(f"Actual image src found: {actual_image_src}")

            soft_assert.assert_true(
                actual_image_src == expected_image_src,
                f"Expected the Sauce Labs Backpack image, but got: {actual_image_src}"
            )

            time.sleep(1)
            capture_screenshot(browser, "visual_user_inventory_page_Sauce_Labs_Backpack_image_check", request)

            soft_assert.assert_true(
                actual_image_src != incorrect_image_src,
                f"Unexpected incorrect image displayed: {actual_image_src}"
            )

            print("Checking the cart element's position on the product page...")
            cart_element = browser.find_element(By.CSS_SELECTOR, ".primary_header .shopping_cart_container")
            top_position_product_page = cart_element.value_of_css_property("top")
            right_position_product_page = cart_element.value_of_css_property("right")

            if top_position_product_page == "40px" or right_position_product_page == "205px":
                print(f"Cart misalignment detected on the product page. Capturing screenshot...")
                time.sleep(1)
                capture_screenshot(browser, "visual_user_product_page_cart_alignment_issue_on_product_page", request)

            soft_assert.assert_true(top_position_product_page != "40px",
                                    f"Expected cart top position on product page to be '10px', but got {top_position_product_page}")
            soft_assert.assert_true(right_position_product_page != "205px",
                                    f"Expected cart right position on product page to be '20px', but got {right_position_product_page}")
            print(f"Cart top position on product page: {top_position_product_page} instead of '10px'")
            print(f"Cart right position on product page: {right_position_product_page} instead of '20px'")

            print("Sorting products by price (low to high)...")
            sort_selector = browser.find_element(By.CLASS_NAME, "product_sort_container")
            sort_selector.click()
            low_high_option = browser.find_element(By.XPATH, "//option[@value='lohi']")
            low_high_option.click()
            time.sleep(2)

            print("Collecting sorted prices...")
            price_elements = browser.find_elements(By.CLASS_NAME, "inventory_item_price")
            prices = [float(price.text.replace("$", "")) for price in price_elements]

            print(f"Prices after sorting: {prices}")

            sorted_prices = sorted(prices)
            if prices != sorted_prices:
                print("Prices are not sorted in ascending order. Capturing screenshot...")
                capture_screenshot(browser, "visual_user_product_page_price_sorting_issue", request)

            soft_assert.assert_true(prices == sorted_prices, "Prices are not sorted in ascending order.")

            print("Adding an item to the cart...")
            product_page.add_first_item_to_cart()
            time.sleep(2)

            print("Navigating to the cart page...")
            product_page.go_to_cart()

            print("Checking if items are in the cart...")
            time.sleep(1)
            cart_items = browser.find_elements(By.CLASS_NAME, "cart_item")
            soft_assert.assert_true(len(cart_items) > 0, "Cart is empty.")
            print(f"Number of items in the cart: {len(cart_items)}")

            print("Checking if the checkout button is part of the footer...")
            checkout_button = browser.find_element(By.ID, "checkout")
            parent_element = checkout_button.find_element(By.XPATH, "..")
            parent_class = parent_element.get_attribute("class")

            if "footer" not in parent_class:
                print(f"Checkout button is not part of the footer. Capturing screenshot...")
                time.sleep(1)
                capture_screenshot(browser, "visual_user_cart_page_checkout_button_incorrect_position", request)

            soft_assert.assert_true("footer" not in parent_class, "Checkout button is not part of the footer.")
            capture_screenshot(browser, "visual_user_cart_page_checkout_button_incorrect_position", request)

            print("Proceeding to checkout...")
            cart_page.click_checkout()

            print("Entering checkout information...")
            checkout_page.enter_checkout_information("John", "Doe", "12345")
            time.sleep(2)

            print("Finishing the checkout process...")
            checkout_page.finish_checkout()

            print("Verifying if the order is completed...")
            try:
                time.sleep(1)
                order_complete_element = browser.find_element(By.CSS_SELECTOR, ".complete-header")
                if order_complete_element.is_displayed():
                    print("Order completed successfully.")
                else:
                    soft_assert.assert_true(False, "Order was not completed successfully.")
            except Exception as e:
                print(f"An error occurred during order completion check: {e}")
                soft_assert.assert_true(False, "Order completion element not found or not visible.")

            soft_assert.assert_all()

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        else:
            print("Test passed. All assertions passed.")
