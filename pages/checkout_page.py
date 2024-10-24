from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_checkout_information(self, first_name, last_name, postal_code):
        self.driver.find_element(By.ID, "first-name").send_keys(first_name)
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)
        self.driver.find_element(By.ID, "continue").click()

    def finish_checkout(self):
        self.driver.find_element(By.ID, "finish").click()


    def click_continue(self):
        self.driver.find_element(By.ID, "continue").click()

    def is_order_complete(self):
        try:
            complete_header = self.driver.find_element(By.CSS_SELECTOR, ".complete-header")
            return complete_header.is_displayed()
        except:
            return False

    def get_checkout_error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".error-message-container").text

    def is_on_checkout_step_two(self):
        return "step-two" in self.driver.current_url
