import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.base_test import BaseTest
from utils.soft_assert import SoftAssert
from conftest import capture_screenshot


@pytest.mark.usefixtures("browser")
class TestStandardUser(BaseTest):

    @pytest.mark.standard_user
    def test_standard_user_checkout_flow(self, browser, request):
        login_page = LoginPage(browser)
        product_page = ProductPage(browser)
        cart_page = CartPage(browser)
        checkout_page = CheckoutPage(browser)
        soft_assert = SoftAssert()

        try:
            print("\nLogging in as standard_user")
            login_page.login('standard_user', 'secret_sauce')

            print("Checking if the product list is displayed")
            soft_assert.assert_true(product_page.is_product_list_displayed(),
                                    "Product list is not displayed for standard user.")

            print("Adding the first item to the cart")
            product_page.add_first_item_to_cart()

            print("Navigating to the cart page")
            product_page.go_to_cart()

            print("Verifying if the item is in the cart")
            soft_assert.assert_true(cart_page.is_item_in_cart(), "Cart is empty after adding item.")

            print("Proceeding to the checkout")
            cart_page.click_checkout()

            print("Entering checkout information (John Doe, 12345)")
            checkout_page.enter_checkout_information("John", "Doe", "12345")

            print("Finishing the checkout process")
            checkout_page.finish_checkout()

            print("Verifying if the order was completed successfully")
            soft_assert.assert_true(checkout_page.is_order_complete(), "Order was not completed successfully.")

            print("Asserting all conditions")
            soft_assert.assert_all()
            print("Order completed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            capture_screenshot(browser, "standard_user_checkout_flow_failure", request)
            raise




