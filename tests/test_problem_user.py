from time import sleep
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from conftest import capture_screenshot
from utils.soft_assert import SoftAssert
from utils.base_test import BaseTest

@pytest.mark.usefixtures("browser")
class TestProblemUser(BaseTest):

    @pytest.mark.problem_user_e2e
    def test_all_product_images_and_checkout_failures(self, browser, request):
        login_page = LoginPage(browser)
        product_page = ProductPage(browser)
        cart_page = CartPage(browser)
        checkout_page = CheckoutPage(browser)
        soft_assert = SoftAssert()

        print("\nAttempting to log in as 'problem_user'...")
        login_page.login('problem_user', 'secret_sauce')
        print("Login successful.")
        sleep(2)

        print("Checking if the product list is displayed...")
        is_product_list_displayed = product_page.is_product_list_displayed()

        soft_assert.assert_true(is_product_list_displayed, "Product list is not displayed or returned None for problem user.")
        print("Product list is displayed.")

        expected_images = {
            0: '/static/media/bike-light-1200x1500.37c843b0.jpg',
            2: '/static/media/red-onesie-1200x1500.2ec615b2.jpg',
            4: '/static/media/sauce-backpack-1200x1500.0a0b85a3.jpg',
            6: '/static/media/sauce-pullover-1200x1500.51d7ffaf.jpg',
            8: '/static/media/sauce-bolt-1200x1500.1f10123a.jpg',
            10: '/static/media/red-tatt-1200x1500.30dadef4.jpg'
        }

        actual_broken_image_src = '/static/media/sl-404.168b1cce.jpg'

        print("Waiting for all product images to be loaded...")
        try:
            product_images = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'inventory_item_img'))
            )
        except Exception as e:
            soft_assert.assert_true(False, f"Error while waiting for product images: {str(e)}")
            return

        print("Starting to validate each product image source...")
        for index, product_image in enumerate(product_images):
            if index % 2 == 1:
                continue
            try:
                image_element = WebDriverWait(product_image, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'img'))
                )
                image_src = image_element.get_attribute('src')
                soft_assert.assert_true(image_src == expected_images.get(index),
                                        f"Image {index} does not match. Expected: {expected_images.get(index)}, Found: {image_src}")
                if actual_broken_image_src in image_src:
                    capture_screenshot(browser, f"broken_image_{index}", request)
            except Exception as e:
                soft_assert.assert_true(False, f"Error loading image {index}: {str(e)}")
                capture_screenshot(browser, f"error_loading_image_{index}", request)

        print("Completed validation of all applicable product images.")

        print("Attempting to sort products Z-A or by Price (High to Low)...")
        initial_product_order = product_page.get_inventory_items_order()

        product_page.sort_by_name_z_a()
        sorted_za_product_order = product_page.get_inventory_items_order()
        print(f"Initial order: {initial_product_order}")
        print(f"Order after Z-A sort: {sorted_za_product_order}")
        soft_assert.assert_true(not initial_product_order == sorted_za_product_order,
                                "Sorting Z-A failed as expected for problem_user. No change in product order.")
        capture_screenshot(browser, "problem_user_sorting_validation Z-A", request)
        product_page.sort_by_price_high_low()
        sorted_price_high_low_order = product_page.get_inventory_items_order()
        print(f"Order after High to Low sort: {sorted_price_high_low_order}")

        soft_assert.assert_true(not initial_product_order == sorted_price_high_low_order,
                                "Sorting by Price (High to Low) failed as expected for problem_user. No change in product order.")
        capture_screenshot(browser, "problem_user_sorting_validation High to Low", request)
        print("Sorting validation completed.")

        print("\nAdding first item to the cart...")
        product_page.add_first_item_to_cart()
        print("First item added to the cart.")

        print("Navigating to the cart page...")
        product_page.go_to_cart()
        print("Proceeding to checkout...")
        cart_page.click_checkout()

        print("Entering checkout information (First Name, Last Name, Postal Code)...")
        checkout_page.enter_checkout_information("Fname", "", "12345")
        checkout_page.click_continue()

        print("Checking for checkout error message regarding missing last name...")
        error_message = checkout_page.get_checkout_error_message()

        soft_assert.assert_true("Error: Last Name is required" in error_message,
                                "Expected 'Last Name is required' error not displayed for problem_user.")
        capture_screenshot(browser, "last_name_required_error_message", request)

        print("Entering correct checkout information (First Name, Last Name, Postal Code)...")
        checkout_page.enter_checkout_information("Fname", "Lname", "12345")
        checkout_page.click_continue()

        print("Checking that the checkout proceeds to the next step...")
        is_on_step_two = checkout_page.is_on_checkout_step_two()

        soft_assert.assert_true(is_on_step_two, "Checkout did not proceed to Step 2 after entering valid details.")
        capture_screenshot(browser, "checkout_step_two", request)
        print("Finalizing test and asserting all collected soft assertions.")
        soft_assert.assert_all()


