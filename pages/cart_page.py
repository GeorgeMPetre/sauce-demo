from selenium.webdriver.common.by import By

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def is_item_in_cart(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "cart_item")) > 0

    def click_checkout(self):
        self.driver.find_element(By.ID, "checkout").click()
