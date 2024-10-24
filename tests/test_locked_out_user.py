from time import sleep
import pytest
from pages.login_page import LoginPage
from utils.base_test import BaseTest
from utils.soft_assert import SoftAssert
from conftest import capture_screenshot

@pytest.mark.usefixtures("browser")
class TestLockedOutUser(BaseTest):


    @pytest.mark.locked_out_user
    def test_locked_out_user(self, browser, request):
        login_page = LoginPage(browser)
        soft_assert = SoftAssert()

        try:
            print("\nAttempting to log in as 'locked_out_user'...")
            login_page.login('locked_out_user', 'secret_sauce')

            print("Retrieving the error message displayed for locked out user...")
            error_message = login_page.get_error_message()
            sleep(2)

            print(f"Verifying the error message. Actual message: '{error_message}'")
            soft_assert.assert_true("Sorry, this user has been locked out." in error_message,
                                    "Locked out error message not displayed.")

            print("Asserting all conditions.")
            soft_assert.assert_all()

        except Exception as e:
            print(f"An error occurred: {e}")
            capture_screenshot(browser, "locked_out_user_login_failure", request)
            raise
        else:
            print("The error message is as expected. Test passed.")
