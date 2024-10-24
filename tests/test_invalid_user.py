from time import sleep
import pytest
from pages.login_page import LoginPage
from utils.base_test import BaseTest
from utils.soft_assert import SoftAssert
from conftest import capture_screenshot  


@pytest.mark.usefixtures("browser")
class TestInvalidUser(BaseTest):

    @pytest.mark.invalid_user
    def test_invalid_login(self, browser, request):
        login_page = LoginPage(browser)
        soft_assert = SoftAssert()

        try:
            print("\nAttempting to log in as 'invalid_user' with wrong password...")
            login_page.login('invalid_user', 'wrong_password')

            print("Retrieving the error message displayed on login failure...")
            error_message = login_page.get_error_message()
            sleep(2)

            print(f"Verifying the error message. Actual message: '{error_message}'")
            soft_assert.assert_true("Username and password do not match" in error_message,
                                    f"Unexpected error message: {error_message}")

            print("Asserting all conditions.")
            soft_assert.assert_all()

        except Exception as e:
            print(f"An error occurred: {e}")
            capture_screenshot(browser, "invalid_user_login_failure", request)
            raise
        else:
             print("The error message is as expected. Test passed.")
